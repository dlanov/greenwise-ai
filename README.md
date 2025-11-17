
# 🌱 GreenWise AI - Sustainable Operations Orchestrator

AI-powered sustainability orchestration for enterprise operations using multi-agent systems and Google Gemini.

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

2. **Launch**: The app will start automatically on Hugging Face Spaces

3. **Explore**:
   - View real-time dashboard
   - Generate AI recommendations
   - Provide feedback on actions
   - Track historical improvements

## Architecture

- **Data Scout Agent**: Aggregates operational data, detects anomalies
- **EcoPlanner Agent**: Generates sustainability recommendations using Gemini
- **Memory Bank**: Persistent storage for context and learning
- **Tool Integration**: Emissions calculator, route optimizer, weather API
- **Gradio UI**: Interactive dashboard for monitoring and control

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

