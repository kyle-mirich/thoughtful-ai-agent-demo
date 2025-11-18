"""
Thoughtful AI Support Agent

This module implements an AI agent that answers questions about Thoughtful AI's
healthcare automation products (EVA, CAM, PHIL) using LangChain's create_agent.

Features:
- Structured output with confidence scores and reasoning
- Short-term memory for conversation context
- Tool integration for knowledge base retrieval
- Fallback to general LLM responses for non-product questions

Author: Kyle M.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver

# Load environment variables
load_dotenv()

# Predefined knowledge base
THOUGHTFUL_AI_DATA = {
    "questions": [
        {
            "question": "What does the eligibility verification agent (EVA) do?",
            "answer": "EVA automates the process of verifying a patient’s eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
        },
        {
            "question": "What does the claims processing agent (CAM) do?",
            "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
        },
        {
            "question": "How does the payment posting agent (PHIL) work?",
            "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
        },
        {
            "question": "Tell me about Thoughtful AI's Agents.",
            "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
        },
        {
            "question": "What are the benefits of using Thoughtful AI's agents?",
            "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
        }
    ]
}

@tool
def get_thoughtful_ai_info(query: str) -> str:
    """
    Retrieves information about Thoughtful AI's agents (EVA, CAM, PHIL) and their benefits.
    Use this tool when the user asks specifically about Thoughtful AI, its products, or benefits.
    """
    query = query.lower()
    # Simple keyword matching for this demo
    for item in THOUGHTFUL_AI_DATA["questions"]:
        if query in item["question"].lower() or item["question"].lower() in query:
             return item["answer"]
    
    # Fallback for broader search if exact match fails
    results = []
    for item in THOUGHTFUL_AI_DATA["questions"]:
        if any(word in item["question"].lower() for word in query.split()):
            results.append(f"Q: {item['question']}\nA: {item['answer']}")
            
    if results:
        return "\n\n".join(results[:2]) # Return top 2 relevant matches
        
    return "No specific information found in the knowledge base."

def get_chat_model(model_name: str = "google_genai:gemini-2.5-flash-lite", temperature: float = 0.7, max_tokens: int = 1024):
    """
    Initializes and returns the chat model.
    Ensures that the GOOGLE_API_KEY is set.
    """
    # Check for API key in environment or Streamlit secrets
    if not os.environ.get("GOOGLE_API_KEY"):
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
        except (FileNotFoundError, AttributeError):
            # st.secrets might not be available if not running via streamlit or no secrets.toml
            pass

    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in environment variables or Streamlit secrets")
        
    return init_chat_model(model_name, temperature=temperature, max_tokens=max_tokens)

class ResponseSchema(BaseModel):
    """Structure for the agent's output."""
    answer: str = Field(description="The direct answer to the user's question")
    confidence: float = Field(description="Confidence score between 0 and 1")
    reasoning: list[str] = Field(description="List of reasoning steps taken", default_factory=list)

def get_agent():
    """
    Creates and returns the Thoughtful AI agent.
    """
    model = get_chat_model()
    checkpointer = InMemorySaver()
    tools = [get_thoughtful_ai_info]
    
    return create_agent(
        model=model,
        tools=tools,
        response_format=ResponseSchema,
        checkpointer=checkpointer
    )

if __name__ == "__main__":
    try:
        # Verify key loading
        print("Key loaded:", bool(os.environ.get("GOOGLE_API_KEY")))
        
        agent = get_agent()
        print("Agent initialized successfully.")
        
        # Config with thread_id for memory
        config = {"configurable": {"thread_id": "1"}}

        # Run agent - First interaction
        print("\n--- Interaction 1 ---")
        print("User: Hi, my name is Bob.")
        result1 = agent.invoke(
            {"messages": [{"role": "user", "content": "Hi, my name is Bob."}]},
            config
        )
        print("Agent:", result1["structured_response"])

        # Run agent - Second interaction (testing memory)
        print("\n--- Interaction 2 ---")
        print("User: What is my name?")
        result2 = agent.invoke(
            {"messages": [{"role": "user", "content": "What is my name?"}]},
            config
        )
        print("Agent:", result2["structured_response"])
        
        # Run agent - Third interaction (testing tool)
        print("\n--- Interaction 3 ---")
        print("User: What does EVA do?")
        result3 = agent.invoke(
            {"messages": [{"role": "user", "content": "What does EVA do?"}]},
            config
        )
        print("Agent:", result3["structured_response"])

    except Exception as e:
        print(f"Error: {e}")
