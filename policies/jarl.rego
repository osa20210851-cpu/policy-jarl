package jarl

import future.keywords.if
import future.keywords.in

# --- THE CONSTITUTION ---
# Forensic Priority: Identity -> Safety -> SEMANTIC MISMATCH -> Handshake -> RBAC/Verb

# Dynamically pull the JWT secret from the environment variables
jwt_secret := opa.runtime().env.JWT_SECRET

# 1. GOVERNANCE REGISTRY
role_permissions := {
    "admin": ["payroll", "performance_reviews", "projects", "employees", "inventory", "suppliers", "it_assets", "db_audit_logs", "office_locations", "employee_benefits", "vendor_contracts", "security_incidents", "training_records", "client_records", "project_milestones"],
    "data_clerk": ["inventory", "db_audit_logs", "suppliers", "employees", "office_locations", "training_records", "project_milestones"],
    "hr_analytics": ["employees", "performance_reviews", "payroll", "employee_benefits", "training_records", "office_locations"],
    "ops_manager": ["inventory", "suppliers", "employees", "it_assets", "office_locations", "project_milestones", "training_records"],
    "finance_analyst": ["payroll", "projects", "suppliers", "employees", "vendor_contracts", "client_records", "employee_benefits", "office_locations"],
    "guest": ["inventory", "employees", "suppliers", "office_locations", "training_records"]
}

role_verbs := {
    "admin": ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"],
    "data_clerk": ["SELECT", "INSERT"],
    "hr_analytics": ["SELECT"],
    "ops_manager": ["SELECT"],
    "finance_analyst": ["SELECT"],
    "guest": ["SELECT"]
}

mask_exceptions := {
    "payroll": ["admin", "finance_analyst"],
    "performance_reviews": ["admin"],
    "projects": ["admin", "finance_analyst"],
    "employee_benefits": ["admin", "hr_analytics"],
    "vendor_contracts": ["admin", "finance_analyst"],
    "security_incidents": ["admin"],
    "client_records": ["admin", "finance_analyst"],
    "employees": ["admin", "finance_analyst"],
    "suppliers": ["admin", "ops_manager", "finance_analyst"],
    "it_assets": ["admin", "ops_manager"],
    "inventory": ["admin", "ops_manager"]
}

table_metadata := {
    "payroll": {"mask_columns": ["salary", "bonus", "bank_account_num", "tax_id"]},
    "performance_reviews": {"mask_columns": ["comments"]},
    "projects": {"mask_columns": ["budget"]},
    "employee_benefits": {"mask_columns": ["monthly_contribution"]},
    "vendor_contracts": {"mask_columns": ["annual_cost", "contract_text"]},
    "security_incidents": {"mask_columns": ["description"]},
    "client_records": {"mask_columns": ["annual_revenue", "primary_contact_email"]},
    "employees": {"mask_columns": ["email", "clearance_level", "hire_date", "office_id"]},
    "suppliers": {"mask_columns": ["contact_info", "contract_value"]},
    "it_assets": {"mask_columns": ["value"]},
    "project_milestones": {"mask_columns": []},
    "office_locations": {"mask_columns": []},
    "inventory": {"mask_columns": ["cost_price"]},
    "training_records": {"mask_columns": []},
    "db_audit_logs": {"mask_columns": []}
}

# 2. IDENTITY VERIFICATION
decoded_jwt := [valid, header, payload] if {
    input.user.token != ""
    input.user.token != null
    [valid, header, payload] := io.jwt.decode_verify(input.user.token, {"secret": jwt_secret, "alg": "HS256"})
}

trusted_role := role if {
    decoded_jwt[0] == true
    role := decoded_jwt[2].role
} else := "unverified"

# --- VERDICT ENGINE ---

default verdict := {"decision": "DENY", "reason": "DEFAULT_DENY", "risk_level": "HIGH", "mask_columns": [], "sql_patch": "NONE"}

# LAYER 1: PHYSICAL SAFETY
verdict := {"decision": "DENY", "reason": "SYSTEM_LOCKED", "risk_level": "CRITICAL", "mask_columns": [], "sql_patch": "NONE"} if {
    input.context.system_status == "LOCKED"
}

# LAYER 2: BEHAVIORAL INTELLIGENCE (PILLAR 16)
# THE CROWN JEWEL: Detect contradictions BEFORE checking permissions.
else := {
    "decision": "ESCALATE",
    "reason": "SEMANTIC_MISMATCH: Reasoning does not match physical action.",
    "risk_level": "HIGH",
    "mask_columns": [],
    "sql_patch": "NONE"
} if {
    input.request.action == "execute_tool"
    intent := object.get(input.signals, "intent_verb", "UNKNOWN")
    sql_obj := object.get(input.signals, "sql", {})
    verb := upper(object.get(sql_obj, "verb", "UNKNOWN"))
    
    intent == "READ"
    verb in ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER"]
}

# LAYER 3: SOVEREIGN OVERRIDE
else := {"decision": "ALLOW", "reason": "ADMIN_OVERRIDE", "risk_level": "LOW", "mask_columns": [], "sql_patch": "NONE"} if {
    trusted_role == "admin"
}

# LAYER 4: CONTEXTUAL GOVERNANCE (DISCOVERY)
else := {
    "decision": "ALLOW",
    "reason": "GOVERNED_DISCOVERY: Metadata handshake.",
    "risk_level": "LOW",
    "mask_columns": [],
    "sql_patch": sprintf("WHERE table_name IN ('%s')", [concat("','", tables)])
} if {
    input.request.action == "execute_tool"
    sql_obj := object.get(input.signals, "sql", {})
    object.get(sql_obj, "is_metadata_discovery", false) == true
    tables := object.get(role_permissions, trusted_role, ["inventory", "employees"])
}

# LAYER 5: HARD SECURITY (BLOCKS)
else := {"decision": "DENY", "reason": "UNAUTHORIZED_SQL_VERB", "risk_level": "CRITICAL", "mask_columns": [], "sql_patch": "NONE"} if {
    input.request.action == "execute_tool"
    allowed_verbs := object.get(role_verbs, trusted_role, ["SELECT"])
    sql_obj := object.get(input.signals, "sql", {})
    verb := upper(object.get(sql_obj, "verb", "UNKNOWN"))
    not verb in allowed_verbs
}

else := {"decision": "DENY", "reason": "INSUFFICIENT_CLEARANCE", "risk_level": "HIGH", "mask_columns": [], "sql_patch": "NONE"} if {
    input.request.action == "execute_tool"
    allowed_list := object.get(role_permissions, trusted_role, [])
    sql_obj := object.get(input.signals, "sql", {})
    tables := object.get(sql_obj, "tables", [])
    some t in tables
    not lower(t) in allowed_list
}

# LAYER 6: DATA TRANSFORMATION (MASKING)
else := {
    "decision": "MASK",
    "reason": "DATA_MASKING_APPLIED",
    "risk_level": "LOW",
    "mask_columns": cols,
    "sql_patch": "NONE"
} if {
    input.request.action == "execute_tool"
    sql_obj := object.get(input.signals, "sql", {})
    verb := upper(object.get(sql_obj, "verb", "UNKNOWN"))
    verb == "SELECT"
    
    tables := object.get(sql_obj, "tables", [])
    some t in tables
    table_name := lower(t)
    cols := table_metadata[table_name].mask_columns
    count(cols) > 0
    exempt_roles := object.get(mask_exceptions, table_name, ["admin"])
    not trusted_role in exempt_roles
}

# LAYER 7: OUTBOUND GOVERNANCE
else := {"decision": "DENY", "reason": "DLP_VIOLATION", "risk_level": "CRITICAL", "mask_columns": [], "sql_patch": "NONE"} if {
    input.request.action == "inspect_response"
    input.signals.contains_pii == true
}

else := {"decision": "DENY", "reason": "MISSION_DRIFT", "risk_level": "MEDIUM", "mask_columns": [], "sql_patch": "NONE"} if {
    input.request.action == "inspect_response"
    content := lower(object.get(input.signals, "raw_content", ""))
    not regex.match("(?i)(hello|greetings|welcome|hi|morning|afternoon|evening|assist|help)", content)
    not contains(content, "data")
    not contains(content, "table")
    not contains(content, "record")
    not contains(content, "policy")
}

else := {"decision": "ALLOW", "reason": "OUTPUT_CLEARED", "risk_level": "LOW", "mask_columns": [], "sql_patch": "NONE"} if {
    input.request.action == "inspect_response"
}

# LAYER 8: FINAL DISPOSITION
else := {"decision": "ALLOW", "reason": "GOVERNED_ACCESS", "risk_level": "LOW", "mask_columns": [], "sql_patch": "NONE"} if {
    input.request.action == "execute_tool"
    trusted_role != "unverified"
}

else := {"decision": "ALLOW", "reason": "VERIFIED_CHAT", "risk_level": "LOW", "mask_columns": [], "sql_patch": "NONE"} if {
    input.request.action == "chat"
    trusted_role != "unverified"
}
