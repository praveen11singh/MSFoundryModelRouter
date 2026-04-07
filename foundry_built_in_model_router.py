import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


DEPLOYMENT = os.environ["DEPLOYMENT_NAME"]

client = OpenAI(
    base_url=os.environ["MODEL_ROUTER_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# ── Demo prompts designed to trigger different models ─────────────────────────

PK_DEMO_PROMPTS = [
    {
        "label": "Simple factual",
        "system": "You are a helpful assistant.",
        "user": "What is the capital of India?",
    },
    {
        "label": "Reasoning / coding",
        "system": "You are an expert Python engineer.",
        "user": (
            "Implement a thread-safe LRU cache in Python using OrderedDict. "
            "Include get, put, and a brief explanation of the locking strategy."
        ),
    },
    {
        "label": "Creative writing",
        "system": "You are a creative writing assistant.",
        "user": "Write a two-paragraph short story about an astronaut who discovers a library on Mars.",
    },
    {
        "label": "Data extraction",
        "system": "Extract structured data. Reply only with JSON.",
        "user": (
            "Extract name, role, and company from: "
            "'Hi, I'm Sarah Chen, a senior data scientist at Contoso Analytics.'"
        ),
    },
    {
        "label": "Summarisation",
        "system": "You are a concise summariser. Reply in 2-3 sentences.",
        "user": (
            "Summarise: Retrieval-Augmented Generation (RAG) combines a retrieval system "
            "with a generative model. The retriever fetches relevant documents from a corpus, "
            "and the generator uses those documents as grounded context to produce accurate, "
            "source-backed answers — reducing hallucinations compared to vanilla LLMs."
        ),
    },
    {
        "label": "Multi-step reasoning",
        "system": "Think step by step.",
        "user": (
            "A train leaves London at 09:00 travelling at 120 mph. "
            "Another leaves Edinburgh (400 miles away) at 10:00 travelling at 80 mph toward London. "
            "At what time do they meet, and how far from London?"
        ),
    },
]


# ── Runner ────────────────────────────────────────────────────────────────────

def pk_run_demo(prompts: list[dict]) -> None:
    print("=" * 64)
    print("  Microsoft Foundry — Model Router Multimodel Demo")
    print("=" * 64)

    results = []

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] {prompt['label']}")
        print(f"  User: {prompt['user'][:80]}{'...' if len(prompt['user']) > 80 else ''}")

        try:
            completion = client.chat.completions.create(
                model=DEPLOYMENT,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user",   "content": prompt["user"]},
                ],
                max_tokens=512,
            )

            content      = completion.choices[0].message.content
            model_used   = completion.model
            prompt_toks  = completion.usage.prompt_tokens
            output_toks  = completion.usage.completion_tokens

            print(f"  Router → {model_used}")
            print(f"  Tokens  prompt={prompt_toks}  completion={output_toks}")
            print(f"  Answer: {content[:200]}{'...' if len(content) > 200 else ''}")

            results.append({
                "label":      prompt["label"],
                "model":      model_used,
                "prompt_tok": prompt_toks,
                "output_tok": output_toks,
            })

        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"label": prompt["label"], "model": "error", "prompt_tok": 0, "output_tok": 0})

    # ── Summary table ─────────────────────────────────────────────────────────
    print("\n" + "=" * 64)
    print("  Routing Summary")
    print("=" * 64)
    print(f"  {'Task':<25} {'Model selected':<20} {'In':>6} {'Out':>6}")
    print(f"  {'-'*25} {'-'*20} {'-'*6} {'-'*6}")
    for r in results:
        print(f"  {r['label']:<25} {r['model']:<20} {r['prompt_tok']:>6} {r['output_tok']:>6}")

    # model distribution
    from collections import Counter
    dist = Counter(r["model"] for r in results if r["model"] != "error")
    print("\n  Model distribution:")
    for model, count in dist.most_common():
        bar = "█" * count
        print(f"    {model:<20} {bar} ({count})")

    print("=" * 64)


if __name__ == "__main__":
    pk_run_demo(PK_DEMO_PROMPTS)


