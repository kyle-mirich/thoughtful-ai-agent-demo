# Thoughtful AI Support Agent

A conversational AI agent built to assist users with questions about Thoughtful AI's healthcare automation products (EVA, CAM, and PHIL). The agent uses LangChain's `create_agent` with structured output and short-term memory to provide accurate, context-aware responses.

## Features

- **🤖 Intelligent Agent**: Uses Google's Gemini model via LangChain
- **🧠 Short-term Memory**: Remembers conversation context within a session
- **📊 Structured Output**: Returns responses with confidence scores and reasoning
- **🔧 Tool Integration**: Retrieves information from a predefined knowledge base
- **💬 Web Interface**: Clean Streamlit chat UI

## Tech Stack

- **Python 3.14**
- **LangChain**: Agent framework with structured output
- **LangGraph**: State management and checkpointing
- **Streamlit**: Web interface
- **Google Gemini**: LLM (gemini-2.5-flash-lite)
- **Pydantic**: Data validation and structured responses

## Project Structure

```
thoughtful-ai-demo/
├── agent.py              # Core agent logic with tools and memory
├── app.py                # Streamlit web interface
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
├── .env.example          # Example environment file
└── README.md             # This file
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd thoughtful-ai-demo
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your Google API key:

```
GOOGLE_API_KEY="your-api-key-here"
```

**Get a Google API key**: [https://ai.google.dev/](https://ai.google.dev/)

## Usage

### Run the Streamlit Web App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Run the CLI Demo

```bash
python agent.py
```

This runs a test script demonstrating:
- Memory persistence (remembering user's name)
- Tool usage (answering questions about Thoughtful AI products)
- Structured output with confidence and reasoning

## Example Queries

Try asking the agent:

- "What does EVA do?"
- "Tell me about Thoughtful AI's agents"
- "What are the benefits of using Thoughtful AI's agents?"
- "How does the payment posting agent work?"
- "What does CAM do?"

The agent will use its knowledge base for Thoughtful AI-specific questions and fall back to general LLM responses for other topics.

## Implementation Details

### Agent Architecture

The agent uses LangChain's `create_agent` with:

1. **Structured Output**: Responses follow a Pydantic schema with `answer`, `confidence`, and `reasoning` fields
2. **Short-term Memory**: `InMemorySaver` checkpointer maintains conversation history per thread
3. **Tool Calling**: `get_thoughtful_ai_info` tool searches the predefined knowledge base

### Knowledge Base

The agent has hardcoded information about:
- **EVA** (Eligibility Verification Agent)
- **CAM** (Claims Processing Agent)
- **PHIL** (Payment Posting Agent)

### Response Schema

```python
class ResponseSchema(BaseModel):
    answer: str              # The direct answer
    confidence: float        # Confidence score (0-1)
    reasoning: list[str]     # Reasoning steps taken
```

## Development

### Code Quality

- Clean, modular code structure
- Type hints throughout
- Comprehensive docstrings
- Error handling for missing API keys

### Best Practices

- Environment variables for sensitive data
- Reusable `get_agent()` function
- Separation of concerns (agent logic vs. UI)
- Session-based memory management

## Requirements

See `requirements.txt` for full dependencies:

- streamlit
- langchain
- langchain-google-genai
- langchain-core
- python-dotenv
- langgraph

## License

This project was created as a technical demonstration for Thoughtful AI.

## Author

Kyle M.

---

**Note**: This is a demonstration project showcasing AI agent development skills including tool integration, memory management, and structured output handling.
