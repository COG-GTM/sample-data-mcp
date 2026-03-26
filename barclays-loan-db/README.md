# Barclays UK Synthetic Loan Database

A PostgreSQL database containing realistic synthetic loan data modelled on a UK retail and commercial bank (Barclays-style). Designed for demonstrating data analyst capabilities.

## Connection Details

| Parameter | Value |
|-----------|-------|
| Host | `localhost` |
| Port | `5432` |
| Database | `barclays_loans` |
| Username | `barclays_admin` |
| Password | Set via `BARCLAYS_DB_PASS` environment variable |
| Connection String | `postgresql://barclays_admin:<password>@localhost:5432/barclays_loans` |

## Setup

```bash
# Set the database password
export BARCLAYS_DB_PASS="your_password_here"

# Run the bootstrap script
./bootstrap.sh
```

## Schema Overview (15 Tables)

### Core Customer Data
- **customers** (5,000 rows) — Customer profiles with KYC, segmentation (Basic/Standard/Premium/Private), risk categories
- **customer_addresses** (6,509 rows) — UK residential and previous addresses with postcodes
- **employment_details** (5,000 rows) — Income, employer, industry sector, employment status

### Accounts & Products
- **accounts** (8,925 rows) — Current, savings, and loan servicing accounts with balances
- **loan_products** (15 rows) — Product catalogue: mortgages, personal loans, auto finance, business loans, buy-to-let, bridging

### Loan Lifecycle
- **loan_applications** (8,000 rows) — Full application pipeline with credit scoring, DTI, LTV, affordability, underwriting decisions
- **loans** (4,625 rows) — Active and historical loans across all product types
- **collateral** (3,299 rows) — Property valuations, vehicle assets, commercial premises
- **payment_schedule** (187,122 rows) — Full amortisation schedules
- **payments** (165,699 rows) — Actual payment transactions with methods and statuses

### Risk & Compliance
- **credit_bureau_data** (9,943 rows) — Experian/Equifax/TransUnion scores, CCJs, bankruptcies, IVAs
- **risk_ratings** (4,625 rows) — PD/LGD/EAD, IFRS 9 staging, internal ratings (AAA→D), provisions
- **collections** (530 rows) — Arrears management, contact attempts, recovery outcomes
- **loan_covenants** (917 rows) — Business loan covenants with compliance tracking

### Analytics
- **loan_performance_monthly** (51,083 rows) — 12-month rolling snapshots for trend analysis

## Portfolio Summary

| Product Category | Loans | Originated (£M) | Current Balance (£M) | Avg Rate |
|-----------------|-------|------------------|---------------------|----------|
| Mortgage | 1,952 | 557.4 | 411.0 | 5.24% |
| Buy-to-Let | 623 | 183.5 | 138.5 | 5.87% |
| Business Loan | 453 | 72.0 | 37.0 | 6.79% |
| Personal Loan | 1,142 | 16.3 | 5.3 | 6.21% |
| Auto Finance | 409 | 8.9 | 2.2 | 7.44% |
| Bridging Loan | 46 | 1.6 | 0.2 | 9.31% |

## Example Queries for Demo

### 1. Portfolio Risk Dashboard
```sql
SELECT lp.product_category, l.loan_status, COUNT(*) as loans,
       ROUND(SUM(l.current_balance)/1e6, 2) as balance_mm,
       ROUND(AVG(rr.pd_score)*100, 2) as avg_pd_pct
FROM loans l
JOIN loan_products lp ON l.product_id = lp.product_id
LEFT JOIN risk_ratings rr ON l.loan_id = rr.loan_id
GROUP BY lp.product_category, l.loan_status
ORDER BY 1, 3 DESC;
```

### 2. IFRS 9 Provisioning Report
```sql
SELECT rr.ifrs9_stage, rr.regulatory_category,
       COUNT(*) as loans,
       ROUND(SUM(rr.ead_amount)/1e6, 2) as ead_mm,
       ROUND(SUM(rr.provision_amount)/1e6, 2) as provisions_mm
FROM risk_ratings rr
GROUP BY rr.ifrs9_stage, rr.regulatory_category
ORDER BY rr.ifrs9_stage;
```

### 3. Customer Segmentation Analysis
```sql
SELECT c.customer_segment, c.risk_category,
       COUNT(DISTINCT c.customer_id) as customers,
       COUNT(l.loan_id) as loans,
       ROUND(AVG(e.annual_income), 0) as avg_income,
       ROUND(AVG(l.principal_amount), 0) as avg_loan
FROM customers c
LEFT JOIN loans l ON c.customer_id = l.customer_id
LEFT JOIN employment_details e ON c.customer_id = e.customer_id
GROUP BY c.customer_segment, c.risk_category
ORDER BY 1, 2;
```

### 4. Arrears & Collections Pipeline
```sql
SELECT co.collection_stage,
       COUNT(*) as cases,
       ROUND(SUM(co.arrears_amount), 0) as total_arrears,
       ROUND(AVG(co.days_in_arrears), 0) as avg_dpd,
       SUM(CASE WHEN co.arrangement_in_place THEN 1 ELSE 0 END) as with_arrangements
FROM collections co
GROUP BY co.collection_stage
ORDER BY avg_dpd;
```

### 5. Monthly Performance Trend
```sql
SELECT snapshot_date,
       COUNT(*) as loans,
       ROUND(SUM(outstanding_balance)/1e6, 2) as balance_mm,
       ROUND(AVG(days_past_due), 1) as avg_dpd,
       ROUND(SUM(provision_amount)/1e6, 4) as provisions_mm
FROM loan_performance_monthly
GROUP BY snapshot_date
ORDER BY snapshot_date;
```

## Files

- `schema.sql` — DDL for all 15 tables + indexes
- `generate_data.py` — Python script to regenerate data
- `load_data.sql` — COPY commands to load CSVs
- `data/` — CSV files for all tables
