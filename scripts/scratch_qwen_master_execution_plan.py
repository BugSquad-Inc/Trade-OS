import os
import sys
from openai import OpenAI

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    api_key = "sk-62ZqYKHRUnesHSnxm00U04Ky87iF3RjLTyj5vlfdG3ydmHjK"
    
    client = OpenAI(
        base_url="https://api.tokenrouter.com/v1",
        api_key=api_key,
        timeout=360.0
    )

    system_prompt = (
        "You are an Elite Enterprise B2B SaaS Chief Product Officer, Principal Solutions Architect, "
        "and Serial Founder who has scaled vertical B2B intelligence platforms from $0 to $10M ARR. "
        "Provide an authoritative, exhaustive, step-by-step master execution plan that links code directly to revenue."
    )

    user_prompt = """
# MASTER PROTOTYPE EXECUTION, IMMEDIATE VALIDATION & FUTURE SCALING PLAN: TRADE OS (BUTLER'S LEATHER CHENNAI)

## 1. CONTEXT & SYNTHESIS OBJECTIVE
Synthesizing all our strategic, architectural, and operational blueprints (`butlers_mvp_react_postgres_execution.md`, `butlers_leather_prototype_and_demo_plan.md`, `trade_os_architecture_and_sprint_plan.md`, and `qwen_strategic_critique_and_roadmap.md`), we need a unified, end-to-end master execution plan for building the complete prototype in the clean workspace `Trade OS`.

### Tech Stack Locked:
- **Frontend**: React (Vite + Tailwind CSS + Lucide Icons + shadcn/ui)
- **Backend**: Python 3.11 + FastAPI + PostgreSQL (Lean Medallion schemas: `bronze`, `silver`, `gold`)
- **Initial Target**: Butler's Leather (Chennai, India) exporting finished cow/goat leather to Germany/Europe.
- **Immediate Commercial Goal**: $500 Paid Pilot with 14-day 5-qualified-match guarantee ➔ Convert to $950/mo subscription.

---

## 2. MASTER PLAN REQUIREMENTS FOR QWEN 3.8 MAX:

Please produce an exhaustive, production-grade master plan covering:

### SECTION 1: END-TO-END PROTOTYPE ARCHITECTURE & CODEBASE BLUEPRINT
1. Exact file and directory structure for `Trade OS/` (`backend/` and `frontend/`).
2. Exact PostgreSQL DDL for the 3 schemas (`bronze`, `silver`, `gold`) scoped cleanly for Butler's Leather.
3. The exact FastAPI endpoint contracts (`/api/v1/matches`, `/api/v1/signals`, `/api/v1/accounts/{id}`, `/api/v1/outreach`, `/api/v1/health`).
4. The exact React component tree for the 3 core views (Match Portal, Live Signals Feed, Account 360 & 1-Click Action).

### SECTION 2: 7-DAY DAY-BY-DAY EXECUTION SPRINT (CODE TO DEMO)
Provide an exact day-by-day task checklist with:
- **Daily Objective**
- **Exact Code/Files Created**
- **Database/Data Seed Action**
- **Definition of Done (DoD)**
- **End-of-Day Deliverable**

### SECTION 3: COMMERCIAL VALIDATION & SALES DEMO REHEARSAL
1. Pre-demo verification checklist (verifying the 5 buyer dossiers: Picard, Roeckl, Bader, Kilger, Otto Schumacher).
2. The 15-Minute Live Sales Demo Script tailored for the CEO/Export Director of Butler's Leather Chennai.
3. The exact Closing Pitch for the $500 Paid Pilot (with written 14-day 5-match refund criteria).
4. Handling the 4 biggest exporter objections in real time.

### SECTION 4: FUTURE SCALING & POST-MVP ROADMAP (PHASE 2 & PHASE 3)
1. **Week 2–4 (Scaling to 3–5 Design Partners)**:
   - Onboarding chemical distributors (e.g. Stahl, BASF) and leather machinery vendors.
   - Transitioning from scripted/manual seed data to automated scraping & RSS ingestion.
2. **Month 2–3 (Activating Enterprise Intelligence)**:
   - Activating `pgvector` HNSW dense search + BM25 hybrid retrieval.
   - Integrating customs manifest (Bill of Lading) data flows.
   - Autonomous LangGraph agent workflows (Scout, Enricher, Resolver, Synthesizer).
   - Packaging the $2,500/mo Enterprise Tier.

Format this as an exhaustive, executive-level markdown document that serves as the permanent build-and-scale manual for Trade OS.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print("Initiating streaming request to Qwen 3.8 Max for Master Execution & Scaling Plan...")
    stream = client.chat.completions.create(
        model="qwen/qwen3.8-max-free",
        messages=messages,
        stream=True,
        stream_options={"include_usage": True}
    )

    reasoning_parts = []
    content_parts = []

    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_parts.append(delta.reasoning_content)
            if hasattr(delta, "content") and delta.content:
                content_parts.append(delta.content)

    full_content = "".join(content_parts)
    if not full_content and reasoning_parts:
        full_content = "".join(reasoning_parts)

    output_file = r"c:\Users\arsac\OneDrive\Documents\GitHub\Trade OS\docs\MASTER_PROTOTYPE_EXECUTION_AND_SCALING_PLAN.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_content)

    print("\n\n--- Master Plan Completed Successfully ---")
    print(f"Total Content Characters: {len(full_content)}")
    print(f"Successfully saved to: {output_file}")

if __name__ == "__main__":
    main()
