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
        timeout=300.0
    )

    system_prompt = (
        "You are an Elite Enterprise B2B SaaS Chief Product Officer, Principal AI Systems Architect, "
        "and Global Leather Supply Chain Strategist. Provide practical, authoritative, and direct advice."
    )

    user_prompt = """
# MVP VALIDATION & EXECUTION ADVICE FOR BUTLER'S LEATHER (CHENNAI, INDIA)

## CONTEXT & TECH STACK DECISION
We are building the first commercial MVP of **Trade OS** specifically tailored for **Butler's Leather (Chennai, India)**.
The founder has locked in the core tech stack:
- **Frontend**: **React (Vite + Tailwind CSS + shadcn/ui)**
- **Backend / Database**: **PostgreSQL (with Medallion Schemas: Bronze/Silver/Gold + pgvector) + Python FastAPI**

We plan to implement the architecture, data processing, and matching methods outlined in our master specification: `trade_os_architecture_and_sprint_plan.md`.

---

## QUESTIONS FOR QWEN 3.8 MAX:

1. **Architecture & Scope Validation**:
   - Is implementing the Medallion Data Platform (Bronze, Silver, Gold) and data processing methods from `trade_os_architecture_and_sprint_plan.md` using **React + PostgreSQL** the right move for the Butler's Leather MVP?
   - How do we scope it so it does NOT become an over-engineered science project, but a lean, bulletproof, high-impact MVP ready in 7 to 10 days?

2. **Lean Data Processing Pipeline for Butler's Leather**:
   - How should the Medallion flow work specifically for Butler's Leather:
     - **Bronze**: How to store raw buyer data (German leather companies like Picard, Roeckl, Bader, Kilger, Otto Schumacher) + trade news/EUDR filings.
     - **Silver**: How to structure the canonical buyer profiles, materials, and compliance records.
     - **Gold**: How to compute the Match Score & Signals for Butler's Leather Chennai (Chennai export capabilities vs European demand).

3. **React Frontend MVP (The 3 Core Screens)**:
   - What are the exact component structures and API endpoints needed for:
     - Screen 1: Match Portal (Butler's capability card + 5 ranked European buyers)
     - Screen 2: Live Signals Feed (EUDR gap scorecard + freight benchmarks)
     - Screen 3: Account 360 & 1-Click Action (Outreach generation & CRM push)

4. **Critical Traps to Avoid During This Build**:
   - What should we explicitly NOT build in this MVP stage?
   - What is the fastest path from code to closing the $500 pilot with Butler's Leather?

Provide a concise, highly practical, and motivating masterclass execution guide.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print("Initiating streaming request to Qwen 3.8 Max for Butler's Leather React + Postgres MVP...")
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

    output_file = r"c:\Users\arsac\OneDrive\Documents\GitHub\Trade OS\docs\butlers_mvp_react_postgres_execution.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_content)

    print("\n\n--- Butler's MVP Execution Guide Completed Successfully ---")
    print(f"Total Content Characters: {len(full_content)}")
    print(f"Successfully saved to: {output_file}")

if __name__ == "__main__":
    main()
