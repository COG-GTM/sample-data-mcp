#!/bin/bash
# ============================================================
# Barclays Loan Database Bootstrap Script
# Sets up PostgreSQL with synthetic loan data from scratch
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Database credentials from environment variables
DB_NAME="${BARCLAYS_DB_NAME:-barclays_loans}"
DB_USER="${BARCLAYS_DB_USER:-barclays_admin}"
DB_PASS="${BARCLAYS_DB_PASS:?Error: BARCLAYS_DB_PASS environment variable must be set}"

echo "=== Barclays Loan DB Bootstrap ==="

# 1. Install PostgreSQL if not present
if ! command -v psql &>/dev/null; then
    echo "Installing PostgreSQL..."
    sudo apt-get update -qq && sudo apt-get install -y -qq postgresql postgresql-contrib > /dev/null 2>&1
fi

# 2. Ensure PostgreSQL is running
if ! pg_isready -q 2>/dev/null; then
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql
    sleep 2
fi

# 3. Check if database already exists and is fully set up
DB_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" 2>/dev/null || echo "")
if [ "$DB_EXISTS" = "1" ]; then
    echo "Database '$DB_NAME' already exists. Checking tables..."
    TABLE_COUNT=$(PGPASSWORD="$DB_PASS" psql -h localhost -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'" 2>/dev/null || echo "0")
    if [ "$TABLE_COUNT" -ge "15" ]; then
        echo "Database is fully set up with $TABLE_COUNT tables. Nothing to do."
        exit 0
    fi
    echo "Database exists but incomplete ($TABLE_COUNT tables). Dropping and recreating..."
    sudo -u postgres psql -c "DROP DATABASE $DB_NAME;" 2>/dev/null || true
fi

# 4. Create database and user
echo "Creating database and user..."
sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $DB_USER;"

# 5. Create schema
echo "Creating schema..."
cp "$SCRIPT_DIR/schema.sql" /tmp/schema.sql
chmod a+r /tmp/schema.sql
sudo -u postgres psql -d "$DB_NAME" -f /tmp/schema.sql

# 6. Fix covenant column precision before loading data
sudo -u postgres psql -d "$DB_NAME" -c "ALTER TABLE loan_covenants ALTER COLUMN threshold_value TYPE NUMERIC(14, 4); ALTER TABLE loan_covenants ALTER COLUMN last_tested_value TYPE NUMERIC(14, 4);"

# 7. Generate synthetic data
echo "Generating synthetic data..."
python3 "$SCRIPT_DIR/generate_data.py"

# 8. Load data
echo "Loading data into PostgreSQL..."
cp -r "$SCRIPT_DIR/data" /tmp/barclays_data
chmod -R a+rX /tmp/barclays_data

# Fix load_data.sql paths to use /tmp
sed 's|/home/ubuntu/barclays_loan_db/data|/tmp/barclays_data|g' "$SCRIPT_DIR/load_data.sql" > /tmp/load_data.sql
chmod a+r /tmp/load_data.sql
sudo -u postgres psql -d "$DB_NAME" -f /tmp/load_data.sql

# 9. Grant permissions
echo "Granting permissions..."
sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;"
sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;"

# 10. Configure for external connections
PG_CONF=$(sudo -u postgres psql -tAc "SHOW config_file;" 2>/dev/null | tr -d ' ')
PG_HBA=$(sudo -u postgres psql -tAc "SHOW hba_file;" 2>/dev/null | tr -d ' ')

if ! grep -q "listen_addresses = '\*'" "$PG_CONF" 2>/dev/null; then
    sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"
    sudo sed -i "s/listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"
fi

if ! grep -q "$DB_USER" "$PG_HBA" 2>/dev/null; then
    echo "host    $DB_NAME  $DB_USER  0.0.0.0/0       md5" | sudo tee -a "$PG_HBA" > /dev/null
fi

sudo systemctl restart postgresql
sleep 2

# 11. Verify
echo ""
echo "=== Verification ==="
PGPASSWORD="$DB_PASS" psql -h localhost -U "$DB_USER" -d "$DB_NAME" -c "
SELECT 'customers' as tbl, count(*) FROM customers
UNION ALL SELECT 'loans', count(*) FROM loans
UNION ALL SELECT 'payments', count(*) FROM payments
UNION ALL SELECT 'risk_ratings', count(*) FROM risk_ratings
ORDER BY 1;"

echo ""
echo "=== Barclays Loan DB Ready ==="
echo "Connection: postgresql://$DB_USER@localhost:5432/$DB_NAME"
