# MODULE_api — FastAPI REST API
**Sprint:** S1 | **Status:** DONE | **Module ID:** M5_api

## Description
Routes: /health, /capability, /matches, /signals, /accounts/{id}, /outreach. Pydantic schemas, repositories, API key auth

## DB Models
_No entities registered yet._

## Service Functions
| Code | Name | Description |
|------|------|-------------|
| TOS-SVC-API-001 | match_service | Ranked match candidate aggregation |
| TOS-SVC-API-002 | compliance_service | EUDR 68/100 readiness and REACH calculations |
| TOS-SVC-API-003 | lane_service | Chennai to Hamburg ocean freight and transit benchmark |
| TOS-SVC-API-004 | outreach_service | AI outreach generation in 4 professional tones |

## Repository Functions
| Code | Name | Description |
|------|------|-------------|
| TOS-REP-API-001 | capability_repo | Exporter capability database queries |
| TOS-REP-API-002 | account_repo | Company, contact and product queries |
| TOS-REP-API-003 | signal_repo | Live trade signals and evidence queries |
| TOS-REP-API-004 | outreach_repo | Outreach action history logger |
| TOS-REP-API-012 | exporter_repo.py | Exporter capability profile, onboarding save-and-resume, and readiness gap analysis repository |
| TOS-REP-API-013 | product_repo.py | Product families, versions, lab test certificates, and Digital Product Passport repository |
| TOS-REP-API-015 | deal_repo.py | Deal opportunities, 12-stage lifecycle transitions, quotes, and task item repository |
| TOS-REP-API-016 | tenant_repo.py | Tenant organization provisioning, member invitation, and role management repository |
| TOS-REP-API-017 | document_repo.py | Export compliance document vault repository and hash verification |
| TOS-REP-API-018 | shipment_repo.py | Container shipment milestones and bank foreign exchange eBRC realization repository |
| TOS-REP-API-014 | verification_repo.py | Verification queue management, claim sign-off, data corrections, and entity resolution repository |

## API Routes
| Code | Name | Description |
|------|------|-------------|
| TOS-RTE-API-001 | get_capability | GET /api/v1/capability authenticated endpoint |
| TOS-RTE-API-002 | get_matches | GET /api/v1/matches authenticated endpoint |
| TOS-RTE-API-003 | get_signals_feed | GET /api/v1/signals authenticated endpoint |
| TOS-RTE-API-004 | get_account_360 | GET /api/v1/accounts/{id} authenticated endpoint |
| TOS-RTE-API-005 | generate_outreach | POST /api/v1/outreach authenticated endpoint |
| TOS-RTE-API-017 | exporters.py | FastAPI routes for exporter profiles, onboarding wizard steps, and readiness gaps |
| TOS-RTE-API-018 | products.py | FastAPI routes for product catalog, versions, certificates, and Digital Product Passports |
| TOS-RTE-API-020 | deals.py | FastAPI routes for 12-stage deal management, quotes, landed-cost calculator, and pipeline totals |
| TOS-RTE-API-021 | today.py | FastAPI routes for Today executive morning cockpit, urgent tasks, and recommended actions |
| TOS-RTE-API-022 | tenants.py | FastAPI routes for tenant organization, member provisioning, and RBAC role updates |
| TOS-RTE-API-023 | users.py | FastAPI routes for current authenticated user profile and permissions |
| TOS-RTE-API-024 | documents.py | FastAPI routes for trade document management and Compliance Rule Engine v2 audits |
| TOS-RTE-API-025 | shipments.py | FastAPI routes for container milestone radar and DGFT eBRC bank payment status |
| TOS-RTE-API-019 | verification.py | FastAPI routes for analyst verification queue, sign-offs, data corrections, and entity resolution |

## Pydantic Schemas
| Code | Name | Description |
|------|------|-------------|
| TOS-SCH-API-001 | ExporterCapabilityResponse | Pydantic capability schema |
| TOS-SCH-API-002 | MatchCardResponse / MatchListResponse | Pydantic match list and card schemas |
| TOS-SCH-API-003 | SignalListResponse / EUDRScorecardResponse | Pydantic signal feed and scorecard schemas |
| TOS-SCH-API-004 | Account360Response / ContactDetail | Pydantic Account 360 dossier schema |
| TOS-SCH-API-005 | OutreachRequest / OutreachResponse | Pydantic AI outreach request and response schemas |
| TOS-SCH-API-015 | Exporter Profile & Readiness Schemas | Pydantic v2 schemas for Indian exporter registrations and readiness gap audits |
| TOS-SCH-API-016 | Product Family & Passport Schemas | Pydantic v2 schemas for product catalog, versions, certificates, and passports |
| TOS-SCH-API-018 | Opportunity & Quotation Schemas | Pydantic v2 schemas for deals, quotes, landed cost calculations, and today cockpit |
| TOS-SCH-API-019 | Tenant & UserAccount Schemas | Pydantic v2 schemas for tenants, members, and role updates |
| TOS-SCH-API-020 | TradeDocument & Shipment Schemas | Pydantic v2 schemas for document vault, compliance checks, and shipment milestones |
| TOS-SCH-API-017 | Verification & Entity Resolution Schemas | Pydantic v2 schemas for verification queue items, claim sign-offs, and entity resolution links |
| TOS-SCH-API-014 | SourceRegistry / EvidenceAssertion Schemas | Pydantic v2 schemas for provenance and truth status |

## Background Workers
_No entities registered yet._

## Frontend Components
_No entities registered yet._

## Infrastructure Files
_No entities registered yet._

## Tests
| Code | Name | Description |
|------|------|-------------|
| TOS-TST-API-001 | test_capability.py | Pytest capability endpoint tests |
| TOS-TST-API-002 | test_provenance.py | Pytest unit tests for liveness, readiness probes and provenance table assertions |
| TOS-TST-API-004 | test_onboarding_products.py | Pytest integration tests for exporter onboarding and product passport APIs |
| TOS-TST-API-003 | test_signals.py | Pytest signals endpoint tests |
| TOS-TST-API-005 | test_verification.py | Pytest integration tests for verification queue sign-offs, corrections, and entity resolution |
| TOS-TST-API-006 | test_deals_today.py | Pytest integration tests for deals pipeline, quotes, landed cost calculations, and today cockpit |
| TOS-TST-API-007 | test_tenants_rbac.py | Pytest integration tests for organization provisioning, invitations, and RBAC permissions |
| TOS-TST-API-008 | test_documents_shipments.py | Pytest integration tests for documents vault, compliance engine v2, and shipments |

---
*Auto-generated by update.py — do not edit manually.*
*Last updated: 2026-08-29T06:11:43Z*