-- ============================================================
-- Load CSV data into Barclays Loan Database
-- ============================================================

-- 1. Loan Products
\copy loan_products(product_id, product_name, product_category, min_amount, max_amount, min_term_months, max_term_months, base_rate, rate_type, arrangement_fee, early_repayment_charge, is_secured, is_active, launch_date, end_date) FROM '__DATA_DIR__/loan_products.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 2. Customers
\copy customers(customer_id, title, first_name, last_name, date_of_birth, gender, email, phone_primary, phone_secondary, national_insurance, customer_segment, customer_since, kyc_status, risk_category, is_politically_exposed, marketing_consent) FROM '__DATA_DIR__/customers.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 3. Customer Addresses
\copy customer_addresses(address_id, customer_id, address_type, address_line_1, address_line_2, city, county, postcode, country, is_current, resident_since) FROM '__DATA_DIR__/customer_addresses.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 4. Employment Details
\copy employment_details(employment_id, customer_id, employment_status, employer_name, job_title, industry_sector, annual_income, additional_income, income_currency, employment_start, is_current, verified) FROM '__DATA_DIR__/employment_details.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 5. Accounts
\copy accounts(account_id, customer_id, account_type, sort_code, account_number, iban, balance, available_balance, currency, status, opened_date, closed_date, overdraft_limit, interest_rate) FROM '__DATA_DIR__/accounts.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 6. Loan Applications
\copy loan_applications(application_id, customer_id, product_id, application_date, requested_amount, requested_term_months, purpose, application_channel, status, decision_date, decision_reason, offered_rate, offered_amount, offered_term_months, credit_score_at_application, debt_to_income_ratio, loan_to_value, affordability_score, assigned_underwriter) FROM '__DATA_DIR__/loan_applications.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 7. Loans
\copy loans(loan_id, application_id, customer_id, product_id, servicing_account_id, disbursement_date, maturity_date, principal_amount, current_balance, interest_rate, rate_type, fixed_rate_end_date, monthly_payment, term_months, remaining_term_months, loan_status, days_past_due, arrears_amount, total_interest_paid, total_principal_paid, total_fees_charged, next_payment_date, last_payment_date, last_payment_amount, origination_fee, insurance_linked) FROM '__DATA_DIR__/loans.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 8. Collateral
\copy collateral(collateral_id, loan_id, collateral_type, description, address_line_1, address_line_2, city, postcode, country, estimated_value, valuation_date, valuation_source, property_type, bedrooms, tenure, year_built, insurance_policy_ref, ltv_at_origination, current_ltv) FROM '__DATA_DIR__/collateral.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 9. Payment Schedule
\copy payment_schedule(schedule_id, loan_id, payment_number, due_date, principal_due, interest_due, total_due, outstanding_balance, status) FROM '__DATA_DIR__/payment_schedule.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 10. Payments
\copy payments(payment_id, loan_id, schedule_id, payment_date, amount, principal_portion, interest_portion, fees_portion, payment_method, payment_status, reference) FROM '__DATA_DIR__/payments.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 11. Collections
\copy collections(collection_id, loan_id, customer_id, collection_stage, arrears_start_date, arrears_amount, days_in_arrears, contact_attempts, last_contact_date, last_contact_method, arrangement_in_place, arrangement_amount, assigned_agent, outcome, notes) FROM '__DATA_DIR__/collections.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 12. Credit Bureau Data
\copy credit_bureau_data(bureau_id, customer_id, bureau_name, report_date, credit_score, score_band, total_accounts, active_accounts, defaulted_accounts, total_debt, monthly_commitments, ccjs_count, bankruptcies, iva_count, missed_payments_12m, hard_searches_12m, electoral_roll, fraud_alert) FROM '__DATA_DIR__/credit_bureau_data.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 13. Risk Ratings
\copy risk_ratings(rating_id, loan_id, rating_date, pd_score, lgd_score, ead_amount, expected_loss, risk_weight, internal_rating, regulatory_category, ifrs9_stage, provision_amount, model_version) FROM '__DATA_DIR__/risk_ratings.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 14. Loan Performance Monthly
\copy loan_performance_monthly(snapshot_id, loan_id, snapshot_date, outstanding_balance, interest_rate, days_past_due, arrears_amount, payment_received, principal_paid, interest_paid, fees_charged, loan_status, ifrs9_stage, provision_amount) FROM '__DATA_DIR__/loan_performance_monthly.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- 15. Loan Covenants
\copy loan_covenants(covenant_id, loan_id, covenant_type, threshold_value, measurement_frequency, last_tested_date, last_tested_value, status) FROM '__DATA_DIR__/loan_covenants.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- Reset sequences
SELECT setval('customer_addresses_address_id_seq', (SELECT MAX(address_id) FROM customer_addresses));
SELECT setval('employment_details_employment_id_seq', (SELECT MAX(employment_id) FROM employment_details));
SELECT setval('collateral_collateral_id_seq', (SELECT MAX(collateral_id) FROM collateral));
SELECT setval('payment_schedule_schedule_id_seq', (SELECT MAX(schedule_id) FROM payment_schedule));
SELECT setval('collections_collection_id_seq', (SELECT MAX(collection_id) FROM collections));
SELECT setval('credit_bureau_data_bureau_id_seq', (SELECT MAX(bureau_id) FROM credit_bureau_data));
SELECT setval('risk_ratings_rating_id_seq', (SELECT MAX(rating_id) FROM risk_ratings));
SELECT setval('loan_performance_monthly_snapshot_id_seq', (SELECT MAX(snapshot_id) FROM loan_performance_monthly));
SELECT setval('loan_covenants_covenant_id_seq', (SELECT MAX(covenant_id) FROM loan_covenants));
