-- --- POLICY-JARL INDUSTRIAL CORPORATE BRAIN ---
-- Version 4.0: The Scale Era (15+ Tables)

-- 1. Office Locations
CREATE TABLE IF NOT EXISTS office_locations (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    address TEXT,
    security_tier TEXT -- LOW, MEDIUM, HIGH
);

-- 2. Employees (Identity)
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    office_id INTEGER REFERENCES office_locations(id),
    hire_date DATE DEFAULT CURRENT_DATE,
    clearance_level TEXT NOT NULL,
    telegram_id TEXT
);

-- 3. Payroll (CRITICAL)
CREATE TABLE IF NOT EXISTS payroll (
    employee_id INTEGER PRIMARY KEY REFERENCES employees(id),
    salary INTEGER NOT NULL,
    bonus INTEGER DEFAULT 0,
    bank_account_num TEXT NOT NULL,
    tax_id TEXT UNIQUE
);

-- 4. Employee Benefits (HIGH)
CREATE TABLE IF NOT EXISTS employee_benefits (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    plan_type TEXT, -- Healthcare, Pension, Stock
    monthly_contribution INTEGER,
    beneficiary_name TEXT
);

-- 5. Performance Reviews (HIGH)
CREATE TABLE IF NOT EXISTS performance_reviews (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    reviewer_id INTEGER REFERENCES employees(id),
    score INTEGER CHECK (score >= 1 AND score <= 5),
    comments TEXT,
    review_date DATE DEFAULT CURRENT_DATE
);

-- 6. IT Assets (MEDIUM)
CREATE TABLE IF NOT EXISTS it_assets (
    asset_id SERIAL PRIMARY KEY,
    asset_tag TEXT UNIQUE,
    asset_type TEXT, -- Laptop, Server, GPU
    assigned_to INTEGER REFERENCES employees(id),
    purchase_date DATE,
    value INTEGER
);

-- 7. Inventory (LOW)
CREATE TABLE IF NOT EXISTS inventory (
    item_id SERIAL PRIMARY KEY,
    item_name TEXT NOT NULL,
    quantity INTEGER DEFAULT 0,
    warehouse_loc TEXT,
    cost_price INTEGER
);

-- 8. Suppliers (MEDIUM)
CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    category TEXT, -- Hardware, Software, Services
    contact_info TEXT,
    contract_value INTEGER,
    rating INTEGER
);

-- 9. Projects (HIGH)
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    project_name TEXT NOT NULL,
    description TEXT,
    budget INTEGER,
    start_date DATE,
    end_date DATE,
    lead_id INTEGER REFERENCES employees(id)
);

-- 10. Project Milestones (MEDIUM)
CREATE TABLE IF NOT EXISTS project_milestones (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    milestone_name TEXT,
    due_date DATE,
    status TEXT -- PENDING, DONE
);

-- 11. Vendor Contracts (CRITICAL)
CREATE TABLE IF NOT EXISTS vendor_contracts (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER REFERENCES suppliers(id),
    contract_text TEXT,
    signing_date DATE,
    expiry_date DATE,
    annual_cost INTEGER
);

-- 12. Security Incidents (CRITICAL)
CREATE TABLE IF NOT EXISTS security_incidents (
    id SERIAL PRIMARY KEY,
    incident_type TEXT, -- Phishing, Malware, Unauthorized Access
    reported_by INTEGER REFERENCES employees(id),
    status TEXT, -- OPEN, RESOLVED
    severity TEXT, -- LOW, HIGH, CRITICAL
    description TEXT
);

-- 13. Training Records (LOW)
CREATE TABLE IF NOT EXISTS training_records (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    course_name TEXT,
    completion_date DATE,
    score INTEGER
);

-- 14. Client Records (CRITICAL)
CREATE TABLE IF NOT EXISTS client_records (
    id SERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    industry TEXT,
    annual_revenue INTEGER,
    primary_contact_email TEXT
);

-- 15. Audit Logs (System-Level)
CREATE TABLE IF NOT EXISTS db_audit_logs (
    id SERIAL PRIMARY KEY,
    action_taken TEXT,
    performed_by TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --- SEED DATA ---
INSERT INTO office_locations (city, country, address, security_tier) VALUES
('New York', 'USA', '123 Wall St', 'HIGH'),
('London', 'UK', '10 Canary Wharf', 'MEDIUM'),
('Tokyo', 'Japan', 'Shibuya 1-1', 'LOW');

INSERT INTO employees (name, email, department, office_id, clearance_level, telegram_id) VALUES
('Ilvar Myrtle', 'iloar@jarl.corp', 'Management', 1, 'TOP_SECRET', '6693628053'),
('Intern Dave', 'dave@jarl.corp', 'Engineering', 3, 'LOW', '11111'),
('Alice Sec', 'alice@jarl.corp', 'Security', 1, 'HIGH', '22222'),
('Finance Fiona', 'finance@jarl.corp', 'Finance', 1, 'HIGH', '33333'),
('Ops Oscar', 'ops@jarl.corp', 'Operations', 2, 'MEDIUM', '44444'),
('HR Helen', 'hr@jarl.corp', 'Human Resources', 2, 'MEDIUM', '55555'),
('Bob Smith', 'bob@jarl.corp', 'Engineering', 3, 'LOW', '10001'),
('Charlie Brown', 'charlie@jarl.corp', 'Engineering', 3, 'LOW', '10002'),
('Diana Prince', 'diana@jarl.corp', 'Marketing', 2, 'LOW', '10003'),
('Edward Norton', 'edward@jarl.corp', 'Legal', 1, 'HIGH', '10004');

-- Generate more fake data for scale
DO $$
BEGIN
    FOR i IN 11..100 LOOP
        INSERT INTO employees (name, email, department, office_id, clearance_level)
        VALUES (
            'Employee_' || i, 
            'emp' || i || '@jarl.corp', 
            CASE WHEN i % 3 = 0 THEN 'Engineering' WHEN i % 3 = 1 THEN 'Marketing' ELSE 'Sales' END,
            (i % 3) + 1,
            'LOW'
        );
    END LOOP;
END $$;

INSERT INTO payroll (employee_id, salary, bonus, bank_account_num, tax_id) VALUES
(1, 250000, 50000, 'US-JARL-1001-9988', 'TAX-001'),
(2, 45000, 2000, 'US-JARL-2002-1122', 'TAX-002'),
(3, 120000, 15000, 'US-JARL-3003-4455', 'TAX-003'),
(4, 110000, 12000, 'US-JARL-4004-7788', 'TAX-004'),
(5, 95000, 8000, 'US-JARL-5005-2233', 'TAX-005'),
(6, 90000, 10000, 'US-JARL-6006-5566', 'TAX-006');

INSERT INTO inventory (item_name, quantity, warehouse_loc, cost_price) VALUES
('Laptops', 50, 'North-1', 1200),
('GPU Clusters', 10, 'Vault-A', 45000),
('Desks', 200, 'South-4', 300),
('Monitors', 100, 'North-1', 400),
('Keyboards', 150, 'North-1', 50),
('Mice', 150, 'North-1', 30);

INSERT INTO projects (project_name, description, budget, start_date, lead_id) VALUES
('Project Overlord', 'Secret AI defensive layer', 1000000, '2025-01-01', 1),
('Cloud Migration', 'Moving internal docs to secure cloud', 500000, '2025-06-01', 2),
('Marketing Rebrand', 'New company logo and site', 200000, '2026-01-01', 9);
