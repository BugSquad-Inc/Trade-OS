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
        "You are an Elite Enterprise B2B SaaS Chief Product Officer, Principal AI Solutions Architect, "
        "and Veteran Supply Chain Systems Engineer. You provide exhaustive, production-grade, highly structured, "
        "and immediately executable technical and business plans. Write in clear, authoritative, and comprehensive Markdown."
    )

    user_prompt = """
# MASTERCLASS ARCHITECTURE SPECIFICATION (HLD/LLD) & 4-WEEK SPRINT PLAN FOR TRADE OS

## CONTEXT & OBJECTIVE
Based on our previous strategic audit in `qwen_strategic_critique_and_roadmap.md`, we are transforming Trade OS from a simple developer scraper script into a high-value, un-cancelable **B2B Vertical Market Intelligence & Decision Platform** for the global leather, chemical, raw materials, and industrial supply chain market.

We need a complete, end-to-end, production-ready specification that provides:
1. **High-Level Design (HLD)**: System Context, Data Flow (Multi-Source Ingestion to Customer Decision), Component Topology.
2. **Low-Level Design (LLD)**:
   - Complete PostgreSQL Database Schema (Medallion: Bronze Raw Ingestion/Lineage, Silver Canonical Entities & Relationships, Gold Signals & Match Datamart).
   - Autonomous Agent Architecture (Deterministic State Machine with LangGraph/Python for Scout, Enricher, Resolver, Synthesizer).
   - Hybrid Search & Retrieval System (pgvector HNSW + BM25 FTS with Reciprocal Rank Fusion RRF).
   - Signal Detection & Diff Engine (AST/Text diff, hash tracking, event classifier).
   - Production FastAPI API Route Contracts & Schemas.
3. **Frontend Customer UX/UI Architecture**: Replacing developer sliders/logs with a high-converting Match Portal, Live Signals Feed, Account 360, and 1-Click RFQ/CRM Push.
4. **4-Week Immediate Business Impact Sprint Plan**: Day-by-day tasks, sprint milestones, Definition of Done (DoD), and commercial deliverables for Weeks 1 through 4.
5. **Founder Operations & GTM Playbook**: Legal/GDPR compliance checklist, Lead Magnet deployment, cold outreach templates, and exact strategy to close the first 3 paying customers ($500 - $1,500/mo).

Please deliver a comprehensive, masterclass-level blueprint covering all these sections thoroughly with concrete SQL schemas, Python signatures, JSON schemas, and architectural diagrams.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print("Initiating streaming request to Qwen 3.8 Max for Architecture & Sprint Plan...")
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

    output_file = r"c:\Users\arsac\.gemini\antigravity-ide\brain\a722a9e7-4a16-4187-aa07-0871743a7ffc\trade_os_architecture_and_sprint_plan.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_content)

    print("\n\n--- Architecture & Sprint Plan Completed Successfully ---")
    print(f"Total Content Characters: {len(full_content)}")
    print(f"Successfully saved to: {output_file}")

if __name__ == "__main__":
    main()
