import os
import sys
from openai import OpenAI

def main():
    # Configure UTF-8 for Windows console
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    api_key = "sk-62ZqYKHRUnesHSnxm00U04Ky87iF3RjLTyj5vlfdG3ydmHjK"
    
    client = OpenAI(
        base_url="https://api.tokenrouter.com/v1",
        api_key=api_key,
        timeout=300.0
    )

    system_prompt = (
        "You are an Elite B2B SaaS Chief Product Officer, Principal AI Architect, and Global Supply Chain Data Strategist. "
        "Provide a direct, exhaustive, highly structured, and brutally honest masterclass audit and strategic execution plan for a founder building Trade OS. "
        "Begin your response directly with the masterclass markdown analysis."
    )

    user_prompt = """
# COMPREHENSIVE PROJECT AUDIT & STRATEGIC CONSULTATION REQUEST: B2B TRADE OS

## 1. FOUNDER CONTEXT & CURRENT STATUS
I am building a B2B Market Intelligence Platform ('Trade OS') focused initially on the European & Global Leather / Raw Materials Industry. I am a builder entering the advanced AI & data engineering space. I want a brutal, honest, and actionable critique of what we have done, what is fundamentally flawed, what advanced AI/Data Engineering practices to implement, who my paying customers are, and how to turn this into a profitable business with high market feasibility.

### What We Have Built So Far:
- **Tech Stack**: Python 3.11 + FastAPI + PostgreSQL (Psycopg 3 async) + React/Vite.
- **Scraping Engine**: 5-Tier Autonomous Scraper (`curl_cffi` Chrome TLS impersonation to bypass Cloudflare/WAF, Crawl4AI markdown conversion, disk caching, asyncio semaphores).
- **Data Ingestion**: Dynamic Excel parser (`openpyxl`) extracting company records with dynamic header row detection.
- **AI Router**: Multi-provider fallback router (`providers/router.py`) supporting NVIDIA NIM (Llama 3.3 70B), Google Gemini (15 RPM free tier), Groq, and Ollama, with SHA-256 deduplication hashing.
- **Accomplishments**: 
  - Verified 56 clean German leather companies (Bader, HELLER-LEDER, Josef Heinen, Südleder, Ludwig Perlinger, Weinheimer, ALVA Leather, BREE, etc.).
  - 100% byte-for-byte fidelity verified against live official websites.
  - Successfully bypassed Cloudflare 403 on protected luxury domains (e.g. AIGNER Munich).

### Identified Product Failures (The Post-Mortem):
1. **Scraper Script != SaaS Product**: Our UI was an internal developer dashboard (worker sliders, raw logs) rather than a customer-facing match portal.
2. **The 1-Month Cancellation Trap**: Selling a static directory of 56 companies means clients export the Excel file on Day 1 and cancel on Day 2. There is no recurring value hook.
3. **Generic Emails ($0 Value)**: Scraped `info@` or `sales@` emails are useless; B2B clients need verified decision-maker names (Head of Procurement, VP of Supply Chain) with LinkedIn profiles.
4. **Stale Single-Source Data**: Traditional tanneries update their websites once every 3-5 years. Relying on website HTML alone yields stale, minimal data.

---

## 2. STRATEGIC & ARCHITECTURAL QUESTIONS FOR YOU (QWEN 3.8 MAX)

Please provide an in-depth, structured master consultation covering:

### PART 1: COMPLETE RE-APPROACH OR ENHANCEMENT?
1. Is our pivot toward a **Medallion Data Lake (Bronze/Silver/Gold) + Multi-Source Signal Engine** the right move, or is a fundamentally different approach needed?
2. What are we doing technically wrong or over-engineering at this stage?

### PART 2: SOLVING THE 'SPARSE DATA' CHALLENGE IN INDUSTRIAL NICHES
1. Since company websites in traditional industries (like leather) have minimal and rarely updated data, how exactly should we combine:
   - Customs Manifest / Bill of Lading (BOL) shipment records
   - Live Trade Show & Expo exhibitor data (Lineapelle Milan, ACLE Shanghai, APLF Hong Kong)
   - Daily trade news & regulatory filings (EUDR, REACH, EN 18199)
   - Commodity raw hide price indices (US Heavy Native Steers, European wet-blue)
2. What are the best free/low-cost or scrapable data sources for international trade & customs data?

### PART 3: ADVANCED AI & AGENTIC IMPLEMENTATION (THE STATE OF THE ART)
1. How should we implement **Autonomous AI Agents** (using frameworks like LangGraph, CrewAI, or AutoGen) to automate:
   - An *Intelligence Scout Agent* (crawling news, expos, and manifests daily)
   - An *Entity Resolution & Enrichment Agent* (validating decision-makers, email pinging, deduplication)
   - A *Synthesis & Briefing Agent* (generating client-specific Monday Morning intelligence briefs)?
2. How can we implement **GraphRAG** and **Hybrid Search (BM25 + Dense Vectors)** in practice with PostgreSQL (`pgvector`) or Neo4j without astronomical costs?
3. How can we integrate real-time web search / Grok-style search grounding into the pipeline?

### PART 4: TARGET CUSTOMERS, VALUE PROPOSITION & MONETIZATION
1. Who are the real high-paying buyers for this data?
   - Global automotive OEMs (BMW, Mercedes, Audi leather procurement)
   - Luxury fashion & footwear brands (LVMH, Kering, Prada, Hugo Boss)
   - Raw hide & wet-blue commodity traders & brokers
   - Chemical & tanning machinery suppliers (BASF, Stahl, TFL)
   - International finished leather exporters (like our case study client 'Butler's Leather')?
2. How should we price and package this:
   - Tier 1: Directory & Compliance Lookup ($199/mo)
   - Tier 2: Live Market Intelligence & ICP Matcher ($499/mo)
   - Tier 3: Enterprise Supply Chain & Customs Manifest Tracking ($1,500 - $3,000/mo)?
3. What Product-Led Growth (PLG) lead magnets will attract enterprise procurement leads for $0 CAC?

### PART 5: CONCRETE STEP-BY-STEP ROADMAP FOR A BEGINNER-TO-REVENUE BUILDER
Give me a clear, prioritized 4-week execution roadmap:
- Week 1: Core Data Lake & Multi-Source Pipelines
- Week 2: AI Entity Resolution & Enrichment
- Week 3: Frontend Product UI (Transforming Admin tool into Customer Match Portal)
- Week 4: GTM, Lead Magnets, and First Paying Client Acquisition.

Provide a comprehensive, masterclass-level response.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print("Initiating streaming call to Qwen 3.8 Max on TokenRouter...")
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
            # Capture reasoning content
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_parts.append(delta.reasoning_content)
            # Capture final answer content
            if hasattr(delta, "content") and delta.content:
                content_parts.append(delta.content)

    full_content = "".join(content_parts)
    if not full_content and reasoning_parts:
        full_content = "".join(reasoning_parts)

    output_file = r"c:\Users\arsac\.gemini\antigravity-ide\brain\a722a9e7-4a16-4187-aa07-0871743a7ffc\qwen_strategic_critique_and_roadmap.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_content)

    print("\n\n--- Stream Completed Successfully ---")
    print(f"Total Content Characters: {len(full_content)}")
    print(f"Master consultation successfully saved to: {output_file}")

if __name__ == "__main__":
    main()
