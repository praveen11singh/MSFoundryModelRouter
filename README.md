MSFoundryModelRouter

Microsoft Foundry — Intelligent Model RouterRoute prompts dynamically across multiple LLMs based on task complexity, cost, and capability — powered by Azure AI Foundry. 

Overview

MSFoundryModelRouter is a reference implementation that demonstrates how to use an Azure AI Foundry Model Router deployment to dispatch prompts to the most appropriate underlying model at inference time. A single router endpoint evaluates each request and routes it to the best-fit model (for example, a smaller model for factual queries and a larger model for complex reasoning) without any client-side hardcoding. 

Key benefits

Automatic model selection per request

Cost and latency optimization by routing to smaller or larger models as appropriate

Token usage tracking and routing summaries for observability

Extensible — add more task categories or models without changing client logic

Features

Six demo task categories: factual, reasoning/coding, creative writing, data extraction, summarisation, multi-step reasoning.

Routing summary: tabular output showing which model handled each task and token counts.

Model distribution chart: ASCII bar chart showing routing spread.

Zero credential leakage: secrets are read from .env only. 

Prerequisites

Python 3.10+

Azure subscription with Azure AI Foundry access

A Model Router deployment configured in your Foundry project (this is a router deployment, not a single-model deployment)

Install dependencies:

pip install -r requirements.txt



Quickstart

Clone the repo

git clone https://github.com/praveen11singh/MSFoundryModelRouter.git
cd MSFoundryModelRouter

Create environment file

cp .env.example .env
# Edit .env and set values:
# DEPLOYMENT_NAME=<your-model-router-deployment-name>
# MODEL_ROUTER_ENDPOINT=https://<your-resource>.openai.azure.com/
# AZURE_OPENAI_API_KEY=<your-azure-openai-key>

Important: DEPLOYMENT_NAME must point to your Model Router deployment in Foundry — not a specific model like gpt-4o. The router deployment performs the dynamic dispatch. 

Run the demo

python foundry_built_in_model_router.py

Usage and Example Output

Running the demo executes a set of sample prompts across the six task categories and prints a routing summary that includes:

Task label and model selected

Prompt and completion token counts

Answer text for each prompt

Overall model distribution (ASCII chart)

Excerpt

[1/6] Simple factual User: What is the capital of India? Router → o4-mini-2025-04-16 Tokens  prompt=23  completion=91 Answer: The capital of India is New Delhi.

[2/6] Reasoning / coding User: Implement a thread-safe LRU cache in Python using OrderedDict. Include get, put,... Router → gpt-4.1-mini-2025-04-14 Tokens  prompt=45  completion=341 Answer: Certainly! Here's a thread-safe implementation of an LRU cache using collections.OrderedDict with a threading lock to ensure safety in concurrent environments.

from collections import Ord...

[3/6] Creative writing
  User: Write a two-paragraph short story about an astronaut who discovers a library on ...
  Router → gpt-4o-mini-2024-07-18
  Tokens  prompt=35  completion=301
  Answer: Captain Elena Torres floated through the desolate landscape of Mars, her breath hitching as she surveyed the rust-red horizon. It had been weeks since humanity's first manned mission to the red planet...

[4/6] Data extraction
  User: Extract name, role, and company from: 'Hi, I'm Sarah Chen, a senior data scienti...
  Router → o4-mini-2025-04-16
  Tokens  prompt=44  completion=102
  Answer: {"name":"Sarah Chen","role":"senior data scientist","company":"Contoso Analytics"}

[5/6] Summarisation
  User: Summarise: Retrieval-Augmented Generation (RAG) combines a retrieval system with...
  Router → o4-mini-2025-04-16
  Tokens  prompt=85  completion=209
  Answer: Retrieval-Augmented Generation (RAG) integrates a retrieval system with a generative model, where the retriever sources relevant documents from a corpus and the generator uses that material as context...

[6/6] Multi-step reasoning
  User: A train leaves London at 09:00 travelling at 120 mph. Another leaves Edinburgh (...
  Router → gpt-4.1-mini-2025-04-14
  Tokens  prompt=65  completion=487
  Answer: Let's analyze the problem step-by-step.

### Given:
- Distance between London and Edinburgh = 400 miles
- Train A leaves London at 09:00 traveling towards Edinburgh at 120 mph.
- Train B leaves Edinbu...

================================================================
  Routing Summary
================================================================
  Task                      Model selected           In    Out
  ------------------------- -------------------- ------ ------
  Simple factual            o4-mini-2025-04-16       23     91
  Reasoning / coding        gpt-4.1-mini-2025-04-14     45    341
  Creative writing          gpt-4o-mini-2024-07-18     35    301
  Data extraction           o4-mini-2025-04-16       44    102
  Summarisation             o4-mini-2025-04-16       85    209
  Multi-step reasoning      gpt-4.1-mini-2025-04-14     65    487

  Model distribution:
    o4-mini-2025-04-16   ███ (3)
    gpt-4.1-mini-2025-04-14 ██ (2)
    gpt-4o-mini-2024-07-18 █ (1)
================================================================

This output helps you verify routing behavior and token usage. 

Project Structure

MSFoundryModelRouter/
├─ foundry_built_in_model_router.py
├─ .env.example       # Environment template
├─ requirements.txt
├─ README.md
├─ .gitignore

foundry_built_in_model_router.py contains DEMO_PROMPTS — add or modify entries to test custom prompt categories. 

How the Router Works

When you call the router endpoint with a prompt, Foundry evaluates signals such as:

Prompt complexity (token count, nested reasoning, code generation)

Task type (factual vs. creative vs. structured output)

Cost and latency preferences configured in the router deployment

The router uses these signals to select the best underlying model for each request; your client code remains model-agnostic.

Customization

Add prompts: Edit DEMO_PROMPTS in foundry_built_in_model_router.py to add new task labels, system prompts, or user prompts.

Change logging: Extend the token tracking and routing summary to persist results to a file or telemetry system.

Extend models: Update your Foundry router deployment to include additional models or change routing policies — no client changes required.

Contributing

Issues and PRs are welcome.

Keep secrets out of commits; use .env for credentials.

Follow the existing code style and add tests for new behaviors where appropriate.

License and Author

Author: Praveen Kumar — Azure Solutions Architect & AI Engineer.

If you’d like, I can:

Produce a ready-to-commit README.md file formatted exactly as above, or

Tailor the Quickstart and .env examples to match any CI/CD or deployment patterns you use.

References (1)

GitHub - praveen11singh/MSFoundryModelRouter: model-router. https://github.com/praveen11singh/MSFoundryModelRouter
