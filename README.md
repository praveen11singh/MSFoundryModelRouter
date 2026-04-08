# MSFoundryModelRouter

> **Microsoft Foundry Open-Source Series · Intelligent Model Router**
> Route prompts dynamically across multiple LLMs — by task complexity, cost, and capability — through a single Azure AI Foundry endpoint.
---

## Overview

`MSFoundryModelRouter` demonstrates how to use **Azure AI Foundry's built-in Model Router** to intelligently dispatch prompts to the most appropriate underlying model — without any hardcoded model selection in your application code.

A single router deployment analyses each incoming request and selects the best-fit model transparently, optimising across three configurable routing modes:

| Routing Mode | Behaviour |
|---|---|
| **Balanced** *(default)* | Balances quality, cost, and latency for general-purpose workloads |
| **Quality** | Always selects the highest-capability model regardless of cost |
| **Cost** | Aggressively routes to the smallest sufficient model to minimise spend |

This reference implementation exercises **six real-world task categories** and prints a full routing summary — showing which model was selected per prompt, token usage, and overall model distribution.

---

## Architecture

```
  Your Application
        │
        │  Single endpoint call
        ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                    Azure AI Foundry                         │
  │                                                             │
  │   ┌─────────────────────────────────────────────────────┐   │
  │   │               Model Router Deployment               │   │
  │   │                                                     │   │
  │   │   Routing Mode:  Balanced | Quality | Cost          │   │
  │   │   Deployment:    Global Standard | Data Zone Std    │   │
  │   │   Model Scope:   All supported | Custom subset      │   │
  │   └───────────────────────┬─────────────────────────────┘   │
  │                           │ classifies per-request          │
  │              ┌────────────┼─────────────────┐               │
  │              │            │                 │               │
  │              ▼            ▼                 ▼               │
  │         o4-mini      gpt-4.1-mini     gpt-4o-mini           │
  │         (reasoning)  (complex tasks)  (creative/fast)       │
  │              │            │                 │               │
  │              └────────────┴────────────┬────┘               │
  │                                        │ automatic failover │
  │                                        ▼                    │
  │                              Streaming Response             │
  └─────────────────────────────────────────────────────────────┘
```

The router endpoint is a **single entry point** for your application. It classifies each request and dispatches to the optimal model — no client-side routing logic required. All routes return a standard streaming-compatible response.

### Deployment Options

**Deployment Type** — choose based on your data residency and compliance requirements:

| Deployment Type | Description |
|---|---|
| **Global Standard** | Routes across Azure's global infrastructure for maximum availability and throughput |
| **Data Zone Standard** | Keeps data within a specific Azure geography for compliance and data residency requirements |

**Model Scope** — control which models the router can dispatch to:

| Model Scope | Description |
|---|---|
| **Route to all supported models** | Router selects from the full catalogue; includes automatic failover across all models |
| **Route to a subset of models** | Restrict routing to a specific list of approved deployments for cost control or compliance |

---

## Features

- **Three routing modes** — Balanced (default), Quality, and Cost to match your workload priorities
- **Flexible deployment types** — Global Standard or Data Zone Standard for compliance requirements
- **Full or subset model routing** — route to all supported models or restrict to an approved list
- **Automatic failover** — built-in transparent failover when routing to all supported models
- **Automatic model selection** — the router decides per-request; no hardcoded deployment per task type
- **Six task categories** — factual, reasoning/coding, creative writing, data extraction, summarisation, multi-step reasoning
- **Token usage tracking** — prompt and completion tokens logged for every call
- **Routing summary table** — tabular view of which model handled each task with token counts
- **Model distribution chart** — ASCII bar chart showing routing spread across the run
- **Zero credential leakage** — all configuration via `.env`, never hardcoded

---

## Why Use Model Router?

Model Router optimises costs and latencies while maintaining comparable quality. Smaller, cheaper models are used when they're sufficient for the task; larger, more expensive models are available for complex tasks. Reasoning models are selected when the task requires complex reasoning; non-reasoning models are used otherwise.

Model Router provides a **single deployment and chat experience** that combines the best features from all underlying chat models — without requiring any changes to your application code when new models are added to the catalogue.

---

## Supported Models

> `*` Available in Global Standard deployments only.
> `**` Available for subset routing only (cannot be used as a standalone deployment target).

| Model | Notes |
|---|---|
| `gpt-5` | `*` |
| `gpt-5-mini` | |
| `gpt-5-nano` | |
| `gpt-5-chat` | |
| `gpt-5.2` | |
| `gpt-5.2-chat` | |
| `gpt-4.1` | |
| `gpt-4.1-mini` | |
| `gpt-4.1-nano` | |
| `gpt-4o` | |
| `gpt-4o-mini` | |
| `o4-mini` | |
| `grok-4` | `**` |
| `grok-4-fast-reasoning` | `**` |
| `DeepSeek-V3.1` | `**` |
| `DeepSeek-V3.2` | `**` |
| `gpt-oss-120b` | `**` |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | `**` |
| `claude-haiku-4-5` | `**` |
| `claude-sonnet-4-5` | `**` |
| `claude-opus-4-1` | `**` |
| `claude-opus-4-6` | `**` |

---

## Automatic Failover

Model Router includes **built-in automatic failover**. When routing to all supported models (default scope), the router transparently redirects each request to the next most appropriate model if a transient issue affects any single model — so your application is never disrupted by individual model availability.

Failover is **enabled by default** — no additional configuration is required.

---

---

## Prerequisites

- Python 3.10+
- Azure subscription with **Azure AI Foundry** access
- A **Model Router** deployment configured in your Foundry project (not a direct model deployment)
- Required packages: `openai`, `python-dotenv`

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

```bash
cp .env.example .env
```

Edit `.env` with your Foundry resource details:

```env
DEPLOYMENT_NAME=<your-model-router-deployment-name>
MODEL_ROUTER_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-azure-openai-key>
```

> **Important:** `DEPLOYMENT_NAME` must point to your **Model Router** deployment in Foundry — not a specific model like `gpt-4o`. The router deployment performs the dynamic dispatch transparently.

### 4. Run the demo

```bash
python foundry_built_in_model_router.py
```

---

## Example Output

```
================================================================
  Microsoft Foundry — Model Router Multimodel Demo
================================================================

[1/6] Simple factual
  User: What is the capital of France?
  Router → o4-mini-2025-04-16
  Tokens  prompt=23  completion=27
  Answer: The capital of France is Paris.

[2/6] Reasoning / coding
  User: Implement a thread-safe LRU cache in Python using OrderedDict...
  Router → gpt-4.1-mini-2025-04-14
  Tokens  prompt=45  completion=353
  Answer: import threading...

[3/6] Creative writing
  User: Write a two-paragraph short story about an astronaut...
  Router → gpt-4o-mini-2024-07-18
  Tokens  prompt=35  completion=297
  Answer: The red dust settled around Commander Yara's boots...

...

================================================================
  Routing Summary
================================================================
  Task                      Model selected                In    Out
  ------------------------- --------------------------  ------  ------
  Simple factual            o4-mini-2025-04-16              23      27
  Reasoning / coding        gpt-4.1-mini-2025-04-14         45     353
  Creative writing          gpt-4o-mini-2024-07-18          35     297
  Data extraction           o4-mini-2025-04-16              44     166
  Summarisation             o4-mini-2025-04-16              85     151
  Multi-step reasoning      gpt-4.1-mini-2025-04-14         65     512

  Model distribution:
    o4-mini-2025-04-16        ███ (3)
    gpt-4.1-mini-2025-04-14   ██  (2)
    gpt-4o-mini-2024-07-18    █   (1)
================================================================
```

---

## How the Router Works

When you call the router endpoint, Foundry evaluates the following signals per request:

| Signal | Examples |
|---|---|
| Prompt complexity | Token count, nested reasoning, code generation |
| Task type | Factual retrieval vs. creative vs. structured output |
| Routing mode | Balanced (default) / Quality / Cost — set at deployment time |
| Cost optimisation | Simple queries routed to smaller, cheaper models |
| Reasoning requirement | Reasoning models selected only when needed |

You do **not** need to implement any of this logic client-side. The router handles classification and dispatch transparently — your application stays clean, model-agnostic, and future-proof as new models are added to the Foundry catalogue.

---

## Project Structure

```
MSFoundryModelRouter/
├── foundry_built_in_model_router.py   # Entry point — runs all demo prompts
├── .env.example                       # Environment variable template (safe to commit)
├── .gitignore                         # Excludes .env and secrets
├── requirements.txt                   # Python dependencies
└── README.md
```

---

## Customising Prompts

Add your own task categories to the `DEMO_PROMPTS` list in `foundry_built_in_model_router.py`:

```python
{
    "label": "Your task label",
    "system": "Your system prompt.",
    "user": "Your user prompt here.",
},
```

The routing summary and model distribution chart update automatically based on whatever prompts you add.

---

## Part of the Microsoft Foundry Open-Source Series

This repo is one of a growing set of production-ready reference implementations for Azure AI Foundry:

| Repo | Focus |
|---|---|
| [MSFoundryAgentMemory](https://github.com/praveen11singh/MSFoundryAgentMemory) | Ephemeral, contextual & persistent memory patterns |
| [MSFoundryFunctionCall](https://github.com/praveen11singh/MSFoundryFunctionCall) | Auto & explicit function calling with ToolSet |
| [MSFoundryAgentImageInput](https://github.com/praveen11singh/MSFoundryAgentImageInput) | Multi-modal image input with Foundry agents |
| [MSFoundryEvaluation](https://github.com/praveen11singh/MSFoundryEvaluation) | Agent evaluation with `azure-ai-evaluation` |
| [MSFoundryRedTeam](https://github.com/praveen11singh/MSFoundryRedTeam) | Red team jailbreak probing & RAI evaluators |
| [MSFoundryAgentStreamEvent](https://github.com/praveen11singh/MSFoundryAgentStreamEvent) | Streaming event handling patterns |
| [MSFoundryAgentFormat](https://github.com/praveen11singh/MSFoundryAgentFormat) | Response formatting & structured output |
| **MSFoundryModelRouter** | Dynamic multi-model routing ← you are here |

---

## Author

**Praveen Kumar**
Azure Solutions Architect & AI Engineer · Associate Consultant @ Tata Consultancy Services

[![LinkedIn]](https://www.linkedin.com/in/praveen11singh)
[![GitHub]](https://github.com/praveen11singh)

---

