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
        "You are an Elite B2B Enterprise SaaS Chief Product Officer and Global Leather Supply Chain Strategist. "
        "You provide deeply practical, concrete, and commercially lethal advice for building and selling a B2B Market Intelligence Prototype."
    )

    user_prompt = """
# CUSTOM PROTOTYPE SPECIFICATION & SALES DEMO PLAN: BUTLER'S LEATHER (CHENNAI, INDIA)

## 1. CLIENT CONTEXT
- **Company**: Butler's Leather
- **Location**: Chennai, Tamil Nadu, India (India's premier leather tanning and manufacturing hub — Ambur/Ranipet/Chennai cluster).
- **Business Model**: Manufacturer and exporter of finished leather, leather goods, and footwear components seeking expansion into premium German & European markets.
- **Target Buyers**: German and European leather goods brands, footwear manufacturers, saddleries, automotive interior suppliers, and wholesale leather distributors.

---

## 2. FOUNDER OBJECTIVE
I am building the first functional prototype of Trade OS tailored specifically for Butler's Leather Chennai as my first design partner / pilot customer. I want to build a prototype demo that delivers immediate, undeniable commercial value and converts Butler's Leather into my first paying client ($500 paid pilot / $950/mo subscription).

---

## 3. QUESTIONS FOR QWEN 3.8 MAX

Please provide a laser-focused, highly practical masterclass plan covering:

### PART A: THE EXACT PROTOTYPE ARCHITECTURE & SCREENS FOR BUTLER'S LEATHER
1. What exact 3 core views should the prototype show Butler's Leather when they log in?
   - Match Portal (Ranked European buyers tailored to Chennai export capabilities)
   - Live Signals Feed (EUDR compliance changes, trade show exhibits, European tenders)
   - Account 360 & 1-Click RFQ/CRM Push
2. What specific attributes of Butler's Leather (e.g. LWG certification, finished cow/goat leather, export port Chennai/Tuticorin, MOQ flexibility) should be parameterized in the matching engine?

### PART B: 5 CONCRETE EUROPEAN BUYER MATCHES TO SHOWCASE IN THE DEMO
Select 5 real, high-profile European/German target accounts (from our verified German/European dataset like Picard, Roeckl, Bader, Kilger, Otto Schumacher, etc.):
- Detail their specific buying demand (e.g. full-grain calfskin, vegetable-tanned lining, footwear uppers).
- Show the exact live signal / evidence why they are matched to Butler's Leather Chennai.
- Show the decision-maker contact title (Head of Sourcing, Procurement Lead) and recommended pitch angle.

### PART C: HIGH-VALUE "WOW" DATA POINTS SPECIFIC TO CHENNAI-TO-EUROPE TRADE
What unique data points will immediately convince Butler's Leather that this is not just another directory:
- EUDR (EU Deforestation Regulation) & EN 18199 compliance readiness mapping for Indian tanneries.
- Shipping trade lane intelligence (Chennai Port / JNPT to Hamburg / Rotterdam freight and transit times).
- Price index benchmarks (European wet-blue vs. Indian crust leather price spreads).
- Lineapelle Milan & APLF Hong Kong exhibitor intelligence on European competitors.

### PART D: THE 15-MINUTE DEMO SCRIPT & PAID PILOT CLOSE
1. Step-by-step 15-minute demo script for presenting the prototype to the CEO / Export Director of Butler's Leather Chennai.
2. The exact objection-handling script for common Indian leather exporter concerns (e.g. "We already use export agents", "We attend Lineapelle physically", "Will this guarantee orders?").
3. The exact closing pitch for the $500 Paid Pilot with the 14-day 5-qualified-match money-back guarantee.

Provide an exhaustive, concrete response formatted in clean Markdown.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print("Initiating streaming request to Qwen 3.8 Max for Butler's Leather Prototype...")
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

    output_file = r"c:\Users\arsac\.gemini\antigravity-ide\brain\a722a9e7-4a16-4187-aa07-0871743a7ffc\butlers_leather_prototype_and_demo_plan.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_content)

    print("\n\n--- Butler's Leather Prototype Plan Completed Successfully ---")
    print(f"Total Content Characters: {len(full_content)}")
    print(f"Successfully saved to: {output_file}")

if __name__ == "__main__":
    main()
