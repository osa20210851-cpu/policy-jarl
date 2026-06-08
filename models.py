from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE"
    MASK = "MASK" # Dynamic Data Masking decision

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class UserContext(BaseModel):
    id: str
    role: str | None = None
    token: Optional[str] = None

class RequestContext(BaseModel):
    id: str
    timestamp: str
    action: str
    tool_name: str | None = None
    tool_args: Dict[str, Any] | None = None
    tool_hash: str | None = None

class SQLSignals(BaseModel):
    verb: Optional[str] = None
    tables: List[str] = []
    columns: List[str] = []
    has_join: bool = False
    has_wildcard: bool = False
    is_destructive: bool = False
    is_metadata_discovery: bool = False # Querying information_schema

class SignalContext(BaseModel):
    severity_score: int
    contains_pii: bool
    matches_threat_pattern: list[str]
    fuzzy_matches: list[str]
    is_prompt_injection: bool
    raw_content: str | None = None 
    sql: Optional[SQLSignals] = None
    intent_verb: str | None = None # READ, WRITE, DELETE, ADMIN
    inferred_intent: str | None = None # The logic behind the intent extraction

class UserRequest(BaseModel):
    user_id: str
    prompt: str
    action: str
    tool_name: str | None = None
    tool_args: Dict[str, Any] | None = None
    correlation_id: str | None = None

class AgentResponse(BaseModel):
    user_id: str
    response_text: str
    original_request_id: str | None = None

class OPAVerdict(BaseModel):
    decision: Decision
    reason: str
    risk_level: RiskLevel
    correlation_id: str | None = None
    mask_columns: List[str] | None = None
    sql_patch: str | None = None # Instruction to rewrite the query (e.g., "LIMIT 10")

class EscalationResolution(BaseModel):
    admin_secret: str
    correlation_id: str
    decision: str # ALLOW or DENY

class EscalationResponse(BaseModel):
    status: str
    message: str

class SystemContext(BaseModel):
    alerts_last_hour: int
    session_risk: RiskLevel
    system_status: str = "ACTIVE"
    autonomy_mode: str = "DISABLED"
    jwt_secret: str | None = None

class OPAInput(BaseModel):
    user: UserContext
    request: RequestContext
    signals: SignalContext
    context: SystemContext
