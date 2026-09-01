import uuid
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, date, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.deal import Opportunity, OpportunityStage, TaskItem
from app.models.journey import JourneyMacroStage, StageEvent
from app.repositories import journey_repo, deal_repo
from app.schemas.journey import (
    JourneyActionDefinition,
    BlockedActionDefinition,
    JourneyStateResponse,
    JourneyTransitionRequest,
    JourneyTransitionResponse,
    StageEventResponse
)

# Macro stage mapping for each deal stage
STAGE_MACRO_MAP: Dict[OpportunityStage, JourneyMacroStage] = {
    OpportunityStage.matched: JourneyMacroStage.find_buyers,
    OpportunityStage.pitch_drafted: JourneyMacroStage.connect,
    OpportunityStage.outreach_sent: JourneyMacroStage.connect,
    OpportunityStage.reply_positive: JourneyMacroStage.connect,
    OpportunityStage.sample_requested: JourneyMacroStage.sample_and_quote,
    OpportunityStage.sample_sent: JourneyMacroStage.sample_and_quote,
    OpportunityStage.sample_approved: JourneyMacroStage.sample_and_quote,
    OpportunityStage.quote_sent: JourneyMacroStage.sample_and_quote,
    OpportunityStage.contract_negotiation: JourneyMacroStage.sample_and_quote,
    OpportunityStage.po_received: JourneyMacroStage.fulfil_order,
    OpportunityStage.in_production: JourneyMacroStage.fulfil_order,
    OpportunityStage.closed_won: JourneyMacroStage.repeat,
    OpportunityStage.closed_lost: JourneyMacroStage.repeat,
}

STAGE_TITLES: Dict[OpportunityStage, str] = {
    OpportunityStage.matched: "1. Buyer Matched & Shortlisted",
    OpportunityStage.pitch_drafted: "2. Outreach Pitch Drafted",
    OpportunityStage.outreach_sent: "3. Direct Outreach Sent",
    OpportunityStage.reply_positive: "4. Positive Buyer Response",
    OpportunityStage.sample_requested: "5. Sample Swatch Requested",
    OpportunityStage.sample_sent: "6. Sample Kit Dispatched",
    OpportunityStage.sample_approved: "7. Quality & Sample Approved",
    OpportunityStage.quote_sent: "8. Landed-Cost Quotation Sent",
    OpportunityStage.contract_negotiation: "9. Contract Terms Negotiation",
    OpportunityStage.po_received: "10. Export Purchase Order Received",
    OpportunityStage.in_production: "11. Tannery Production & QC",
    OpportunityStage.closed_won: "12. Order Won & Realized",
    OpportunityStage.closed_lost: "Archived / Closed Lost",
}

OWNER_QUESTIONS: Dict[JourneyMacroStage, str] = {
    JourneyMacroStage.get_ready: "Can my business export this product?",
    JourneyMacroStage.find_buyers: "Who should I sell to?",
    JourneyMacroStage.connect: "How should I approach them?",
    JourneyMacroStage.sample_and_quote: "What should I send and what price should I offer?",
    JourneyMacroStage.fulfil_order: "What must we manufacture and by when?",
    JourneyMacroStage.ship: "What documents and logistics are required?",
    JourneyMacroStage.get_paid: "Have I received and properly closed the export payment?",
    JourneyMacroStage.repeat: "Was this profitable and what should I do next?",
}

def get_journey_state(db: Session, opp_id: uuid.UUID) -> Optional[JourneyStateResponse]:
    """Retrieve full journey state, available actions, blockers, and history for an opportunity."""
    opp = deal_repo.get_opportunity(db, opp_id)
    if not opp:
        return None

    current_stage = opp.stage
    macro_stage = STAGE_MACRO_MAP.get(current_stage, JourneyMacroStage.find_buyers)
    available, blocked = compute_available_and_blocked_actions(opp)
    
    events = journey_repo.list_stage_events_for_entity(db, "opportunity", opp.id)
    history_responses = [StageEventResponse.model_validate(e) for e in events]

    return JourneyStateResponse(
        entity_id=opp.id,
        entity_type="opportunity",
        current_stage=current_stage.value,
        macro_stage=macro_stage.value,
        stage_title=STAGE_TITLES.get(current_stage, current_stage.value),
        owner_question=OWNER_QUESTIONS.get(macro_stage, "What is the next business action?"),
        available_actions=available,
        blocked_actions=blocked,
        history=history_responses
    )

def compute_available_and_blocked_actions(opp: Opportunity) -> Tuple[List[JourneyActionDefinition], List[BlockedActionDefinition]]:
    """Compute permitted next actions and human-readable blocked actions based on current stage and prerequisites."""
    current = opp.stage
    available: List[JourneyActionDefinition] = []
    blocked: List[BlockedActionDefinition] = []

    has_quotes = bool(opp.quotes and len(opp.quotes) > 0)

    if current == OpportunityStage.matched:
        available.append(JourneyActionDefinition(
            action_id="draft_pitch",
            label="Prepare Outreach Draft",
            target_stage=OpportunityStage.pitch_drafted.value,
            target_macro_stage=JourneyMacroStage.connect.value,
            required_role="sales",
            description="Generate customized export pitch matching buyer leather requirements."
        ))
        available.append(JourneyActionDefinition(
            action_id="archive_deal",
            label="Decline / Pass on Buyer",
            target_stage=OpportunityStage.closed_lost.value,
            target_macro_stage=JourneyMacroStage.repeat.value,
            required_role="owner",
            requires_evidence=True,
            evidence_prompt="Reason for declining match",
            description="Archive this buyer match if material or MOQ does not align."
        ))

    elif current == OpportunityStage.pitch_drafted:
        available.append(JourneyActionDefinition(
            action_id="send_outreach",
            label="Send Approved Outreach Email",
            target_stage=OpportunityStage.outreach_sent.value,
            target_macro_stage=JourneyMacroStage.connect.value,
            required_role="sales",
            description="Send introductory email and capability deck to procurement contact."
        ))

    elif current == OpportunityStage.outreach_sent:
        available.append(JourneyActionDefinition(
            action_id="record_reply",
            label="Record Positive Buyer Response",
            target_stage=OpportunityStage.reply_positive.value,
            target_macro_stage=JourneyMacroStage.connect.value,
            required_role="sales",
            description="Buyer responded showing interest in material swatches or pricing."
        ))
        available.append(JourneyActionDefinition(
            action_id="request_sample",
            label="Buyer Requested Sample Swatches",
            target_stage=OpportunityStage.sample_requested.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="sales",
            description="Buyer requested physical sample swatches for inspection."
        ))

    elif current == OpportunityStage.reply_positive:
        available.append(JourneyActionDefinition(
            action_id="request_sample",
            label="Record Sample Request",
            target_stage=OpportunityStage.sample_requested.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="sales",
            description="Log requested sample articles and dispatch address."
        ))
        available.append(JourneyActionDefinition(
            action_id="issue_direct_quote",
            label="Issue Indicative Quotation",
            target_stage=OpportunityStage.quote_sent.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="sales",
            description="Directly issue landed-cost quotation if sample is pre-cleared."
        ))

    elif current == OpportunityStage.sample_requested:
        available.append(JourneyActionDefinition(
            action_id="dispatch_sample",
            label="Dispatch Sample Kit (DHL/Air)",
            target_stage=OpportunityStage.sample_sent.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="operations",
            requires_evidence=True,
            evidence_prompt="Air Waybill (AWB) or courier tracking number",
            description="Confirm dispatch of 2kg leather swatch pack to Germany."
        ))

    elif current == OpportunityStage.sample_sent:
        available.append(JourneyActionDefinition(
            action_id="approve_sample",
            label="Sample Approved by Buyer Quality Team",
            target_stage=OpportunityStage.sample_approved.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="sales",
            description="Buyer verified thickness, hand-feel, and chemical testing."
        ))
        available.append(JourneyActionDefinition(
            action_id="re_sample",
            label="Buyer Requested Revision / Re-Sample",
            target_stage=OpportunityStage.sample_requested.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="operations",
            description="Re-dispatch adjusted sample article based on feedback."
        ))

    elif current == OpportunityStage.sample_approved:
        available.append(JourneyActionDefinition(
            action_id="send_quote",
            label="Issue Official Landed-Cost Quotation",
            target_stage=OpportunityStage.quote_sent.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="owner",
            description="Generate and issue quotation with FOB Chennai / CIF Hamburg terms."
        ))

    elif current == OpportunityStage.quote_sent:
        available.append(JourneyActionDefinition(
            action_id="start_negotiation",
            label="Enter Contract Negotiations",
            target_stage=OpportunityStage.contract_negotiation.value,
            target_macro_stage=JourneyMacroStage.sample_and_quote.value,
            required_role="sales",
            description="Negotiate payment terms, volume discounts, or delivery dates."
        ))
        available.append(JourneyActionDefinition(
            action_id="receive_po",
            label="Purchase Order Received",
            target_stage=OpportunityStage.po_received.value,
            target_macro_stage=JourneyMacroStage.fulfil_order.value,
            required_role="owner",
            requires_evidence=True,
            evidence_prompt="Buyer PO Number and Contract Copy",
            description="Buyer accepted quotation and issued formal Purchase Order."
        ))

    elif current == OpportunityStage.contract_negotiation:
        available.append(JourneyActionDefinition(
            action_id="receive_po",
            label="Purchase Order Confirmed",
            target_stage=OpportunityStage.po_received.value,
            target_macro_stage=JourneyMacroStage.fulfil_order.value,
            required_role="owner",
            requires_evidence=True,
            evidence_prompt="Buyer PO Number and Contract Copy",
            description="Buyer executed contract and submitted formal PO."
        ))

    elif current == OpportunityStage.po_received:
        available.append(JourneyActionDefinition(
            action_id="start_production",
            label="Release PO to Tannery Production",
            target_stage=OpportunityStage.in_production.value,
            target_macro_stage=JourneyMacroStage.fulfil_order.value,
            required_role="operations",
            description="Issue production order to Ambur factory floor with batch specifications."
        ))

    elif current == OpportunityStage.in_production:
        available.append(JourneyActionDefinition(
            action_id="complete_order",
            label="Mark Production & QC Completed",
            target_stage=OpportunityStage.closed_won.value,
            target_macro_stage=JourneyMacroStage.repeat.value,
            required_role="owner",
            requires_evidence=True,
            evidence_prompt="Finished Goods QC Certificate / Packing List",
            description="Production completed, quality cleared, ready for container loading."
        ))

    # Universal Closed Lost option for active stages
    if current not in (OpportunityStage.closed_won, OpportunityStage.closed_lost):
        available.append(JourneyActionDefinition(
            action_id="close_lost",
            label="Mark Deal Closed Lost",
            target_stage=OpportunityStage.closed_lost.value,
            target_macro_stage=JourneyMacroStage.repeat.value,
            required_role="owner",
            requires_evidence=True,
            evidence_prompt="Reason for loss (e.g. price, lead time, buyer canceled)",
            description="Archive deal with recorded loss reason."
        ))

    return available, blocked

def execute_stage_transition(
    db: Session,
    opp_id: uuid.UUID,
    req: JourneyTransitionRequest
) -> JourneyTransitionResponse:
    """
    Execute backend-governed transition with prerequisite validation and immutable audit logging.
    """
    # Check idempotency
    if req.idempotency_key:
        existing_event = journey_repo.get_event_by_idempotency_key(db, req.idempotency_key)
        if existing_event:
            opp = deal_repo.get_opportunity(db, opp_id)
            available, _ = compute_available_and_blocked_actions(opp)
            return JourneyTransitionResponse(
                success=True,
                entity_id=opp.id,
                previous_stage=existing_event.previous_stage,
                new_stage=existing_event.new_stage,
                macro_stage=existing_event.macro_stage,
                event_id=existing_event.id,
                message="Transition already executed (idempotent request).",
                available_actions=available
            )

    opp = deal_repo.get_opportunity(db, opp_id)
    if not opp:
        raise ValueError("Opportunity not found.")

    previous_stage = opp.stage
    available, blocked = compute_available_and_blocked_actions(opp)

    # Validate requested action is currently permitted
    matching_action = next((a for a in available if a.action_id == req.action_id or a.target_stage == req.action_id), None)
    if not matching_action:
        blocked_match = next((b for b in blocked if b.action_id == req.action_id), None)
        reason_msg = "; ".join(blocked_match.blocked_reasons) if blocked_match else "Action not permitted from current stage."
        raise ValueError(f"Transition rejected: {reason_msg}")

    target_stage = OpportunityStage(matching_action.target_stage)
    target_macro = STAGE_MACRO_MAP.get(target_stage, JourneyMacroStage.find_buyers)

    # Execute update on Opportunity entity
    opp.stage = target_stage
    if req.notes:
        opp.notes = f"{opp.notes}\n[{datetime.now().strftime('%Y-%m-%d')}] {req.notes}" if opp.notes else req.notes

    db.commit()
    db.refresh(opp)

    # Insert immutable StageEvent into gold.stage_events
    event = journey_repo.insert_stage_event(
        db=db,
        entity_type="opportunity",
        entity_id=opp.id,
        macro_stage=target_macro.value,
        previous_stage=previous_stage.value,
        new_stage=target_stage.value,
        action=matching_action.label,
        actor=req.actor,
        actor_role=req.actor_role,
        reason_code=req.reason_code,
        notes=req.notes,
        evidence_references=req.evidence_references,
        idempotency_key=req.idempotency_key,
        tenant_id=opp.tenant_id
    )

    # Automatically generate / update contextual tasks for Today Actions
    generate_contextual_tasks_for_transition(db, opp, target_stage)

    # Compute updated available actions
    new_available, _ = compute_available_and_blocked_actions(opp)

    return JourneyTransitionResponse(
        success=True,
        entity_id=opp.id,
        previous_stage=previous_stage.value,
        new_stage=target_stage.value,
        macro_stage=target_macro.value,
        event_id=event.id,
        message=f"Successfully transitioned to {STAGE_TITLES.get(target_stage, target_stage.value)}.",
        available_actions=new_available
    )

def generate_contextual_tasks_for_transition(db: Session, opp: Opportunity, new_stage: OpportunityStage):
    """Generate or update actionable tasks in the Today cockpit based on journey state change."""
    buyer_name = opp.buyer.legal_name if opp.buyer else "Buyer"
    
    if new_stage == OpportunityStage.sample_requested:
        task = TaskItem(
            opportunity_id=opp.id,
            buyer_id=opp.buyer_id,
            title=f"Dispatch 2kg Swatch Kit to {buyer_name}",
            description=f"Prepare 2kg swatch pack (1.2-1.4mm) with lab test certificate and send via DHL Air Express.",
            due_date=date.today() + timedelta(days=2),
            priority="urgent",
            status="todo",
            task_type="sample_dispatch",
            assigned_to="Operations Lead"
        )
        db.add(task)
        db.commit()

    elif new_stage == OpportunityStage.quote_sent:
        task = TaskItem(
            opportunity_id=opp.id,
            buyer_id=opp.buyer_id,
            title=f"Follow up on Quotation with {buyer_name}",
            description="Check with buyer procurement team if quotation terms and FOB/CIF breakdown meet their target budget.",
            due_date=date.today() + timedelta(days=5),
            priority="high",
            status="todo",
            task_type="quote_followup",
            assigned_to="Sales Lead"
        )
        db.add(task)
        db.commit()

    elif new_stage == OpportunityStage.po_received:
        task = TaskItem(
            opportunity_id=opp.id,
            buyer_id=opp.buyer_id,
            title=f"Issue Production Batch Card for {buyer_name} PO",
            description="Verify tanning chemical formulation, LWG lot number, and release 30,000 sqft batch to shop floor.",
            due_date=date.today() + timedelta(days=1),
            priority="urgent",
            status="todo",
            task_type="production_release",
            assigned_to="Operations Lead"
        )
        db.add(task)
        db.commit()
