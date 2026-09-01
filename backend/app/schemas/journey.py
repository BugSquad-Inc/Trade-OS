import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class JourneyActionDefinition(BaseModel):
    action_id: str
    label: str
    target_stage: str
    target_macro_stage: str
    required_role: str = "sales"
    requires_evidence: bool = False
    evidence_prompt: Optional[str] = None
    description: str

class BlockedActionDefinition(BaseModel):
    action_id: str
    label: str
    target_stage: str
    blocked_reasons: List[str]
    prerequisites: List[str]

class StageEventResponse(BaseModel):
    id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    macro_stage: str
    previous_stage: str
    new_stage: str
    action: str
    actor: str
    actor_role: str
    reason_code: str
    notes: Optional[str] = None
    evidence_references: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JourneyStateResponse(BaseModel):
    entity_id: uuid.UUID
    entity_type: str
    current_stage: str
    macro_stage: str
    stage_title: str
    owner_question: str
    available_actions: List[JourneyActionDefinition]
    blocked_actions: List[BlockedActionDefinition]
    history: List[StageEventResponse]

class JourneyTransitionRequest(BaseModel):
    action_id: str
    actor: str = "Johann Butler"
    actor_role: str = "owner"
    reason_code: str = "owner_decision"
    notes: Optional[str] = None
    evidence_references: Dict[str, Any] = Field(default_factory=dict)
    idempotency_key: Optional[str] = None

class JourneyTransitionResponse(BaseModel):
    success: bool
    entity_id: uuid.UUID
    previous_stage: str
    new_stage: str
    macro_stage: str
    event_id: uuid.UUID
    message: str
    available_actions: List[JourneyActionDefinition]
