import urllib.request
import json
import time
import sys

api_key = "sk-62ZqYKHRUnesHSnxm00U04Ky87iF3RjLTyj5vlfdG3ydmHjK"
url = "https://api.tokenrouter.com/v1/chat/completions"

with open("scripts/prompt_qwen_business_audit.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

system_prompt = (
    "You are an Elite B2B SaaS Chief Product Officer, Principal Solutions Architect, "
    "and Global Supply Chain Commercial Strategist for Trade OS. Provide direct, exhaustive, highly structured, "
    "and actionable advice formatted in clean Markdown."
)

payload = {
    "model": "qwen/qwen3.8-max-free",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.3,
    "max_tokens": 4096
}

data = json.dumps(payload).encode("utf-8")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("Connecting to Qwen 3.8 Max (TokenRouter)...")
for attempt in range(1, 6):
    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            content = res_json["choices"][0]["message"]["content"]
            with open("docs/qwen_business_readiness_audit.md", "w", encoding="utf-8") as out_f:
                out_f.write(content)
            print("[SUCCESS] Qwen 3.8 Max response saved to docs/qwen_business_readiness_audit.md!")
            print("\n--- SNIPPET OF QWEN RESPONSE ---\n")
            print(content[:1500])
            break
    except Exception as e:
        print(f"[Attempt {attempt}/5] Error: {e}. Retrying in {attempt * 3}s...")
        time.sleep(attempt * 3)
