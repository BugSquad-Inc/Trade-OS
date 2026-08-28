import os
import sys
import time
from openai import OpenAI

api_key = "sk-62ZqYKHRUnesHSnxm00U04Ky87iF3RjLTyj5vlfdG3ydmHjK"
client = OpenAI(
    base_url="https://api.tokenrouter.com/v1",
    api_key=api_key,
    timeout=60.0
)

with open("scripts/prompt_qwen_business_audit.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

system_prompt = (
    "You are an Elite B2B SaaS Chief Product Officer, Principal Solutions Architect, "
    "and Global Supply Chain Commercial Strategist for Trade OS. Provide direct, exhaustive, highly structured, "
    "and actionable advice formatted in clean Markdown."
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
]

print("Connecting and streaming from Qwen 3.8 Max...")
for attempt in range(1, 6):
    try:
        stream = client.chat.completions.create(
            model="qwen/qwen3.8-max-free",
            messages=messages,
            stream=True,
            temperature=0.3
        )
        content_parts = []
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                content_parts.append(text)
                sys.stdout.write(text)
                sys.stdout.flush()
        
        full_text = "".join(content_parts)
        if full_text:
            with open("docs/qwen_business_readiness_audit.md", "w", encoding="utf-8") as f_out:
                f_out.write(full_text)
            print("\n\n[SUCCESS] Saved to docs/qwen_business_readiness_audit.md!")
            break
    except Exception as e:
        print(f"\n[Attempt {attempt}/5] Error: {e}. Retrying in {attempt * 2}s...", file=sys.stderr)
        time.sleep(attempt * 2)
