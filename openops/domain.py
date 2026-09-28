from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timezone
from typing import Any
import uuid

def now(): return datetime.now(timezone.utc).isoformat()
def uid(): return str(uuid.uuid4())
class State(str, Enum):
 RECEIVED='RECEIVED'; VALIDATING='VALIDATING'; POLICY_CHECK='POLICY_CHECK'; RISK_ASSESSMENT='RISK_ASSESSMENT'; AWAITING_APPROVAL='AWAITING_APPROVAL'; APPROVED='APPROVED'; EXECUTING='EXECUTING'; SUCCEEDED='SUCCEEDED'; REJECTED='REJECTED'; BLOCKED='BLOCKED'; EXPIRED='EXPIRED'; FAILED='FAILED'; CANCELLED='CANCELLED'; TIMED_OUT='TIMED_OUT'
class Risk(str, Enum): LOW='LOW'; MEDIUM='MEDIUM'; HIGH='HIGH'; CRITICAL='CRITICAL'
@dataclass
class ActionRequest:
 action:str; payload:dict[str,Any]; actor:str='anonymous'; environment:str='development'; source:str='api'; source_event_id:str|None=None; automation:str|None=None; parent_execution_id:str|None=None; correlation_id:str=field(default_factory=uid); idempotency_key:str|None=None
@dataclass
class PolicyDecision: allowed:bool; approval_required:bool; reasons:list[str]; risk_level:str
@dataclass
class RiskAssessment: level:str; score:int; factors:list[str]
@dataclass
class ActionPlan: action:str; target:Any; risk:str; approval_required:bool; rollback_supported:bool; side_effects:list[str]
@dataclass
class Execution:
 id:str=field(default_factory=uid); state:str=State.RECEIVED.value; created_at:str=field(default_factory=now); updated_at:str=field(default_factory=now); actor:str=''; action:str=''; payload:dict[str,Any]=field(default_factory=dict); correlation_id:str=''; idempotency_key:str|None=None; plan:dict[str,Any]=field(default_factory=dict); policy:dict[str,Any]=field(default_factory=dict); risk:dict[str,Any]=field(default_factory=dict); result:dict[str,Any]=field(default_factory=dict)
 def json(self): return asdict(self)
