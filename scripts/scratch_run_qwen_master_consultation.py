import urllib.request
import json
import os
import sys

def main():
    api_key = "sk-62ZqYKHRUnesHSnxm00U04Ky87iF3RjLTyj5vlfdG3ydmHjK"
    url = "https://api.tokenrouter.com/v1/chat/completions"

    # Read existing architecture artifacts
    blueprint_path = r"c:\Users\arsac\.gemini\antigravity-ide\brain\a722a9e7-4a16-4187-aa07-0871743a7ffc\enterprise_data_intelligence_blueprint.md"
    missing_path = r"c:\Users\arsac\.gemini\antigravity-ide\brain\a722a9e7-4a16-4187-aa07-0871743a7ffc\missing_enterprise_elements.md"

    blueprint_content = open(blueprint_path, "r", encoding="utf-8").read() if os.path.exists(blueprint_path) else ""
    missing_content = open(missing_path, "r", encoding="utf-8").read() if os.path.exists(missing_path) else ""

    system_prompt = (
        "You are an Elite B2B SaaS Chief Product Officer, Principal AI Architect, and Global Supply Chain Data Strategist. "
        "Provide a world-class, rigorous, brutally honest, and deeply actionable audit and strategic execution plan for a founder building Trade OS."
    )

    user_prompt = f"""
# COMPREHENSIVE PROJECT AUDIT & STRATEGIC CONSULTATION REQUEST

## 1. FOUNDER PROFILE & SITUATION
I am building a B2B Market Intelligence Platform ('Trade OS') focused initially on the European & Global Leather / Raw Materials Industry. As a builder entering the advanced AI & data engineering space, I want an honest, deep, and actionable critique of what we have done, what is fundamentally flawed, what advanced AI/Data Engineering practices I should implement, who my paying customers are, and how to turn this into a profitable, highly feasible SaaS business.

---

## 2. WHAT WE HAVE BUILT & ACCOMPLISHED SO FAR
- **Tech Stack**: Python 3.11 + FastAPI + PostgreSQL (Psycopg 3 async) + React/Vite + TailwindCSS.
- **Scraping Engine**: 5-Tier Autonomous Scraper (`curl_cffi` Chrome TLS impersonation to bypass Cloudflare/WAF, Crawl4AI markdown conversion, disk caching, asyncio semaphores).
- **Data Ingestion**: Dynamic Excel parser (`openpyxl`) extracting company records even with merged title/header rows.
- **AI Router**: Multi-provider fallback router (`providers/router.py`) supporting NVIDIA NIM (Llama 3.3 70B), Google Gemini (15 RPM free tier), Groq, and Ollama, with SHA-256 deduplication hashing.
- **Accomplishments**: 
  - Verified 56 clean German leather companies (Bader, HELLER-LEDER, Josef Heinen, Südleder, Ludwig Perlinger, Weinheimer, ALVA Leather, BREE, etc.).
  - 100% byte-for-byte fidelity verified against live official websites.
  - Successfully bypassed Cloudflare 403 on protected luxury domains (e.g. AIGNER Munich).

---

## 3. IDENTIFIED PRODUCT FAILURES (THE POST-MORTEM)
1. **Scraper Script != SaaS Product**: Our UI was an internal developer dashboard (worker sliders, raw logs) rather than a customer-facing match portal.
2. **The 1-Month Cancellation Trap**: Selling a static directory of 56 companies means clients export the Excel file on Day 1 and cancel on Day 2. There is no recurring value hook.
3. **Generic Emails ($0 Value)**: Scraped `info@` or `sales@` emails are useless; B2B clients need verified decision-maker names (Head of Procurement, VP of Supply Chain) with LinkedIn profiles.
4. **Stale Single-Source Data**: Traditional tanneries update their websites once every 3-5 years. Relying on website HTML alone yields stale, minimal data.

---

## 4. OUR PROPOSED BLUEPRINT & MISSING ELEMENTS
Enterprise Data Intelligence Blueprint:
\"\"\"
{blueprint_content[:2500]}
\"\"\"

Missing Enterprise Elements Identified:
\"\"\"
{missing_content[:2500]}
\"\"\"

---

## 5. STRATEGIC & ARCHITECTURAL QUESTIONS FOR YOU (QWEN 3.8 MAX)

Please provide an in-depth, structured master consultation covering:

### PART 1: COMPLETE RE-APPROACH OR ENHANCEMENT?
1. Is our pivot toward a **Medallion Data Lake (Bronze/Silver/Gold) + Multi-Source Signal Engine** the right move, or is a fundamentally different approach needed?
2. What are we doing technically wrong or over-engineering at this stage?

### PART 2: SOLVING THE 'SPARSE DATA' CHALLENGE IN INDUSTRIAL NICHES
1. Since company websites in traditional industries (like leather) have minimal and rarely updated data, how exactly should we combine:
   - Customs Manifest / Bill of Lading (BOL) shipment records
   - Live Trade Show & Expo exhibitor data (Lineapelle Milan, ACLE Shanghai, APLF)
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

Provide a comprehensive, masterclass-level response formatted in clean Markdown.
"""

    payload = {
        "model": "qwen/qwen3.8-max-free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print("Sending comprehensive consultation request to Qwen 3.8 Max...")
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            msg = data["choices"][0]["message"]
            content = msg.get("content") or msg.get("reasoning_content") or ""

            output_file = r"c:\Users\arsac\.gemini\antigravity-ide\brain\a722a9e7-4a16-4187-aa07-0871743a7ffc\qwen_strategic_critique_and_roadmap.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Successfully received and saved response to {output_file}!")
            print(f"Total characters: {len(content)}")
    except Exception as e:
        print("Error calling Qwen API:", e)

if __name__ == "__main__":
    main()
