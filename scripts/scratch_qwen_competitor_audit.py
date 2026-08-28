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
        "You are an Elite Silicon Valley VC General Partner, Global Supply Chain Tech Analyst, "
        "and Veteran B2B Competitive Intelligence Strategist. You provide brutally honest, realistic, "
        "and deeply researched competitive market landscape assessments."
    )

    user_prompt = """
# BRUTAL COMPETITIVE AUDIT & UNIQUENESS ASSESSMENT: TRADE OS

## 1. FOUNDER QUESTION
"Is there any existing product that is actually doing my idea? Check latest AI news, B2B sales intelligence platforms, supply chain AI tools, Chinese trade intelligence platforms (like Tendata, 52wmb), and AI agent platforms. Tell me honestly: Is this a unique idea or not, and how can I win?"

---

## 2. OUR EXACT PRODUCT DEFINITION
- **Product**: Trade OS — a vertical B2B Market Intelligence & Decision Platform initially targeting the global leather, chemical, and raw material supply chains (MVP: Butler's Leather Chennai exporting finished cow/goat leather to Germany/Europe).
- **Core Value Loop**: Fuses multi-source signals (Trade manifest data / HS 4101-4107, Trade show exhibitors Lineapelle/ACLE, EUDR & REACH regulatory filings, commodity hide price indices) ➔ Computes an explainable 100-point Match Score ➔ Generates 1-click tailored B2B outreach and CRM actions.

---

## 3. AUDIT DIMENSIONS TO COVER (BE EXHAUSTIVE AND HONEST):

### PART 1: THE BRUTAL TRUTH ABOUT "UNIQUENESS"
1. Is the *concept* of "AI B2B Lead Gen / Market Intelligence" unique? (Give the honest reality check).
2. What part of our product is commoditized vs. what part is a genuine **vertical niche wedge**?

### PART 2: THE EXISTING COMPETITIVE LANDSCAPE (WHO IS ALREADY DOING SIMILAR THINGS?)
Analyze the 4 competitor tiers:
1. **The Customs & Trade Data Giants**:
   - Western: Panjiva (S&P Global), ImportGenius, Descartes Datamyne, Trademo, ImportYeti.
   - Enterprise Supply Chain Knowledge Graphs: Altana AI ($1B+ valuation), Sayari, Resilinc, Interos.
   - What are their strengths, and why are they failing small exporters like Butler's Leather?
2. **The Chinese B2B Trade & AI Platforms**:
   - Tendata (特易资讯), 52wmb (外贸邦), TradeInt, Alibaba International AI Supplier tools, Yuguo.
   - How do they use AI today, and what are their blindspots?
3. **The Horizontal AI Sales Agent & Intelligence Tools**:
   - Clay, Apollo.io, ZoomInfo, 6sense, 11x.ai (Alice), Artisan (Ava), Regie.ai.
   - Why can't a horizontal tool like Apollo or Clay easily replace Trade OS for an Indian leather exporter?
4. **The Incumbent Industry Directories**:
   - Leatherhead, World Leather, Lineapelle 365, APLF directory, Europages, Kompass.
   - Why are these dying or ineffective?

### PART 3: THE "WHITE SPACE" & OUR REAL DEFENSIBLE MOAT
1. Where exactly is the gap between the $50,000/yr enterprise tools (Altana/Panjiva) and the $50/mo generic databases (Apollo/Tendata)?
2. Why is **Verticalization in Leather / Raw Materials** (EUDR compliance scorecard, Chennai cluster hide specs, tannery chemistry, Lineapelle exhibitor tracking) the winning moat?

### PART 4: VERDICT & FOUNDER ACTION PLAN
1. Clear verdict: "Is this worth building, and can you make money?"
2. How should the founder position Trade OS when speaking to clients like Butler's Leather to ensure they never compare it to a cheap database?
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print("Initiating streaming request to Qwen 3.8 Max for Competitor Analysis...")
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

    output_file = r"c:\Users\arsac\OneDrive\Documents\GitHub\Trade OS\docs\competitor_analysis_and_uniqueness_audit.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_content)

    print("\n\n--- Competitor Audit Completed Successfully ---")
    print(f"Total Content Characters: {len(full_content)}")
    print(f"Successfully saved to: {output_file}")

if __name__ == "__main__":
    main()
