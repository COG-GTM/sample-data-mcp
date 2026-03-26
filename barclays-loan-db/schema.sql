-- ============================================================
-- Barclays UK Synthetic Loan Database Schema
-- ============================================================
-- Covers: Customers, Addresses, Employment, Accounts,
--         Loan Products, Loan Applications, Loans, Collateral,
--         Payment Schedules, Payments, Collections, Risk Ratings,
--         Credit Bureau Data, and Loan Performance Metrics
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- 1. CUSTOMERS
-- ============================================================
CREATE TABLE customers (
    customer_id         VARCHAR(12) PRIMARY KEY,
    title               VARCHAR(10),
    first_name          VARCHAR(100) NOT NULL,
    last_name           VARCHAR(100) NOT NULL,
    date_of_birth       DATE NOT NULL,
    gender              VARCHAR(10),
    email               VARCHAR(255),
    phone_primary       VARCHAR(20),
    phone_secondary     VARCHAR(20),
    national_insurance  VARCHAR(15),  -- UK NI number format
    customer_segment    VARCHAR(20) NOT NULL CHECK (customer_segment IN ('Basic', 'Standard', 'Premium', 'Private')),
    customer_since      DATE NOT NULL,
    kyc_status          VARCHAR(20) NOT NULL DEFAULT 'Verified' CHECK (kyc_status IN ('Verified', 'Pending', 'Failed', 'Expired')),
    risk_category       VARCHAR(20) DEFAULT 'Standard' CHECK (risk_category IN ('Low', 'Standard', 'Medium', 'High', 'Very High')),
    is_politically_exposed BOOLEAN DEFAULT FALSE,
    marketing_consent   BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 2. CUSTOMER ADDRESSES
-- ============================================================
CREATE TABLE customer_addresses (
    address_id          SERIAL PRIMARY KEY,
    customer_id         VARCHAR(12) NOT NULL REFERENCES customers(customer_id),
    address_type        VARCHAR(20) NOT NULL CHECK (address_type IN ('Residential', 'Correspondence', 'Previous')),
    address_line_1      VARCHAR(255) NOT NULL,
    address_line_2      VARCHAR(255),
    city                VARCHAR(100) NOT NULL,
    county              VARCHAR(100),
    postcode            VARCHAR(10) NOT NULL,
    country             VARCHAR(3) NOT NULL DEFAULT 'GBR',
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    resident_since      DATE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 3. EMPLOYMENT DETAILS
-- ============================================================
CREATE TABLE employment_details (
    employment_id       SERIAL PRIMARY KEY,
    customer_id         VARCHAR(12) NOT NULL REFERENCES customers(customer_id),
    employment_status   VARCHAR(30) NOT NULL CHECK (employment_status IN ('Employed', 'Self-Employed', 'Retired', 'Unemployed', 'Student', 'Part-Time')),
    employer_name       VARCHAR(255),
    job_title           VARCHAR(255),
    industry_sector     VARCHAR(100),
    annual_income       NUMERIC(12, 2) NOT NULL,
    additional_income   NUMERIC(12, 2) DEFAULT 0,
    income_currency     VARCHAR(3) DEFAULT 'GBP',
    employment_start    DATE,
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    verified            BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 4. ACCOUNTS (Current / Savings linked to loan servicing)
-- ============================================================
CREATE TABLE accounts (
    account_id          VARCHAR(20) PRIMARY KEY,
    customer_id         VARCHAR(12) NOT NULL REFERENCES customers(customer_id),
    account_type        VARCHAR(30) NOT NULL CHECK (account_type IN ('Current', 'Savings', 'Loan Servicing', 'Offset')),
    sort_code           VARCHAR(8) NOT NULL,
    account_number      VARCHAR(8) NOT NULL,
    iban                VARCHAR(34),
    balance             NUMERIC(14, 2) NOT NULL DEFAULT 0,
    available_balance   NUMERIC(14, 2) NOT NULL DEFAULT 0,
    currency            VARCHAR(3) DEFAULT 'GBP',
    status              VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Dormant', 'Closed', 'Frozen', 'Suspended')),
    opened_date         DATE NOT NULL,
    closed_date         DATE,
    overdraft_limit     NUMERIC(12, 2) DEFAULT 0,
    interest_rate       NUMERIC(5, 4),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 5. LOAN PRODUCTS (Product catalogue)
-- ============================================================
CREATE TABLE loan_products (
    product_id          VARCHAR(20) PRIMARY KEY,
    product_name        VARCHAR(100) NOT NULL,
    product_category    VARCHAR(30) NOT NULL CHECK (product_category IN ('Mortgage', 'Personal Loan', 'Business Loan', 'Auto Finance', 'Buy-to-Let', 'Bridging Loan', 'Credit Card', 'Overdraft')),
    min_amount          NUMERIC(14, 2) NOT NULL,
    max_amount          NUMERIC(14, 2) NOT NULL,
    min_term_months     INT NOT NULL,
    max_term_months     INT NOT NULL,
    base_rate           NUMERIC(5, 4) NOT NULL,
    rate_type           VARCHAR(20) NOT NULL CHECK (rate_type IN ('Fixed', 'Variable', 'Tracker', 'Discount', 'SVR')),
    arrangement_fee     NUMERIC(10, 2) DEFAULT 0,
    early_repayment_charge NUMERIC(5, 4) DEFAULT 0,
    is_secured          BOOLEAN NOT NULL,
    requires_guarantor  BOOLEAN DEFAULT FALSE,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    launch_date         DATE NOT NULL,
    end_date            DATE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 6. LOAN APPLICATIONS
-- ============================================================
CREATE TABLE loan_applications (
    application_id      VARCHAR(20) PRIMARY KEY,
    customer_id         VARCHAR(12) NOT NULL REFERENCES customers(customer_id),
    product_id          VARCHAR(20) NOT NULL REFERENCES loan_products(product_id),
    application_date    DATE NOT NULL,
    requested_amount    NUMERIC(14, 2) NOT NULL,
    requested_term_months INT NOT NULL,
    purpose             VARCHAR(100),
    application_channel VARCHAR(30) CHECK (application_channel IN ('Online', 'Branch', 'Telephone', 'Broker', 'Mobile App')),
    status              VARCHAR(30) NOT NULL CHECK (status IN ('Submitted', 'Under Review', 'Approved', 'Declined', 'Withdrawn', 'Referred', 'Offered', 'Completed')),
    decision_date       DATE,
    decision_reason     TEXT,
    offered_rate        NUMERIC(5, 4),
    offered_amount      NUMERIC(14, 2),
    offered_term_months INT,
    credit_score_at_application INT,
    debt_to_income_ratio NUMERIC(5, 4),
    loan_to_value       NUMERIC(5, 4),
    affordability_score NUMERIC(5, 2),
    assigned_underwriter VARCHAR(100),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 7. LOANS (Active / Historical)
-- ============================================================
CREATE TABLE loans (
    loan_id             VARCHAR(20) PRIMARY KEY,
    application_id      VARCHAR(20) REFERENCES loan_applications(application_id),
    customer_id         VARCHAR(12) NOT NULL REFERENCES customers(customer_id),
    product_id          VARCHAR(20) NOT NULL REFERENCES loan_products(product_id),
    servicing_account_id VARCHAR(20) REFERENCES accounts(account_id),
    disbursement_date   DATE NOT NULL,
    maturity_date       DATE NOT NULL,
    principal_amount    NUMERIC(14, 2) NOT NULL,
    current_balance     NUMERIC(14, 2) NOT NULL,
    interest_rate       NUMERIC(5, 4) NOT NULL,
    rate_type           VARCHAR(20) NOT NULL CHECK (rate_type IN ('Fixed', 'Variable', 'Tracker', 'Discount', 'SVR')),
    fixed_rate_end_date DATE,
    monthly_payment     NUMERIC(10, 2) NOT NULL,
    term_months         INT NOT NULL,
    remaining_term_months INT NOT NULL,
    loan_status         VARCHAR(20) NOT NULL CHECK (loan_status IN ('Active', 'Closed', 'Default', 'Arrears', 'Written Off', 'Restructured', 'Settled Early')),
    days_past_due       INT DEFAULT 0,
    arrears_amount      NUMERIC(12, 2) DEFAULT 0,
    total_interest_paid NUMERIC(14, 2) DEFAULT 0,
    total_principal_paid NUMERIC(14, 2) DEFAULT 0,
    total_fees_charged  NUMERIC(10, 2) DEFAULT 0,
    next_payment_date   DATE,
    last_payment_date   DATE,
    last_payment_amount NUMERIC(10, 2),
    origination_fee     NUMERIC(10, 2) DEFAULT 0,
    insurance_linked    BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 8. COLLATERAL (For secured loans / mortgages)
-- ============================================================
CREATE TABLE collateral (
    collateral_id       SERIAL PRIMARY KEY,
    loan_id             VARCHAR(20) NOT NULL REFERENCES loans(loan_id),
    collateral_type     VARCHAR(30) NOT NULL CHECK (collateral_type IN ('Residential Property', 'Commercial Property', 'Vehicle', 'Cash Deposit', 'Investment Portfolio', 'Land')),
    description         TEXT,
    address_line_1      VARCHAR(255),
    address_line_2      VARCHAR(255),
    city                VARCHAR(100),
    postcode            VARCHAR(10),
    country             VARCHAR(3) DEFAULT 'GBR',
    estimated_value     NUMERIC(14, 2) NOT NULL,
    valuation_date      DATE NOT NULL,
    valuation_source    VARCHAR(50),
    property_type       VARCHAR(30) CHECK (property_type IN ('Detached', 'Semi-Detached', 'Terraced', 'Flat', 'Bungalow', 'Maisonette', 'New Build', 'Commercial', NULL)),
    bedrooms            INT,
    tenure              VARCHAR(20) CHECK (tenure IN ('Freehold', 'Leasehold', NULL)),
    year_built          INT,
    insurance_policy_ref VARCHAR(50),
    ltv_at_origination  NUMERIC(5, 4),
    current_ltv         NUMERIC(5, 4),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 9. PAYMENT SCHEDULE (Amortisation)
-- ============================================================
CREATE TABLE payment_schedule (
    schedule_id         SERIAL PRIMARY KEY,
    loan_id             VARCHAR(20) NOT NULL REFERENCES loans(loan_id),
    payment_number      INT NOT NULL,
    due_date            DATE NOT NULL,
    principal_due       NUMERIC(10, 2) NOT NULL,
    interest_due        NUMERIC(10, 2) NOT NULL,
    total_due           NUMERIC(10, 2) NOT NULL,
    outstanding_balance NUMERIC(14, 2) NOT NULL,
    status              VARCHAR(20) DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Paid', 'Partial', 'Missed', 'Late')),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 10. PAYMENTS (Actual payment transactions)
-- ============================================================
CREATE TABLE payments (
    payment_id          VARCHAR(20) PRIMARY KEY,
    loan_id             VARCHAR(20) NOT NULL REFERENCES loans(loan_id),
    schedule_id         INT REFERENCES payment_schedule(schedule_id),
    payment_date        DATE NOT NULL,
    amount              NUMERIC(10, 2) NOT NULL,
    principal_portion   NUMERIC(10, 2),
    interest_portion    NUMERIC(10, 2),
    fees_portion        NUMERIC(10, 2) DEFAULT 0,
    payment_method      VARCHAR(30) CHECK (payment_method IN ('Direct Debit', 'Standing Order', 'Bank Transfer', 'Overpayment', 'Lump Sum', 'Card Payment')),
    payment_status      VARCHAR(20) NOT NULL CHECK (payment_status IN ('Completed', 'Pending', 'Failed', 'Reversed', 'Returned')),
    reference           VARCHAR(50),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 11. COLLECTIONS & RECOVERIES
-- ============================================================
CREATE TABLE collections (
    collection_id       SERIAL PRIMARY KEY,
    loan_id             VARCHAR(20) NOT NULL REFERENCES loans(loan_id),
    customer_id         VARCHAR(12) NOT NULL REFERENCES customers(customer_id),
    collection_stage    VARCHAR(30) NOT NULL CHECK (collection_stage IN ('Pre-Arrears', 'Early Arrears', 'Late Arrears', 'Default', 'Litigation', 'Recovery', 'Write Off')),
    arrears_start_date  DATE NOT NULL,
    arrears_amount      NUMERIC(12, 2) NOT NULL,
    days_in_arrears     INT NOT NULL,
    contact_attempts    INT DEFAULT 0,
    last_contact_date   DATE,
    last_contact_method VARCHAR(30) CHECK (last_contact_method IN ('Phone', 'Letter', 'Email', 'SMS', 'Home Visit')),
    arrangement_in_place BOOLEAN DEFAULT FALSE,
    arrangement_amount  NUMERIC(10, 2),
    assigned_agent      VARCHAR(100),
    outcome             VARCHAR(30) CHECK (outcome IN ('Resolved', 'Ongoing', 'Escalated', 'Written Off', 'Sold', NULL)),
    notes               TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 12. CREDIT BUREAU DATA
-- ============================================================
CREATE TABLE credit_bureau_data (
    bureau_id           SERIAL PRIMARY KEY,
    customer_id         VARCHAR(12) NOT NULL REFERENCES customers(customer_id),
    bureau_name         VARCHAR(30) NOT NULL CHECK (bureau_name IN ('Experian', 'Equifax', 'TransUnion')),
    report_date         DATE NOT NULL,
    credit_score        INT NOT NULL,
    score_band          VARCHAR(20) CHECK (score_band IN ('Excellent', 'Good', 'Fair', 'Poor', 'Very Poor')),
    total_accounts      INT,
    active_accounts     INT,
    defaulted_accounts  INT DEFAULT 0,
    total_debt          NUMERIC(14, 2),
    monthly_commitments NUMERIC(12, 2),
    ccjs_count          INT DEFAULT 0,  -- County Court Judgments
    bankruptcies        INT DEFAULT 0,
    iva_count           INT DEFAULT 0,  -- Individual Voluntary Arrangements
    missed_payments_12m INT DEFAULT 0,
    hard_searches_12m   INT DEFAULT 0,
    electoral_roll      BOOLEAN DEFAULT TRUE,
    fraud_alert         BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 13. RISK RATINGS (Internal scoring)
-- ============================================================
CREATE TABLE risk_ratings (
    rating_id           SERIAL PRIMARY KEY,
    loan_id             VARCHAR(20) NOT NULL REFERENCES loans(loan_id),
    rating_date         DATE NOT NULL,
    pd_score            NUMERIC(6, 5) NOT NULL,  -- Probability of Default (0-1)
    lgd_score           NUMERIC(6, 5) NOT NULL,  -- Loss Given Default (0-1)
    ead_amount          NUMERIC(14, 2) NOT NULL,  -- Exposure At Default
    expected_loss       NUMERIC(14, 2) NOT NULL,
    risk_weight         NUMERIC(5, 4),
    internal_rating     VARCHAR(5) NOT NULL CHECK (internal_rating IN ('AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC', 'C', 'D')),
    regulatory_category VARCHAR(30) CHECK (regulatory_category IN ('Performing', 'Underperforming', 'Non-Performing', 'Default')),
    ifrs9_stage         INT CHECK (ifrs9_stage IN (1, 2, 3)),
    provision_amount    NUMERIC(14, 2) DEFAULT 0,
    model_version       VARCHAR(20),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 14. LOAN COVENANTS (For business loans)
-- ============================================================
CREATE TABLE loan_covenants (
    covenant_id         SERIAL PRIMARY KEY,
    loan_id             VARCHAR(20) NOT NULL REFERENCES loans(loan_id),
    covenant_type       VARCHAR(50) NOT NULL CHECK (covenant_type IN ('Debt Service Coverage', 'Loan to Value', 'Interest Coverage', 'Current Ratio', 'Net Worth', 'Revenue Minimum')),
    threshold_value     NUMERIC(10, 4) NOT NULL,
    measurement_frequency VARCHAR(20) CHECK (measurement_frequency IN ('Monthly', 'Quarterly', 'Semi-Annual', 'Annual')),
    last_tested_date    DATE,
    last_tested_value   NUMERIC(10, 4),
    status              VARCHAR(20) DEFAULT 'Compliant' CHECK (status IN ('Compliant', 'Breached', 'Waived', 'Not Yet Tested')),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 15. LOAN PERFORMANCE MONTHLY SNAPSHOT
-- ============================================================
CREATE TABLE loan_performance_monthly (
    snapshot_id         SERIAL PRIMARY KEY,
    loan_id             VARCHAR(20) NOT NULL REFERENCES loans(loan_id),
    snapshot_date       DATE NOT NULL,
    outstanding_balance NUMERIC(14, 2) NOT NULL,
    interest_rate       NUMERIC(5, 4) NOT NULL,
    days_past_due       INT DEFAULT 0,
    arrears_amount      NUMERIC(12, 2) DEFAULT 0,
    payment_received    NUMERIC(10, 2) DEFAULT 0,
    principal_paid      NUMERIC(10, 2) DEFAULT 0,
    interest_paid       NUMERIC(10, 2) DEFAULT 0,
    fees_charged        NUMERIC(10, 2) DEFAULT 0,
    loan_status         VARCHAR(20) NOT NULL,
    ifrs9_stage         INT,
    provision_amount    NUMERIC(14, 2) DEFAULT 0,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (loan_id, snapshot_date)
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_customers_risk ON customers(risk_category);
CREATE INDEX idx_addresses_customer ON customer_addresses(customer_id);
CREATE INDEX idx_employment_customer ON employment_details(customer_id);
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_applications_customer ON loan_applications(customer_id);
CREATE INDEX idx_applications_product ON loan_applications(product_id);
CREATE INDEX idx_applications_status ON loan_applications(status);
CREATE INDEX idx_loans_customer ON loans(customer_id);
CREATE INDEX idx_loans_product ON loans(product_id);
CREATE INDEX idx_loans_status ON loans(loan_status);
CREATE INDEX idx_loans_disbursement ON loans(disbursement_date);
CREATE INDEX idx_collateral_loan ON collateral(loan_id);
CREATE INDEX idx_schedule_loan ON payment_schedule(loan_id);
CREATE INDEX idx_payments_loan ON payments(loan_id);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_collections_loan ON collections(loan_id);
CREATE INDEX idx_collections_stage ON collections(collection_stage);
CREATE INDEX idx_bureau_customer ON credit_bureau_data(customer_id);
CREATE INDEX idx_risk_loan ON risk_ratings(loan_id);
CREATE INDEX idx_performance_loan_date ON loan_performance_monthly(loan_id, snapshot_date);
