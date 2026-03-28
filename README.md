# MSFoundryModelRouter

> **Microsoft Foundry — Intelligent Model Router**
> Route prompts dynamically across multiple LLMs based on task complexity, cost, and capability — powered by Azure AI Foundry.

---

## Overview

`MSFoundryModelRouter` demonstrates how to use **Azure AI Foundry's Model Router** to intelligently dispatch prompts to the most appropriate underlying model — without hardcoding a destination. A single router deployment inspects each request and selects the best-fit model (e.g. GPT-4o for reasoning, GPT-4o-mini for simple factual queries) transparently.

This reference implementation covers six real-world task categories and prints a full routing summary, showing which model was selected for each prompt, token usage, and overall model distribution.

---

## Architecture

```
Client (Python)
    │
    ▼
OpenAI SDK  ──►  MODEL_ROUTER_ENDPOINT  (Azure AI Foundry)
                        │
                        ├──► GPT-4o          (reasoning / coding)
                        ├──► GPT-4o-mini     (factual / summarisation)
                        ├──► GPT-4           (creative writing)
                        └──► ...             (extensible)
```

The router endpoint acts as a **single entry point**. It evaluates prompt characteristics at inference time and routes to the optimal model — no client-side logic required.

---

## Features

- **Automatic model selection** — router decides per-request; no hardcoded deployment per task
- **Six task categories** — factual, reasoning/coding, creative writing, data extraction, summarisation, multi-step reasoning
- **Token usage tracking** — prompt and completion tokens logged per call
- **Routing summary table** — tabular view of which model handled each task
- **Model distribution chart** — ASCII bar chart showing routing spread
- **Zero credential leakage** — all secrets via `.env`, never in code

---

## Prerequisites

- Python 3.10+
- Azure subscription with **Azure AI Foundry** access
- A **Model Router** deployment configured in your Foundry project
- `pip install openai python-dotenv`

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/praveen11singh/MSFoundryModelRouter.git
cd MSFoundryModelRouter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

```env
# .env
DEPLOYMENT_NAME=<your-model-router-deployment-name>
MODEL_ROUTER_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-azure-openai-key>
```

> **Important:** `DEPLOYMENT_NAME` must point to your **Model Router** deployment in Foundry — not a specific model like `gpt-4o`. The router deployment is what performs the dynamic dispatch.

### 4. Run the demo

```bash
python main.py
```

---

## Example Output

```
================================================================
  Microsoft Foundry — Model Router Multimodel Demo
================================================================

[1/6] Simple factual
  User: What is the capital of France?
  Router → gpt-4o-mini
  Tokens  prompt=18  completion=5
  Answer: The capital of France is Paris.

[2/6] Reasoning / coding
  User: Implement a thread-safe LRU cache in Python using OrderedDict...
  Router → gpt-4o
  Tokens  prompt=42  completion=310
  Answer: import threading...

...

================================================================
  Routing Summary
================================================================
  Task                      Model selected         In    Out
  ------------------------- -------------------- ------ ------
  Simple factual            gpt-4o-mini              18      5
  Reasoning / coding        gpt-4o                   42    310
  Creative writing          gpt-4o                   28    198
  Data extraction           gpt-4o-mini              35     42
  Summarisation             gpt-4o-mini              88     52
  Multi-step reasoning      gpt-4o                   55    175

  Model distribution:
    gpt-4o               ███ (3)
    gpt-4o-mini          ███ (3)
================================================================
```

---

## Project Structure

```
MSFoundryModelRouter/
├── main.py            # Entry point — runs all demo prompts
├── .env.example       # Environment variable template (safe to commit)
├── .gitignore         # Excludes .env and secrets
├── requirements.txt   # Python dependencies
└── README.md
```

---

## How the Router Works

When you call the router endpoint with a prompt, Foundry evaluates signals including:

| Signal | Examples |
|---|---|
| Prompt complexity | Token count, nested reasoning, code generation |
| Task type | Factual retrieval vs. creative vs. structured output |
| Cost optimisation | Simple queries routed to smaller, cheaper models |
| Latency requirements | Can be configured per deployment |

You do **not** need to implement any of this logic client-side. The router handles it transparently — your code stays clean and model-agnostic.

---

## Customising Prompts

Add your own prompt categories to `DEMO_PROMPTS` in `main.py`:

```python
{
    "label": "Your task label",
    "system": "Your system prompt.",
    "user": "Your user prompt here.",
},
```

---

## Part of the Microsoft Foundry Open-Source Series

This repo is one of a growing set of production-ready reference implementations:

| Repo | Focus |
|---|---|
| [MSFoundryAgentMemory](https://github.com/praveen11singh/MSFoundryAgentMemory) | Ephemeral, contextual & persistent memory patterns |
| [MSFoundryFunctionCall](https://github.com/praveen11singh/MSFoundryFunctionCall) | Auto & explicit function calling |
| [MSFoundryAgentImageInput](https://github.com/praveen11singh/MSFoundryAgentImageInput) | Multi-modal image input with agents |
| [MSFoundryEvaluation](https://github.com/praveen11singh/MSFoundryEvaluation) | Agent evaluation with azure-ai-evaluation |
| [MSFoundryRedTeam](https://github.com/praveen11singh/MSFoundryRedTeam) | Red team jailbreak probing & RAI evaluators |
| **MSFoundryModelRouter** | Dynamic multi-model routing ← you are here |

---

## Author

**Praveen Kumar**
Azure Solutions Architect & AI Engineer 

---

MIT License — see [LICENSE](LICENSE) for details.
