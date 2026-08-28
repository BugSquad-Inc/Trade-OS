"""
Trade OS — Qwen 3.8 Max Query & Streaming CLI Tool
Usage:
    python scripts/ask_qwen.py "Your strategic or technical question here"
    python scripts/ask_qwen.py --file prompt.txt --out response.md
    python scripts/ask_qwen.py  (Interactive mode)
"""

import os
import sys
import argparse
from pathlib import Path
from openai import OpenAI

def load_api_key():
    # 1. Check environment variable
    if os.getenv("TOKEN_ROUTER"):
        return os.getenv("TOKEN_ROUTER")
    
    # 2. Check .env in current directory or parent directory
    env_paths = [
        Path(".env"),
        Path("../.env"),
        Path(__file__).resolve().parent.parent / ".env"
    ]
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("TOKEN_ROUTER="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    
    # 3. Fallback to hardcoded TokenRouter key
    return "sk-62ZqYKHRUnesHSnxm00U04Ky87iF3RjLTyj5vlfdG3ydmHjK"

def ask_qwen(prompt: str, system_prompt: str = None, output_file: str = None):
    # Configure UTF-8 for Windows console
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    api_key = load_api_key()
    if not api_key:
        print("❌ Error: TOKEN_ROUTER API key not found in .env or environment.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        base_url="https://api.tokenrouter.com/v1",
        api_key=api_key,
        timeout=360.0
    )

    if not system_prompt:
        system_prompt = (
            "You are an Elite Enterprise B2B SaaS Chief Product Officer, Principal Solutions Architect, "
            "and Global Supply Chain Strategist for Trade OS. Provide direct, exhaustive, highly structured, "
            "and actionable advice formatted in clean Markdown."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    print(f"\n🚀 Sending request to Qwen 3.8 Max (TokenRouter)...\n" + "-"*60 + "\n")

    stream = client.chat.completions.create(
        model="qwen/qwen3.8-max-free",
        messages=messages,
        stream=True,
        stream_options={"include_usage": True}
    )

    content_parts = []
    reasoning_parts = []

    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            # Capture reasoning content if available
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_parts.append(delta.reasoning_content)
            # Capture content and stream live to stdout
            if hasattr(delta, "content") and delta.content:
                content_parts.append(delta.content)
                sys.stdout.write(delta.content)
                sys.stdout.flush()

    full_content = "".join(content_parts)
    if not full_content and reasoning_parts:
        full_content = "".join(reasoning_parts)
        sys.stdout.write(full_content)
        sys.stdout.flush()

    print("\n\n" + "-"*60 + "\n✅ Response Completed.")

    if output_file:
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"📁 Response successfully saved to: {out_path.resolve()}")

def main():
    parser = argparse.ArgumentParser(description="Query Qwen 3.8 Max via TokenRouter API")
    parser.add_argument("query", nargs="*", help="Query string to send to Qwen")
    parser.add_argument("--file", "-f", help="Read prompt from a file")
    parser.add_argument("--out", "-o", help="Save response to a Markdown file")
    parser.add_argument("--system", "-s", help="Custom system prompt")

    args = parser.parse_args()

    prompt = ""
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            prompt = f.read()
    elif args.query:
        prompt = " ".join(args.query)
    else:
        print("💬 Enter your question for Qwen 3.8 Max (Press Enter, then Ctrl+Z / Ctrl+D to submit):\n")
        prompt = sys.stdin.read().strip()

    if not prompt:
        print("❌ Error: No prompt provided.", file=sys.stderr)
        sys.exit(1)

    ask_qwen(prompt=prompt, system_prompt=args.system, output_file=args.out)

if __name__ == "__main__":
    main()
