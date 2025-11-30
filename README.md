
# 🌱 GreenWise AI - Sustainable Operations Orchestrator

AI-powered sustainability orchestration for enterprise operations using multi-agent systems and Google Gemini.

## Problem Statement
Enterprises struggle to reduce energy consumption and emissions because operational data is siloed, anomalies go undetected, and sustainability teams cannot quickly quantify the impact of proposed actions. GreenWise AI tackles this by continuously aggregating telemetry, detecting inefficiencies, and generating measurable, prioritized eco-actions.

## Solution Overview
GreenWise AI orchestrates two collaborating agents—**Data Scout** and **EcoPlanner**—to turn raw telemetry into actionable sustainability recommendations. The system provides:
- **Multi-Agent Orchestration**: Coordinated context gathering and planning for sustainability.
- **Real-time Analysis**: Continuous monitoring, anomaly detection, and metric visualization.
- **AI-Powered Recommendations**: Context-aware actions grounded in operational data.
- **Impact Quantification**: CO₂ and energy savings estimates with confidence scoring.
- **Feedback Loop**: User feedback on recommendations drives iterative improvement.
- **Enterprise Readiness**: Async Python backbone with observability and extensible tool integrations.

## System Architecture
- **Data Scout Agent**: Aggregates operational data, detects anomalies
- **EcoPlanner Agent**: Generates sustainability recommendations using Gemini
- **Memory Bank**: Persistent storage for context and learning
- **Tool Integration**: Emissions calculator, route optimizer, weather API
- **Gradio UI**: Interactive dashboard for monitoring and control

```
┌────────────────────┐      ┌────────────────────┐
│   Data Scout Agent │      │  EcoPlanner Agent  │
│  - ingest telemetry│      │  - generate plans  │
│  - detect anomalies│      │  - quantify impact │
└─────────┬──────────┘      └─────────┬──────────┘
          │                           │
          ▼                           ▼
    ┌───────────┐              ┌────────────┐
    │ Memory    │◄────────────►│ Gemini LLM │
    │ Bank (SQLite)            └────────────┘
    └─────┬─────┘
          │
          ▼
    ┌───────────┐
    │   Tools   │  Emissions calculator, IoT simulator, route/efficiency helpers
    └─────┬─────┘
          │
          ▼
    ┌───────────┐
    │ Gradio UI │  Real-time dashboard, feedback capture, history browser
    └───────────┘
```
### Core Components

- **Data Scout Agent**: Aggregates operational data and flags anomalies.
- **EcoPlanner Agent**: Generates sustainability recommendations with quantified impacts.
- **Memory Bank**: Persists context, plans, and feedback for longitudinal analysis.
- **Tool Integrations**: Emissions calculator, IoT simulator, and domain-specific utilities.
- **Gradio UI**: Interactive dashboard for monitoring, recommendations, and feedback.

## Setup & Run Instructions

### Prerequisites

- Python 3.10+
- Google Gemini API key

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment

Set required variables (locally or in your deployment platform):

```bash
export GEMINI_API_KEY="your_key_here"
# Optional overrides
export GEMINI_MODEL_NAME="gemini-2.5-flash"
export GEMINI_MAX_RETRIES=3
export GEMINI_RATE_LIMIT_DELAY=2
```

### 3) Launch the app locally

```bash
python app.py
```

Open the Gradio URL printed in the console to access the dashboard, generate recommendations, and submit feedback.

### 4) Deploy to Hugging Face Spaces

1. Add the secrets above in **Settings → Secrets**.
2. Push this repository to your Space; Gradio will auto-launch via `app.py`.
3. Monitor logs for rate limits; adjust retry/delay env vars as needed.

## Usage

1. Click **🔄 Refresh Data** on the dashboard to pull the latest simulated telemetry.
2. Use **Generate Sustainability Plan** to create a new set of AI recommendations.
3. Browse **Historical Plans** to compare recent runs and surfaced anomalies.
4. Submit **Feedback** on individual recommendations to refine future plans.
   
## Features

- **Multi-Agent Orchestration**: Data Scout + EcoPlanner agents working collaboratively
- **Real-time Analysis**: Continuous monitoring and anomaly detection
- **AI-Powered Recommendations**: Context-aware sustainability actions
- **Impact Quantification**: Precise CO2 and energy savings estimates
- **Feedback Loop**: Learn from user decisions and outcomes
- **Enterprise-Ready**: Scalable architecture with full observability

## Quick Start

1. **Set up API Key**: Add your Google Gemini API key to Hugging Face Secrets
   - Go to Settings → Secrets
   - Add: `GEMINI_API_KEY = your_key_here`
   - (Optional) Override the default lightweight model or rate limit handling:
     - `GEMINI_MODEL_NAME` – e.g. `gemini-2.5-flash`
     - `GEMINI_MAX_RETRIES` – number of retries when the RPM limit is hit
     - `GEMINI_RATE_LIMIT_DELAY` – seconds to wait between retries

2. **Launch**: The app will start automatically on Hugging Face Spaces

3. **Explore**:
   - View real-time dashboard
   - Generate AI recommendations
   - Provide feedback on actions
   - Track historical improvements

## Use Cases

- Manufacturing: Energy optimization, process efficiency
- Logistics: Route optimization, fleet management
- Facilities: HVAC control, lighting automation, space utilization

## Tech Stack

- Google Gemini (LLM)
- Gradio (UI)
- SQLite (Memory)
- Python asyncio (Multi-agent orchestration)

## License

MIT

## Live Demo & Hugging Face Space
- [Live Demo](https://youtu.be/CXMta4JoCJo)
- [Hugging Face Space](https://huggingface.co/spaces/dlanov/greenwise-ai)
