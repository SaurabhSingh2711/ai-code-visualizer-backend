# AI Code-to-Architecture Visualizer (Backend)

This backend powers the AI Visualizer tool that parses source code and generates architecture diagrams in real-time.

## Stack
- FastAPI (Python)
- Uvicorn Server
- Modular architecture for parsing, diagram generation, and AI insights.

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate environment: `venv\Scripts\activate` or `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run app: `uvicorn app.main:app --reload`
