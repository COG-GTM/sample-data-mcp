"""
Synthetic Loan Data Generator for Barclays UK Demo
Generates realistic UK banking data for loan portfolios.
"""

import random
import string
import csv
import os
from datetime import date, timedelta, datetime
from decimal import Decimal, ROUND_HALF_UP

# ============================================================
# Configuration
# ============================================================
NUM_CUSTOMERS = 5000
NUM_LOAN_APPLICATIONS = 8000
NUM_LOANS = 6000
SEED = 42
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "data")

random.seed(SEED)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Reference Data
# ============================================================

UK_FIRST_NAMES_MALE = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard",
    "Joseph", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony",
    "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth",
    "Oliver", "Harry", "George", "Jack", "Charlie", "Noah", "Leo",
    "Arthur", "Muhammad", "Oscar", "Henry", "Alexander", "Edward",
    "Samuel", "Sebastian", "Freddie", "Archie", "Ethan", "Isaac", "Theo",
]

UK_FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth",
    "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty",
    "Margaret", "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily",
    "Olivia", "Amelia", "Isla", "Ava", "Mia", "Isabella", "Sophia",
    "Grace", "Lily", "Freya", "Ella", "Charlotte", "Florence",
    "Rosie", "Poppy", "Willow", "Daisy", "Evie", "Sienna", "Phoebe",
]

UK_LAST_NAMES = [
    "Smith", "Jones", "Williams", "Taylor", "Brown", "Davies", "Evans",
    "Wilson", "Thomas", "Roberts", "Johnson", "Lewis", "Walker", "Robinson",
    "Wood", "Thompson", "White", "Watson", "Jackson", "Wright", "Green",
    "Harris", "Cooper", "King", "Lee", "Martin", "Clarke", "James",
    "Morgan", "Hughes", "Edwards", "Hill", "Moore", "Clark", "Harrison",
    "Scott", "Young", "Morris", "Hall", "Ward", "Turner", "Carter",
    "Phillips", "Mitchell", "Patel", "Adams", "Campbell", "Anderson",
    "Allen", "Cook", "Bailey", "Palmer", "Stevens", "Bell", "Khan",
    "Singh", "Ali", "Ahmed", "Hussain", "Shah", "Begum", "Rahman",
    "Murphy", "O'Brien", "Kelly", "McCarthy", "Sullivan", "Byrne",
]

UK_CITIES = [
    ("London", "Greater London", ["E1", "E2", "EC1", "EC2", "N1", "NW1", "SE1", "SW1", "W1", "WC1"]),
    ("Manchester", "Greater Manchester", ["M1", "M2", "M3", "M4", "M14", "M20", "M21"]),
    ("Birmingham", "West Midlands", ["B1", "B2", "B3", "B4", "B5", "B15", "B16"]),
    ("Leeds", "West Yorkshire", ["LS1", "LS2", "LS3", "LS6", "LS7", "LS8"]),
    ("Glasgow", "Scotland", ["G1", "G2", "G3", "G4", "G11", "G12"]),
    ("Liverpool", "Merseyside", ["L1", "L2", "L3", "L4", "L8", "L15"]),
    ("Bristol", "Bristol", ["BS1", "BS2", "BS3", "BS4", "BS5", "BS6"]),
    ("Sheffield", "South Yorkshire", ["S1", "S2", "S3", "S5", "S10", "S11"]),
    ("Edinburgh", "Scotland", ["EH1", "EH2", "EH3", "EH4", "EH7", "EH8"]),
    ("Cardiff", "Wales", ["CF1", "CF10", "CF11", "CF14", "CF24"]),
    ("Newcastle", "Tyne and Wear", ["NE1", "NE2", "NE3", "NE4", "NE6"]),
    ("Nottingham", "Nottinghamshire", ["NG1", "NG2", "NG3", "NG5", "NG7"]),
    ("Southampton", "Hampshire", ["SO14", "SO15", "SO16", "SO17"]),
    ("Oxford", "Oxfordshire", ["OX1", "OX2", "OX3", "OX4"]),
    ("Cambridge", "Cambridgeshire", ["CB1", "CB2", "CB3", "CB4"]),
    ("Brighton", "East Sussex", ["BN1", "BN2", "BN3"]),
    ("Bath", "Somerset", ["BA1", "BA2"]),
    ("York", "North Yorkshire", ["YO1", "YO10", "YO23", "YO31"]),
    ("Reading", "Berkshire", ["RG1", "RG2", "RG4", "RG6"]),
    ("Coventry", "West Midlands", ["CV1", "CV2", "CV3", "CV4"]),
]

UK_STREET_NAMES = [
    "High Street", "Station Road", "Church Lane", "Park Avenue", "Victoria Road",
    "Queen Street", "King Street", "New Road", "The Crescent", "Manor Way",
    "Green Lane", "Mill Lane", "School Lane", "The Grove", "Springfield Road",
    "Church Street", "London Road", "Main Street", "George Street", "Albert Road",
    "Bridge Street", "Castle Street", "Market Street", "Broad Street", "North Road",
    "South Street", "West Road", "East Street", "Meadow Lane", "Oak Drive",
    "Elm Close", "Beech Avenue", "Cedar Way", "Willow Court", "Birch Lane",
]

INDUSTRY_SECTORS = [
    "Financial Services", "Technology", "Healthcare", "Education", "Manufacturing",
    "Retail", "Construction", "Legal Services", "Public Sector", "Energy",
    "Media & Entertainment", "Transport", "Hospitality", "Real Estate",
    "Pharmaceuticals", "Telecommunications", "Agriculture", "Professional Services",
    "Charity & Non-Profit", "Defence",
]

EMPLOYER_NAMES = [
    "Barclays PLC", "HSBC Holdings", "Lloyds Banking Group", "NatWest Group",
    "Tesco PLC", "Unilever", "GlaxoSmithKline", "AstraZeneca", "BP PLC",
    "Shell PLC", "Vodafone Group", "BT Group", "BAE Systems", "Rolls-Royce",
    "National Health Service", "HM Revenue & Customs", "Ministry of Defence",
    "BBC", "Deloitte LLP", "PricewaterhouseCoopers", "Ernst & Young", "KPMG",
    "Accenture", "Capgemini", "IBM UK", "Microsoft UK", "Amazon UK",
    "Google UK", "Facebook UK", "Goldman Sachs International",
    "JPMorgan Chase", "Morgan Stanley", "Sainsbury's", "Marks & Spencer",
    "John Lewis Partnership", "Royal Mail", "Network Rail", "Heathrow Airport",
    "British Airways", "EasyJet", "ARM Holdings", "Dyson Ltd",
]

JOB_TITLES = [
    "Software Engineer", "Accountant", "Teacher", "Nurse", "Doctor",
    "Solicitor", "Barrister", "Architect", "Civil Servant", "Police Officer",
    "Project Manager", "Marketing Manager", "Sales Director", "Financial Analyst",
    "Data Scientist", "Operations Manager", "HR Director", "Chief Executive",
    "Consultant", "Pharmacist", "Dentist", "Veterinarian", "Plumber",
    "Electrician", "Carpenter", "Chef", "Journalist", "Graphic Designer",
    "Mechanical Engineer", "Quantity Surveyor", "Estate Agent", "Investment Banker",
    "Actuary", "Pilot", "Physiotherapist", "Social Worker", "Lecturer",
]

LOAN_PURPOSES_PERSONAL = [
    "Home Improvement", "Debt Consolidation", "Car Purchase", "Wedding",
    "Holiday", "Medical Expenses", "Education", "Moving Costs",
    "Furniture & Appliances", "Emergency Fund",
]

LOAN_PURPOSES_MORTGAGE = [
    "First Time Purchase", "Home Mover", "Remortgage", "Buy-to-Let Purchase",
    "BTL Remortgage", "Second Home", "Self Build", "Equity Release",
]

LOAN_PURPOSES_BUSINESS = [
    "Working Capital", "Equipment Purchase", "Expansion", "Property Acquisition",
    "Stock Finance", "Refurbishment", "Vehicle Fleet", "Technology Investment",
    "Acquisition Finance", "Research & Development",
]


# ============================================================
# Helper Functions
# ============================================================

def generate_customer_id():
    """Generate a Barclays-style customer ID: alphanumeric, 10 chars."""
    return "BC" + ''.join(random.choices(string.digits, k=8))


def generate_ni_number():
    """Generate a UK National Insurance number format."""
    prefix = random.choice(["AB", "CD", "EF", "GH", "JK", "LM", "NP", "RS", "TW"])
    digits = ''.join(random.choices(string.digits, k=6))
    suffix = random.choice(["A", "B", "C", "D"])
    return f"{prefix}{digits}{suffix}"


def generate_sort_code():
    """Generate a UK sort code."""
    return f"{random.randint(10,99):02d}-{random.randint(10,99):02d}-{random.randint(10,99):02d}"


def generate_account_number():
    """Generate an 8-digit UK account number."""
    return ''.join(random.choices(string.digits, k=8))


def generate_postcode(base):
    """Generate a UK postcode from a base prefix."""
    number = random.randint(1, 9)
    suffix = f"{random.randint(0,9)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"
    return f"{base} {number}{suffix}"


def random_date(start, end):
    """Generate a random date between start and end."""
    delta = (end - start).days
    if delta <= 0:
        return start
    return start + timedelta(days=random.randint(0, delta))


def generate_email(first, last):
    """Generate a realistic email address."""
    domains = ["gmail.com", "yahoo.co.uk", "outlook.com", "hotmail.co.uk",
               "btinternet.com", "sky.com", "icloud.com", "protonmail.com",
               "mail.com", "aol.com"]
    sep = random.choice([".", "_", ""])
    num = random.choice(["", str(random.randint(1, 99))])
    return f"{first.lower()}{sep}{last.lower()}{num}@{random.choice(domains)}"


def generate_phone():
    """Generate a UK phone number."""
    prefix = random.choice(["07", "+447"])
    return prefix + ''.join(random.choices(string.digits, k=9))


def round_decimal(value, places=2):
    """Round a float to specified decimal places."""
    return float(Decimal(str(value)).quantize(Decimal(10) ** -places, rounding=ROUND_HALF_UP))


def write_csv(filename, rows, headers):
    """Write rows to a CSV file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"  Written {len(rows)} rows to {filename}")


# ============================================================
# Data Generation
# ============================================================

print("=" * 60)
print("Barclays UK Synthetic Loan Data Generator")
print("=" * 60)

# ------ LOAN PRODUCTS ------
print("\n[1/12] Generating loan products...")
loan_products = []
product_defs = [
    ("PROD-MTG-FIX2", "2-Year Fixed Rate Mortgage", "Mortgage", 50000, 2000000, 24, 300, 0.0425, "Fixed", 999, 0.02, True),
    ("PROD-MTG-FIX5", "5-Year Fixed Rate Mortgage", "Mortgage", 50000, 2000000, 60, 300, 0.0395, "Fixed", 999, 0.03, True),
    ("PROD-MTG-TRACK", "Base Rate Tracker Mortgage", "Mortgage", 50000, 1500000, 24, 300, 0.0475, "Tracker", 0, 0.01, True),
    ("PROD-MTG-SVR", "Standard Variable Rate Mortgage", "Mortgage", 50000, 1500000, 12, 300, 0.0625, "SVR", 0, 0, True),
    ("PROD-MTG-BTL2", "Buy-to-Let 2-Year Fixed", "Buy-to-Let", 75000, 2500000, 24, 300, 0.0525, "Fixed", 1495, 0.03, True),
    ("PROD-MTG-BTL5", "Buy-to-Let 5-Year Fixed", "Buy-to-Let", 75000, 2500000, 60, 300, 0.0495, "Fixed", 1495, 0.04, True),
    ("PROD-PL-STAND", "Personal Loan Standard", "Personal Loan", 1000, 25000, 12, 84, 0.069, "Fixed", 0, 0, False),
    ("PROD-PL-PREM", "Personal Loan Premium", "Personal Loan", 7500, 50000, 12, 84, 0.039, "Fixed", 0, 0, False),
    ("PROD-PL-HOME", "Home Improvement Loan", "Personal Loan", 5000, 50000, 12, 120, 0.049, "Fixed", 0, 0, False),
    ("PROD-AUTO-NEW", "New Car Finance", "Auto Finance", 5000, 75000, 12, 60, 0.059, "Fixed", 150, 0.01, True),
    ("PROD-AUTO-USED", "Used Car Finance", "Auto Finance", 3000, 40000, 12, 60, 0.079, "Fixed", 150, 0.01, True),
    ("PROD-BL-SMALL", "Small Business Loan", "Business Loan", 5000, 100000, 12, 60, 0.075, "Fixed", 500, 0.02, False),
    ("PROD-BL-MED", "Medium Business Loan", "Business Loan", 100000, 500000, 12, 120, 0.055, "Variable", 1000, 0.02, True),
    ("PROD-BL-LARGE", "Large Business Loan", "Business Loan", 500000, 5000000, 24, 180, 0.045, "Variable", 2500, 0.03, True),
    ("PROD-BRIDGE", "Bridging Loan", "Bridging Loan", 25000, 5000000, 1, 18, 0.085, "Variable", 1500, 0, True),
]

for p in product_defs:
    loan_products.append(list(p) + [True, "2018-01-15", None])

write_csv("loan_products.csv", loan_products,
    ["product_id", "product_name", "product_category", "min_amount", "max_amount",
     "min_term_months", "max_term_months", "base_rate", "rate_type",
     "arrangement_fee", "early_repayment_charge", "is_secured",
     "is_active", "launch_date", "end_date"])

# Build product lookup
product_lookup = {}
for p in product_defs:
    product_lookup[p[0]] = {
        "category": p[2], "min_amt": p[3], "max_amt": p[4],
        "min_term": p[5], "max_term": p[6], "base_rate": p[7],
        "rate_type": p[8], "fee": p[9], "erc": p[10], "secured": p[11],
    }

# ------ CUSTOMERS ------
print("[2/12] Generating customers...")
customers = []
customer_ids = []
customer_data = {}

segment_weights = {"Basic": 0.30, "Standard": 0.40, "Premium": 0.20, "Private": 0.10}
segments = list(segment_weights.keys())
seg_weights = list(segment_weights.values())

income_ranges = {
    "Basic": (18000, 35000),
    "Standard": (30000, 65000),
    "Premium": (55000, 120000),
    "Private": (100000, 500000),
}

for i in range(NUM_CUSTOMERS):
    cid = generate_customer_id()
    while cid in [c[0] for c in customers]:
        cid = generate_customer_id()
    customer_ids.append(cid)

    gender = random.choice(["Male", "Female"])
    if gender == "Male":
        first = random.choice(UK_FIRST_NAMES_MALE)
        title = random.choice(["Mr", "Dr"])
    else:
        first = random.choice(UK_FIRST_NAMES_FEMALE)
        title = random.choice(["Mrs", "Ms", "Miss", "Dr"])

    last = random.choice(UK_LAST_NAMES)
    dob = random_date(date(1950, 1, 1), date(2000, 12, 31))
    segment = random.choices(segments, weights=seg_weights, k=1)[0]
    customer_since = random_date(date(2005, 1, 1), date(2024, 6, 30))

    risk_cat_weights = {
        "Basic": [0.1, 0.3, 0.3, 0.2, 0.1],
        "Standard": [0.2, 0.4, 0.25, 0.1, 0.05],
        "Premium": [0.35, 0.4, 0.15, 0.08, 0.02],
        "Private": [0.5, 0.35, 0.1, 0.04, 0.01],
    }
    risk_cat = random.choices(
        ["Low", "Standard", "Medium", "High", "Very High"],
        weights=risk_cat_weights[segment], k=1
    )[0]

    kyc_status = random.choices(
        ["Verified", "Pending", "Failed", "Expired"],
        weights=[0.90, 0.05, 0.02, 0.03], k=1
    )[0]

    pep = random.random() < 0.005
    marketing = random.random() < 0.7

    customers.append([
        cid, title, first, last, dob.isoformat(), gender,
        generate_email(first, last), generate_phone(),
        generate_phone() if random.random() < 0.3 else "",
        generate_ni_number(), segment, customer_since.isoformat(),
        kyc_status, risk_cat, pep, marketing,
    ])

    customer_data[cid] = {
        "segment": segment, "risk": risk_cat, "dob": dob,
        "since": customer_since, "first": first, "last": last,
    }

write_csv("customers.csv", customers,
    ["customer_id", "title", "first_name", "last_name", "date_of_birth",
     "gender", "email", "phone_primary", "phone_secondary",
     "national_insurance", "customer_segment", "customer_since",
     "kyc_status", "risk_category", "is_politically_exposed", "marketing_consent"])

# ------ ADDRESSES ------
print("[3/12] Generating customer addresses...")
addresses = []
addr_id = 1
for cid in customer_ids:
    city, county, postcodes = random.choice(UK_CITIES)
    street_num = random.randint(1, 200)
    street = random.choice(UK_STREET_NAMES)
    pc = generate_postcode(random.choice(postcodes))
    resident_since = random_date(
        max(customer_data[cid]["since"] - timedelta(days=3650), date(2000, 1, 1)),
        customer_data[cid]["since"]
    )

    addresses.append([
        addr_id, cid, "Residential", f"{street_num} {street}", "",
        city, county, pc, "GBR", True, resident_since.isoformat(),
    ])
    addr_id += 1

    # ~30% have a previous address
    if random.random() < 0.3:
        prev_city, prev_county, prev_postcodes = random.choice(UK_CITIES)
        addresses.append([
            addr_id, cid, "Previous",
            f"{random.randint(1,200)} {random.choice(UK_STREET_NAMES)}", "",
            prev_city, prev_county,
            generate_postcode(random.choice(prev_postcodes)), "GBR", False,
            random_date(date(1990, 1, 1), resident_since).isoformat(),
        ])
        addr_id += 1

write_csv("customer_addresses.csv", addresses,
    ["address_id", "customer_id", "address_type", "address_line_1",
     "address_line_2", "city", "county", "postcode", "country",
     "is_current", "resident_since"])

# ------ EMPLOYMENT ------
print("[4/12] Generating employment details...")
employment = []
emp_id = 1
for cid in customer_ids:
    seg = customer_data[cid]["segment"]
    lo, hi = income_ranges[seg]
    income = round_decimal(random.uniform(lo, hi))
    additional = round_decimal(random.uniform(0, income * 0.2)) if random.random() < 0.25 else 0

    status_weights = [0.65, 0.12, 0.08, 0.05, 0.02, 0.08]
    emp_status = random.choices(
        ["Employed", "Self-Employed", "Retired", "Unemployed", "Student", "Part-Time"],
        weights=status_weights, k=1
    )[0]

    employer = random.choice(EMPLOYER_NAMES) if emp_status == "Employed" else (
        "Self" if emp_status == "Self-Employed" else ""
    )
    job = random.choice(JOB_TITLES) if emp_status in ("Employed", "Self-Employed", "Part-Time") else ""
    industry = random.choice(INDUSTRY_SECTORS) if employer else ""
    emp_start = random_date(date(2005, 1, 1), date(2024, 1, 1)) if emp_status != "Unemployed" else None

    employment.append([
        emp_id, cid, emp_status, employer, job, industry,
        income, additional, "GBP",
        emp_start.isoformat() if emp_start else "",
        True, random.random() < 0.85,
    ])
    emp_id += 1
    customer_data[cid]["income"] = income

write_csv("employment_details.csv", employment,
    ["employment_id", "customer_id", "employment_status", "employer_name",
     "job_title", "industry_sector", "annual_income", "additional_income",
     "income_currency", "employment_start", "is_current", "verified"])

# ------ ACCOUNTS ------
print("[5/12] Generating accounts...")
accounts = []
account_ids_by_customer = {}
acct_counter = 1

for cid in customer_ids:
    # Each customer gets 1-3 accounts
    num_accounts = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2], k=1)[0]
    cust_accounts = []
    seg = customer_data[cid]["segment"]

    for j in range(num_accounts):
        if j == 0:
            acct_type = "Current"
        elif j == 1:
            acct_type = random.choice(["Savings", "Loan Servicing"])
        else:
            acct_type = "Loan Servicing"

        acct_id = f"ACC-{acct_counter:07d}"
        acct_counter += 1
        sort_code = generate_sort_code()
        acct_num = generate_account_number()

        balance_ranges = {
            "Basic": (100, 5000),
            "Standard": (1000, 25000),
            "Premium": (5000, 100000),
            "Private": (25000, 500000),
        }
        lo, hi = balance_ranges[seg]
        balance = round_decimal(random.uniform(lo, hi))
        available = round_decimal(balance * random.uniform(0.85, 1.0))

        status = random.choices(
            ["Active", "Dormant", "Closed"],
            weights=[0.88, 0.07, 0.05], k=1
        )[0]
        opened = random_date(customer_data[cid]["since"], date(2024, 6, 30))
        closed = random_date(opened + timedelta(days=365), date(2025, 12, 31)) if status == "Closed" else None
        overdraft = round_decimal(random.choice([0, 250, 500, 1000, 1500, 2000, 3000])) if acct_type == "Current" else 0
        interest = round_decimal(random.uniform(0.001, 0.045), 4) if acct_type == "Savings" else 0

        accounts.append([
            acct_id, cid, acct_type, sort_code, acct_num, "",
            balance, available, "GBP", status, opened.isoformat(),
            closed.isoformat() if closed else "", overdraft, interest,
        ])
        cust_accounts.append(acct_id)

    account_ids_by_customer[cid] = cust_accounts

write_csv("accounts.csv", accounts,
    ["account_id", "customer_id", "account_type", "sort_code", "account_number",
     "iban", "balance", "available_balance", "currency", "status",
     "opened_date", "closed_date", "overdraft_limit", "interest_rate"])

# ------ LOAN APPLICATIONS ------
print("[6/12] Generating loan applications...")
applications = []
app_counter = 1
approved_apps = []

product_ids = list(product_lookup.keys())
# Weighted product selection (mortgages most common)
product_weights = [15, 15, 8, 5, 8, 5, 12, 8, 5, 5, 4, 4, 3, 2, 1]

for i in range(NUM_LOAN_APPLICATIONS):
    cid = random.choice(customer_ids)
    seg = customer_data[cid]["segment"]
    income = customer_data[cid].get("income", 40000)

    prod_id = random.choices(product_ids, weights=product_weights, k=1)[0]
    prod = product_lookup[prod_id]

    # Realistic amount based on product and income
    if prod["category"] == "Mortgage":
        amount = round_decimal(random.uniform(
            max(prod["min_amt"], income * 2),
            min(prod["max_amt"], income * 5.5)
        ))
    elif prod["category"] == "Buy-to-Let":
        amount = round_decimal(random.uniform(
            max(prod["min_amt"], 100000),
            min(prod["max_amt"], income * 6)
        ))
    elif prod["category"] == "Business Loan":
        amount = round_decimal(random.uniform(prod["min_amt"], min(prod["max_amt"], income * 3)))
    elif prod["category"] == "Auto Finance":
        amount = round_decimal(random.uniform(prod["min_amt"], min(prod["max_amt"], income * 0.8)))
    else:
        amount = round_decimal(random.uniform(prod["min_amt"], min(prod["max_amt"], income * 0.5)))

    term = random.randint(prod["min_term"], prod["max_term"])
    app_date = random_date(date(2019, 1, 1), date(2025, 9, 30))

    # Application channel
    channel = random.choices(
        ["Online", "Branch", "Telephone", "Broker", "Mobile App"],
        weights=[0.35, 0.15, 0.10, 0.25, 0.15], k=1
    )[0]

    # Credit score
    score_ranges = {
        "Low": (720, 999), "Standard": (620, 800),
        "Medium": (520, 700), "High": (400, 600), "Very High": (300, 500),
    }
    risk = customer_data[cid]["risk"]
    lo_score, hi_score = score_ranges[risk]
    credit_score = random.randint(lo_score, hi_score)

    # DTI ratio
    dti = round_decimal(random.uniform(0.15, 0.55), 4)

    # LTV (for secured)
    ltv = round_decimal(random.uniform(0.50, 0.95), 4) if prod["secured"] else None

    # Affordability
    affordability = round_decimal(random.uniform(40, 95), 2)

    # Decision
    if credit_score >= 700 and dti < 0.40 and affordability > 60:
        status_weights_app = [0, 0, 0.75, 0.05, 0.05, 0.05, 0.05, 0.05]
    elif credit_score >= 550:
        status_weights_app = [0, 0.05, 0.50, 0.20, 0.05, 0.10, 0.05, 0.05]
    else:
        status_weights_app = [0, 0.05, 0.15, 0.50, 0.10, 0.10, 0.05, 0.05]

    statuses = ["Submitted", "Under Review", "Approved", "Declined",
                "Withdrawn", "Referred", "Offered", "Completed"]
    app_status = random.choices(statuses, weights=status_weights_app, k=1)[0]

    decision_date = app_date + timedelta(days=random.randint(1, 21)) if app_status not in ("Submitted", "Under Review") else None

    # Purpose
    if prod["category"] in ("Mortgage", "Buy-to-Let"):
        purpose = random.choice(LOAN_PURPOSES_MORTGAGE)
    elif prod["category"] == "Business Loan":
        purpose = random.choice(LOAN_PURPOSES_BUSINESS)
    else:
        purpose = random.choice(LOAN_PURPOSES_PERSONAL)

    offered_rate = round_decimal(prod["base_rate"] + random.uniform(-0.005, 0.02), 4) if app_status in ("Approved", "Offered", "Completed") else None
    offered_amount = amount if app_status in ("Approved", "Offered", "Completed") else None
    offered_term = term if app_status in ("Approved", "Offered", "Completed") else None

    app_id = f"APP-{app_counter:07d}"
    app_counter += 1

    underwriter = f"UW-{random.randint(100,999)}" if app_status not in ("Submitted",) else ""

    decision_reason = ""
    if app_status == "Declined":
        decision_reason = random.choice([
            "Credit score below minimum threshold",
            "Debt-to-income ratio exceeds policy limit",
            "Insufficient employment history",
            "Affordability assessment failed",
            "Adverse credit history detected",
            "LTV exceeds maximum for product",
        ])

    applications.append([
        app_id, cid, prod_id, app_date.isoformat(), amount, term, purpose,
        channel, app_status,
        decision_date.isoformat() if decision_date else "",
        decision_reason,
        offered_rate if offered_rate else "",
        offered_amount if offered_amount else "",
        offered_term if offered_term else "",
        credit_score, dti, ltv if ltv else "", affordability,
        underwriter,
    ])

    if app_status in ("Approved", "Offered", "Completed"):
        approved_apps.append({
            "app_id": app_id, "cid": cid, "prod_id": prod_id,
            "amount": offered_amount or amount, "term": offered_term or term,
            "rate": offered_rate or prod["base_rate"], "app_date": app_date,
            "credit_score": credit_score, "ltv": ltv,
        })

write_csv("loan_applications.csv", applications,
    ["application_id", "customer_id", "product_id", "application_date",
     "requested_amount", "requested_term_months", "purpose",
     "application_channel", "status", "decision_date", "decision_reason",
     "offered_rate", "offered_amount", "offered_term_months",
     "credit_score_at_application", "debt_to_income_ratio",
     "loan_to_value", "affordability_score", "assigned_underwriter"])

# ------ LOANS ------
print("[7/12] Generating loans...")
loans = []
loan_ids = []
loan_data = {}
loan_counter = 1

# Use approved applications to create loans (up to NUM_LOANS)
random.shuffle(approved_apps)
apps_for_loans = approved_apps[:NUM_LOANS]

for app in apps_for_loans:
    loan_id = f"LN-{loan_counter:07d}"
    loan_counter += 1
    loan_ids.append(loan_id)

    cid = app["cid"]
    prod_id = app["prod_id"]
    prod = product_lookup[prod_id]
    amount = app["amount"]
    term = app["term"]
    rate = app["rate"]

    disbursement = app["app_date"] + timedelta(days=random.randint(7, 45))
    maturity = disbursement + timedelta(days=term * 30)

    # Monthly payment (simplified amortisation)
    monthly_rate = rate / 12
    if monthly_rate > 0:
        monthly_payment = round_decimal(
            amount * (monthly_rate * (1 + monthly_rate) ** term) /
            ((1 + monthly_rate) ** term - 1)
        )
    else:
        monthly_payment = round_decimal(amount / term)

    # Time elapsed
    months_elapsed = max(0, (date(2025, 10, 1) - disbursement).days // 30)
    remaining = max(0, term - months_elapsed)

    # Balance calculation (simplified)
    if months_elapsed > 0 and months_elapsed < term:
        balance_factor = ((1 + monthly_rate) ** term - (1 + monthly_rate) ** months_elapsed) / \
                         ((1 + monthly_rate) ** term - 1) if monthly_rate > 0 else (term - months_elapsed) / term
        current_balance = round_decimal(amount * balance_factor)
    elif months_elapsed >= term:
        current_balance = 0
    else:
        current_balance = amount

    total_principal_paid = round_decimal(amount - current_balance)
    total_interest_paid = round_decimal(monthly_payment * min(months_elapsed, term) - total_principal_paid)

    # Status
    if current_balance <= 0:
        loan_status = random.choices(["Closed", "Settled Early"], weights=[0.8, 0.2], k=1)[0]
        current_balance = 0
        remaining = 0
    else:
        status_weights_loan = {
            "Low": [0.92, 0.03, 0.005, 0.02, 0.005, 0.01, 0.01],
            "Standard": [0.85, 0.05, 0.01, 0.05, 0.01, 0.02, 0.01],
            "Medium": [0.75, 0.08, 0.03, 0.08, 0.02, 0.03, 0.01],
            "High": [0.60, 0.12, 0.06, 0.12, 0.04, 0.04, 0.02],
            "Very High": [0.45, 0.15, 0.10, 0.15, 0.06, 0.06, 0.03],
        }
        risk = customer_data[cid]["risk"]
        loan_status = random.choices(
            ["Active", "Arrears", "Default", "Arrears", "Written Off", "Restructured", "Settled Early"],
            weights=status_weights_loan[risk], k=1
        )[0]

    days_past_due = 0
    arrears_amount = 0
    if loan_status == "Arrears":
        days_past_due = random.randint(1, 89)
        arrears_amount = round_decimal(monthly_payment * (days_past_due // 30 + 1))
    elif loan_status == "Default":
        days_past_due = random.randint(90, 365)
        arrears_amount = round_decimal(monthly_payment * (days_past_due // 30 + 1))
    elif loan_status == "Written Off":
        days_past_due = random.randint(180, 720)
        arrears_amount = round_decimal(current_balance * random.uniform(0.3, 1.0))

    servicing_acct = account_ids_by_customer.get(cid, [None])[0]

    fixed_end = None
    if prod["rate_type"] == "Fixed":
        fixed_period = int(prod_id.split("FIX")[1][0]) if "FIX" in prod_id else 2
        fixed_end = disbursement + timedelta(days=fixed_period * 365)

    next_payment = None
    last_payment = None
    last_payment_amount = None
    if loan_status in ("Active", "Arrears", "Restructured"):
        next_payment = date(2025, 11, 1) + timedelta(days=random.randint(0, 28))
        last_payment = date(2025, 10, 1) + timedelta(days=random.randint(0, 5))
        last_payment_amount = monthly_payment

    loans.append([
        loan_id, app["app_id"], cid, prod_id, servicing_acct or "",
        disbursement.isoformat(), maturity.isoformat(),
        amount, current_balance, rate, prod["rate_type"],
        fixed_end.isoformat() if fixed_end else "",
        monthly_payment, term, remaining, loan_status,
        days_past_due, arrears_amount,
        total_interest_paid, total_principal_paid,
        round_decimal(prod["fee"]),
        next_payment.isoformat() if next_payment else "",
        last_payment.isoformat() if last_payment else "",
        last_payment_amount if last_payment_amount else "",
        prod["fee"], random.random() < 0.15,
    ])

    loan_data[loan_id] = {
        "cid": cid, "prod_id": prod_id, "amount": amount,
        "balance": current_balance, "rate": rate, "term": term,
        "remaining": remaining, "monthly": monthly_payment,
        "status": loan_status, "disbursement": disbursement,
        "maturity": maturity, "dpd": days_past_due,
        "arrears": arrears_amount, "category": prod["category"],
        "secured": prod["secured"], "ltv": app.get("ltv"),
    }

write_csv("loans.csv", loans,
    ["loan_id", "application_id", "customer_id", "product_id",
     "servicing_account_id", "disbursement_date", "maturity_date",
     "principal_amount", "current_balance", "interest_rate", "rate_type",
     "fixed_rate_end_date", "monthly_payment", "term_months",
     "remaining_term_months", "loan_status", "days_past_due",
     "arrears_amount", "total_interest_paid", "total_principal_paid",
     "total_fees_charged", "next_payment_date", "last_payment_date",
     "last_payment_amount", "origination_fee", "insurance_linked"])

# ------ COLLATERAL ------
print("[8/12] Generating collateral...")
collateral = []
coll_id = 1

property_types_weight = {
    "Detached": 0.15, "Semi-Detached": 0.25, "Terraced": 0.25,
    "Flat": 0.20, "Bungalow": 0.05, "Maisonette": 0.05, "New Build": 0.05,
}

for lid in loan_ids:
    ld = loan_data[lid]
    if not ld["secured"]:
        continue

    if ld["category"] in ("Mortgage", "Buy-to-Let", "Bridging Loan"):
        coll_type = "Residential Property" if ld["category"] != "Buy-to-Let" else random.choice(["Residential Property", "Commercial Property"])
        city, county, postcodes = random.choice(UK_CITIES)
        prop_type = random.choices(
            list(property_types_weight.keys()),
            weights=list(property_types_weight.values()), k=1
        )[0]
        value = round_decimal(ld["amount"] / (ld["ltv"] if ld["ltv"] and ld["ltv"] > 0 else 0.75))
        current_value = round_decimal(value * random.uniform(0.95, 1.15))
        current_ltv = round_decimal(ld["balance"] / current_value, 4) if current_value > 0 else 0

        bedrooms = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.25, 0.35, 0.2, 0.1], k=1)[0]
        tenure = random.choice(["Freehold", "Leasehold"])
        year_built = random.randint(1850, 2024)

        collateral.append([
            coll_id, lid, coll_type, f"{prop_type} property in {city}",
            f"{random.randint(1,200)} {random.choice(UK_STREET_NAMES)}", "",
            city, generate_postcode(random.choice(postcodes)), "GBR",
            value, ld["disbursement"].isoformat(), "RICS Surveyor",
            prop_type, bedrooms, tenure, year_built,
            f"INS-{random.randint(100000,999999)}" if random.random() < 0.85 else "",
            ld["ltv"] if ld["ltv"] else "", current_ltv,
        ])
        coll_id += 1

    elif ld["category"] == "Auto Finance":
        value = round_decimal(ld["amount"] * random.uniform(1.0, 1.2))
        depreciated = round_decimal(value * random.uniform(0.5, 0.9))
        collateral.append([
            coll_id, lid, "Vehicle",
            f"{random.choice(['BMW', 'Audi', 'Mercedes', 'VW', 'Ford', 'Toyota', 'Jaguar', 'Range Rover', 'Tesla', 'Volvo'])} "
            f"{random.choice(['3 Series', 'A4', 'C-Class', 'Golf', 'Focus', 'Corolla', 'XE', 'Evoque', 'Model 3', 'XC60'])}",
            "", "", "", "", "GBR",
            value, ld["disbursement"].isoformat(), "Glass Guide",
            "", "", "", random.randint(2018, 2025),
            f"INS-{random.randint(100000,999999)}" if random.random() < 0.9 else "",
            "", "",
        ])
        coll_id += 1

    elif ld["category"] == "Business Loan" and ld["secured"]:
        city, county, postcodes = random.choice(UK_CITIES)
        value = round_decimal(ld["amount"] * random.uniform(1.1, 1.5))
        collateral.append([
            coll_id, lid, "Commercial Property",
            f"Commercial premises in {city}",
            f"{random.randint(1,50)} {random.choice(UK_STREET_NAMES)}", "",
            city, generate_postcode(random.choice(postcodes)), "GBR",
            value, ld["disbursement"].isoformat(), "Commercial Valuation",
            "Commercial", "", "Leasehold", random.randint(1960, 2020),
            f"INS-{random.randint(100000,999999)}", "", "",
        ])
        coll_id += 1

write_csv("collateral.csv", collateral,
    ["collateral_id", "loan_id", "collateral_type", "description",
     "address_line_1", "address_line_2", "city", "postcode", "country",
     "estimated_value", "valuation_date", "valuation_source",
     "property_type", "bedrooms", "tenure", "year_built",
     "insurance_policy_ref", "ltv_at_origination", "current_ltv"])

# ------ PAYMENTS ------
print("[9/12] Generating payment schedule & payments...")
schedules = []
payments = []
sched_id = 1
pay_counter = 1

for lid in loan_ids:
    ld = loan_data[lid]
    if ld["status"] in ("Written Off",) and ld["remaining"] == ld["term"]:
        continue  # no payments ever made

    balance = ld["amount"]
    monthly_rate = ld["rate"] / 12
    payment_date = ld["disbursement"] + timedelta(days=30)

    num_payments = ld["term"] - ld["remaining"]
    if ld["status"] in ("Closed", "Settled Early"):
        num_payments = ld["term"]

    # Limit schedule entries to keep data manageable
    max_schedule = min(num_payments + 6, ld["term"])

    for pn in range(1, max_schedule + 1):
        interest_due = round_decimal(balance * monthly_rate)
        principal_due = round_decimal(ld["monthly"] - interest_due)
        if principal_due < 0:
            principal_due = 0
        total_due = round_decimal(principal_due + interest_due)
        balance = max(0, round_decimal(balance - principal_due))

        sched_status = "Paid" if pn <= num_payments else "Scheduled"
        if ld["status"] == "Arrears" and pn == num_payments:
            sched_status = random.choice(["Partial", "Missed", "Late"])
        if ld["status"] == "Default" and pn >= num_payments - 2:
            sched_status = "Missed"

        schedules.append([
            sched_id, lid, pn, payment_date.isoformat(),
            principal_due, interest_due, total_due, balance, sched_status,
        ])

        # Generate actual payment record for paid/late schedules
        if sched_status in ("Paid", "Late"):
            pay_date = payment_date if sched_status == "Paid" else payment_date + timedelta(days=random.randint(1, 15))
            pay_id = f"PAY-{pay_counter:08d}"
            pay_counter += 1

            method = random.choices(
                ["Direct Debit", "Standing Order", "Bank Transfer", "Overpayment"],
                weights=[0.70, 0.15, 0.10, 0.05], k=1
            )[0]

            payments.append([
                pay_id, lid, sched_id, pay_date.isoformat(),
                total_due, principal_due, interest_due, 0,
                method, "Completed", f"REF-{random.randint(100000,999999)}",
            ])
        elif sched_status == "Partial":
            partial_amt = round_decimal(total_due * random.uniform(0.3, 0.7))
            pay_id = f"PAY-{pay_counter:08d}"
            pay_counter += 1
            payments.append([
                pay_id, lid, sched_id, payment_date.isoformat(),
                partial_amt, round_decimal(partial_amt * 0.6),
                round_decimal(partial_amt * 0.4), 0,
                "Direct Debit", "Completed", f"REF-{random.randint(100000,999999)}",
            ])

        sched_id += 1
        payment_date += timedelta(days=30)

write_csv("payment_schedule.csv", schedules,
    ["schedule_id", "loan_id", "payment_number", "due_date",
     "principal_due", "interest_due", "total_due",
     "outstanding_balance", "status"])

write_csv("payments.csv", payments,
    ["payment_id", "loan_id", "schedule_id", "payment_date",
     "amount", "principal_portion", "interest_portion", "fees_portion",
     "payment_method", "payment_status", "reference"])

# ------ COLLECTIONS ------
print("[10/12] Generating collections data...")
collections = []
coll_counter = 1

for lid in loan_ids:
    ld = loan_data[lid]
    if ld["status"] not in ("Arrears", "Default", "Written Off"):
        continue

    stage_map = {
        "Arrears": random.choice(["Early Arrears", "Late Arrears"]) if ld["dpd"] < 60 else "Late Arrears",
        "Default": random.choice(["Default", "Litigation"]),
        "Written Off": random.choice(["Write Off", "Recovery"]),
    }
    stage = stage_map[ld["status"]]

    arrears_start = ld["disbursement"] + timedelta(days=random.randint(180, max(181, (date(2025, 10, 1) - ld["disbursement"]).days - 90)))
    contact_attempts = random.randint(1, 20)
    last_contact = random_date(arrears_start, date(2025, 10, 1))

    arrangement = random.random() < 0.35
    arrangement_amt = round_decimal(ld["monthly"] * random.uniform(0.3, 0.8)) if arrangement else None

    outcome = None
    if ld["status"] == "Written Off":
        outcome = random.choice(["Written Off", "Sold"])
    elif arrangement:
        outcome = "Ongoing"

    collections.append([
        coll_counter, lid, ld["cid"], stage,
        arrears_start.isoformat(), ld["arrears"], ld["dpd"],
        contact_attempts, last_contact.isoformat(),
        random.choice(["Phone", "Letter", "Email", "SMS"]),
        arrangement, arrangement_amt if arrangement_amt else "",
        f"AGT-{random.randint(100,999)}",
        outcome if outcome else "",
        random.choice([
            "Customer contacted, payment plan discussed",
            "No response to communications",
            "Customer experiencing financial hardship",
            "Awaiting further documentation",
            "Referred to specialist team",
            "Payment arrangement agreed",
        ]) if random.random() < 0.7 else "",
    ])
    coll_counter += 1

write_csv("collections.csv", collections,
    ["collection_id", "loan_id", "customer_id", "collection_stage",
     "arrears_start_date", "arrears_amount", "days_in_arrears",
     "contact_attempts", "last_contact_date", "last_contact_method",
     "arrangement_in_place", "arrangement_amount", "assigned_agent",
     "outcome", "notes"])

# ------ CREDIT BUREAU DATA ------
print("[11/12] Generating credit bureau data...")
bureau_data = []
bureau_id = 1

bureaus = ["Experian", "Equifax", "TransUnion"]
for cid in customer_ids:
    # Each customer has 1-3 bureau records (different dates/bureaus)
    num_records = random.randint(1, 3)
    for _ in range(num_records):
        bureau = random.choice(bureaus)
        report_date = random_date(date(2023, 1, 1), date(2025, 10, 1))

        risk = customer_data[cid]["risk"]
        score_ranges = {
            "Low": (720, 999), "Standard": (620, 800),
            "Medium": (520, 700), "High": (400, 600), "Very High": (300, 500),
        }
        lo, hi = score_ranges[risk]
        score = random.randint(lo, hi)

        if score >= 800:
            band = "Excellent"
        elif score >= 670:
            band = "Good"
        elif score >= 560:
            band = "Fair"
        elif score >= 440:
            band = "Poor"
        else:
            band = "Very Poor"

        total_accts = random.randint(3, 20)
        active_accts = random.randint(2, total_accts)
        defaulted = random.randint(0, 3) if risk in ("High", "Very High") else (1 if random.random() < 0.05 else 0)

        income = customer_data[cid].get("income", 40000)
        total_debt = round_decimal(random.uniform(income * 0.5, income * 4))
        monthly_commit = round_decimal(total_debt / random.uniform(24, 120))

        ccjs = random.randint(0, 2) if risk in ("High", "Very High") else 0
        bankruptcies = 1 if risk == "Very High" and random.random() < 0.1 else 0
        ivas = 1 if risk in ("High", "Very High") and random.random() < 0.05 else 0
        missed = random.randint(0, 6) if risk in ("Medium", "High", "Very High") else (1 if random.random() < 0.05 else 0)
        hard_searches = random.randint(0, 8)

        bureau_data.append([
            bureau_id, cid, bureau, report_date.isoformat(),
            score, band, total_accts, active_accts, defaulted,
            total_debt, monthly_commit, ccjs, bankruptcies, ivas,
            missed, hard_searches,
            random.random() < 0.95, random.random() < 0.005,
        ])
        bureau_id += 1

write_csv("credit_bureau_data.csv", bureau_data,
    ["bureau_id", "customer_id", "bureau_name", "report_date",
     "credit_score", "score_band", "total_accounts", "active_accounts",
     "defaulted_accounts", "total_debt", "monthly_commitments",
     "ccjs_count", "bankruptcies", "iva_count",
     "missed_payments_12m", "hard_searches_12m",
     "electoral_roll", "fraud_alert"])

# ------ RISK RATINGS ------
print("[12/12] Generating risk ratings & loan performance...")
risk_ratings = []
risk_id = 1
performance = []
perf_id = 1

for lid in loan_ids:
    ld = loan_data[lid]

    # PD based on risk
    risk = customer_data[ld["cid"]]["risk"]
    pd_ranges = {
        "Low": (0.001, 0.02), "Standard": (0.01, 0.05),
        "Medium": (0.03, 0.12), "High": (0.08, 0.25), "Very High": (0.15, 0.50),
    }
    pd_lo, pd_hi = pd_ranges[risk]
    pd = round_decimal(random.uniform(pd_lo, pd_hi), 5)

    # LGD
    if ld["secured"]:
        lgd = round_decimal(random.uniform(0.10, 0.40), 5)
    else:
        lgd = round_decimal(random.uniform(0.30, 0.70), 5)

    ead = ld["balance"]
    expected_loss = round_decimal(pd * lgd * ead)
    risk_weight = round_decimal(random.uniform(0.20, 1.50), 4)

    # Internal rating
    if pd < 0.005:
        rating = "AAA"
    elif pd < 0.01:
        rating = "AA"
    elif pd < 0.02:
        rating = "A"
    elif pd < 0.05:
        rating = "BBB"
    elif pd < 0.10:
        rating = "BB"
    elif pd < 0.15:
        rating = "B"
    elif pd < 0.25:
        rating = "CCC"
    elif pd < 0.40:
        rating = "CC"
    elif pd < 0.60:
        rating = "C"
    else:
        rating = "D"

    # IFRS 9 Stage
    if ld["status"] in ("Active",) and ld["dpd"] == 0:
        ifrs9 = 1
        reg_cat = "Performing"
    elif ld["status"] in ("Arrears", "Restructured") or (0 < ld["dpd"] < 90):
        ifrs9 = 2
        reg_cat = "Underperforming"
    else:
        ifrs9 = 3 if ld["status"] in ("Default", "Written Off") else 1
        reg_cat = "Non-Performing" if ifrs9 == 3 else "Performing"

    provision = round_decimal(expected_loss * [1.0, 2.5, 8.0][ifrs9 - 1] * random.uniform(0.8, 1.2))

    risk_ratings.append([
        risk_id, lid, date(2025, 10, 1).isoformat(),
        pd, lgd, ead, expected_loss, risk_weight,
        rating, reg_cat, ifrs9, provision, "v3.2",
    ])
    risk_id += 1

    # Monthly performance snapshots (last 12 months)
    for m in range(12):
        snap_date = date(2024, 11, 1) + timedelta(days=30 * m)
        if snap_date > date(2025, 10, 1):
            break
        if snap_date < ld["disbursement"]:
            continue

        months_from_start = (snap_date - ld["disbursement"]).days // 30
        monthly_rate = ld["rate"] / 12
        if monthly_rate > 0 and months_from_start < ld["term"]:
            bal_factor = ((1 + monthly_rate) ** ld["term"] - (1 + monthly_rate) ** months_from_start) / \
                         ((1 + monthly_rate) ** ld["term"] - 1)
            snap_balance = round_decimal(ld["amount"] * bal_factor)
        else:
            snap_balance = 0

        snap_dpd = max(0, ld["dpd"] - (12 - m) * 5) if ld["dpd"] > 0 else 0
        snap_arrears = round_decimal(ld["monthly"] * max(0, snap_dpd // 30)) if snap_dpd > 0 else 0

        snap_status = ld["status"]
        if snap_dpd == 0 and ld["status"] in ("Arrears", "Default"):
            snap_status = "Active"
        elif 0 < snap_dpd < 90 and ld["status"] == "Default":
            snap_status = "Arrears"

        snap_ifrs9 = 1 if snap_dpd == 0 else (2 if snap_dpd < 90 else 3)
        snap_provision = round_decimal(provision * (m + 1) / 12)

        performance.append([
            perf_id, lid, snap_date.isoformat(), snap_balance,
            ld["rate"], snap_dpd, snap_arrears,
            ld["monthly"] if snap_status != "Written Off" else 0,
            round_decimal(ld["monthly"] * 0.4) if snap_status not in ("Written Off", "Default") else 0,
            round_decimal(ld["monthly"] * 0.6) if snap_status not in ("Written Off", "Default") else 0,
            0, snap_status, snap_ifrs9, snap_provision,
        ])
        perf_id += 1

write_csv("risk_ratings.csv", risk_ratings,
    ["rating_id", "loan_id", "rating_date", "pd_score", "lgd_score",
     "ead_amount", "expected_loss", "risk_weight", "internal_rating",
     "regulatory_category", "ifrs9_stage", "provision_amount", "model_version"])

write_csv("loan_performance_monthly.csv", performance,
    ["snapshot_id", "loan_id", "snapshot_date", "outstanding_balance",
     "interest_rate", "days_past_due", "arrears_amount", "payment_received",
     "principal_paid", "interest_paid", "fees_charged", "loan_status",
     "ifrs9_stage", "provision_amount"])

# ------ LOAN COVENANTS (for business loans only) ------
print("Generating loan covenants for business loans...")
covenants = []
cov_id = 1
covenant_types = ["Debt Service Coverage", "Loan to Value", "Interest Coverage",
                  "Current Ratio", "Net Worth", "Revenue Minimum"]

for lid in loan_ids:
    ld = loan_data[lid]
    if ld["category"] != "Business Loan":
        continue

    num_covenants = random.randint(1, 3)
    chosen = random.sample(covenant_types, num_covenants)
    for ct in chosen:
        thresholds = {
            "Debt Service Coverage": (1.2, 2.0),
            "Loan to Value": (0.5, 0.8),
            "Interest Coverage": (2.0, 5.0),
            "Current Ratio": (1.0, 2.5),
            "Net Worth": (100000, 5000000),
            "Revenue Minimum": (200000, 10000000),
        }
        lo, hi = thresholds[ct]
        threshold = round_decimal(random.uniform(lo, hi), 4)
        freq = random.choice(["Quarterly", "Semi-Annual", "Annual"])
        tested_date = random_date(date(2025, 1, 1), date(2025, 10, 1))
        tested_val = round_decimal(threshold * random.uniform(0.8, 1.3), 4)
        status = "Compliant" if tested_val >= threshold else "Breached"

        covenants.append([
            cov_id, lid, ct, threshold, freq,
            tested_date.isoformat(), tested_val, status,
        ])
        cov_id += 1

write_csv("loan_covenants.csv", covenants,
    ["covenant_id", "loan_id", "covenant_type", "threshold_value",
     "measurement_frequency", "last_tested_date", "last_tested_value", "status"])

print("\n" + "=" * 60)
print("DATA GENERATION COMPLETE")
print("=" * 60)

# Summary stats
print(f"\nCustomers:          {len(customers):,}")
print(f"Addresses:          {len(addresses):,}")
print(f"Employment:         {len(employment):,}")
print(f"Accounts:           {len(accounts):,}")
print(f"Loan Products:      {len(loan_products):,}")
print(f"Applications:       {len(applications):,}")
print(f"Loans:              {len(loans):,}")
print(f"Collateral:         {len(collateral):,}")
print(f"Payment Schedules:  {len(schedules):,}")
print(f"Payments:           {len(payments):,}")
print(f"Collections:        {len(collections):,}")
print(f"Credit Bureau:      {len(bureau_data):,}")
print(f"Risk Ratings:       {len(risk_ratings):,}")
print(f"Perf Snapshots:     {len(performance):,}")
print(f"Covenants:          {len(covenants):,}")
print(f"\nAll CSV files in: {OUTPUT_DIR}")
