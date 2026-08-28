# Trade OS — Documentation Index & Architecture Map

> **Master Reference Manual:** [\MASTER_ULTIMATE_EXECUTION_AND_SCALING_PLAN.md\](./MASTER_ULTIMATE_EXECUTION_AND_SCALING_PLAN.md)  
> **Active Sprint Execution Plan:** [\../implementation_plan_v2.md\](../implementation_plan_v2.md)

---

## 1. Master Strategic Reference

| Document | Purpose & Scope | Status |
|---|---|---|
| [\MASTER_ULTIMATE_EXECUTION_AND_SCALING_PLAN.md\](./MASTER_ULTIMATE_EXECUTION_AND_SCALING_PLAN.md) | **The Single Source of Truth.** Master execution manual detailing the vertical revenue OS category, defensible wedge, 100-point scoring formula, medallion schema, 3-screen workflow, 8-day sprint roadmap, and enterprise scaling plan. | **Approved / Canonical** |
| [\MASTER_PROTOTYPE_EXECUTION_AND_SCALING_PLAN.md\](./MASTER_PROTOTYPE_EXECUTION_AND_SCALING_PLAN.md) | Original master prototype roadmap (superseded by ULTIMATE). | Historical Reference |

---

## 2. Architecture & Technical Specifications

| Document | Purpose & Scope | Status |
|---|---|---|
| [\	rade_os_architecture_and_sprint_plan.md\](./trade_os_architecture_and_sprint_plan.md) | Comprehensive system architecture, PostgreSQL medallion DDL definitions, indexing strategies, API contracts, and non-functional requirements. | Active Reference |
| [\utlers_mvp_react_postgres_execution.md\](./butlers_mvp_react_postgres_execution.md) | MVP execution guardrails, API response shapes, and component wireframe definitions. | Active Reference |
| [\enterprise_data_intelligence_blueprint.md\](./enterprise_data_intelligence_blueprint.md) | Enterprise data architecture, entity resolution pipelines, and multi-source fusion mechanics. | Phase 2/3 Reference |
| [\multi_source_intelligence_strategy.md\](./multi_source_intelligence_strategy.md) | Strategy for ingesting trade shows, regulatory filings, customs BOL, and freight indicators. | Phase 2 Reference |
| [\missing_enterprise_elements.md\](./missing_enterprise_elements.md) | Checklist of 7 enterprise requirements (GDPR Legitimate Interest, BOL data, ERP 2-way sync, PLG hooks). | Active Reference |

---

## 3. Customer Wedge, Demo & Commercial Strategy

| Document | Purpose & Scope | Status |
|---|---|---|
| [\utlers_leather_prototype_and_demo_plan.md\](./butlers_leather_prototype_and_demo_plan.md) | Butler's Leather factory capability specs, 5 German buyer dossiers (*Picard, Roeckl, Bader, Kilger, Otto Schumacher*), EUDR 68/100 audit, freight corridors, and 15-min sales demo script. | Active Reference |
| [\competitor_analysis_and_uniqueness_audit.md\](./competitor_analysis_and_uniqueness_audit.md) | Competitive moat analysis against Apollo, Panjiva, Altana AI, Lineapelle, and commodity customs directories. | Active Reference |
| [\product_reality_check_roast.md\](./product_reality_check_roast.md) | Critical failure mode audit: anti-scraping traps, fake AI hallucination prevention, one-month churn trap mitigation, and GDPR compliance. | Active Reference |
| [\qwen_strategic_critique_and_roadmap.md\](./qwen_strategic_critique_and_roadmap.md) | Deep strategic critique and architecture audit recommendations. | Active Reference |
| [\rainstorm_trade_os_roadmap.md\](./brainstorm_trade_os_roadmap.md) | Initial brainstorming roadmap. | Historical Reference |

---

## 4. Documentation Hierarchy & Decision Rules

1. When in doubt regarding **strategy, commercial terms, or scoring weights**, consult [\MASTER_ULTIMATE_EXECUTION_AND_SCALING_PLAN.md\](./MASTER_ULTIMATE_EXECUTION_AND_SCALING_PLAN.md).
2. For **active day-by-day implementation**, consult [\../implementation_plan_v2.md\](../implementation_plan_v2.md).
3. All code modifications must follow the structured memory rules in [\../ai_context/RULES.md\](../ai_context/RULES.md) and assign codes via [\../CODEMAP.json\](../CODEMAP.json).
