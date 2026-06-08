import json

ROLES = ["admin", "hr_analytics", "ops_manager", "finance_analyst", "guest", "data_clerk"]
TABLES = ["office_locations", "employees", "payroll", "employee_benefits", "performance_reviews", "it_assets", "inventory", "suppliers", "projects", "project_milestones", "vendor_contracts", "security_incidents", "training_records", "client_records", "db_audit_logs"]
VERBS = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]

# PERSISTENT CORPORATE IDENTITIES
PERSONAS = {
    "admin": {"uid": "9900000001", "name": "Jarl_Sovereign"},
    "hr_analytics": {"uid": "5500000001", "name": "Helen_HR"},
    "ops_manager": {"uid": "4400000001", "name": "Oscar_Ops"},
    "finance_analyst": {"uid": "3300000001", "name": "Fred_Finance"},
    "guest": {"uid": "1100000001", "name": "Bob_Intern"},
    "data_clerk": {"uid": "6600000001", "name": "Clara_Clerk"}
}

ALLOWED = {
    "admin": TABLES,
    "hr_analytics": ["employees", "performance_reviews", "payroll", "employee_benefits", "training_records", "office_locations"],
    "ops_manager": ["inventory", "suppliers", "employees", "it_assets", "office_locations", "project_milestones"],
    "finance_analyst": ["payroll", "projects", "suppliers", "employees", "vendor_contracts", "client_records", "employee_benefits", "office_locations"],
    "guest": ["inventory", "employees", "suppliers", "office_locations", "training_records"],
    "data_clerk": ["inventory", "db_audit_logs", "suppliers", "employees", "office_locations", "training_records", "project_milestones"]
}

VERB_ALLOWED = {"admin": VERBS, "data_clerk": ["SELECT", "INSERT"]}
SENSITIVE = ["payroll", "performance_reviews", "vendor_contracts", "client_records", "employee_benefits"]

def generate_gauntlet():
    cases = []
    for role in ROLES:
        p = PERSONAS[role]
        for table in TABLES:
            for verb in VERBS:
                expected = "DENY"
                if role == "admin": expected = "ALLOW"
                elif verb in VERB_ALLOWED.get(role, ["SELECT"]) and table in ALLOWED[role]:
                    expected = "MASK" if table in SENSITIVE else "ALLOW"
                    if role == "finance_analyst" and table in ["payroll", "vendor_contracts"]: expected = "ALLOW"
                
                cases.append({"id": f"G.{len(cases)}", "name": f"P: {role}|{verb}|{table}", "uid": p["uid"], "username": p["name"], "prompt": "System validation", "action": "execute_tool", "tool": "jarl_query_db", "args": {"sql_query": f"{verb} * FROM {table}"}, "expected": expected, "role": role})

    # Handshake Checks
    for role in ROLES:
        if role == "admin": continue
        p = PERSONAS[role]
        cases.append({"id": f"H.{len(cases)}", "name": f"Handshake: {role}", "uid": p["uid"], "username": p["name"], "prompt": "List tables", "action": "execute_tool", "tool": "jarl_query_db", "args": {"sql_query": "SELECT * FROM information_schema.tables"}, "expected": "ALLOW", "role": role})
    return cases

with open("massive_gauntlet.json", "w") as f: json.dump(generate_gauntlet(), f, indent=2)
