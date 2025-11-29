"""
Episode 1: LangGraph Basics - Part 2
=====================================
Agent with a Tool

Now we'll build a REAL agent:
- Uses an actual LLM (like ChatGPT or Claude)
- Can call tools (like a calculator)
- Makes decisions about when to use tools

This is where the magic happens!
"""

import os
from typing import Annotated, Literal
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


# Step 1: Create a Tool
# ----------------------
# A tool is just a Python function with a decorator
# The LLM can "call" this function when it needs to
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The product of a and b
    """
    result = a * b
    print(f"  🔧 Tool called: multiply({a}, {b}) = {result}")
    return result


# Step 2: Define State with Messages
# -----------------------------------
# This time we use a special "messages" field
# The add_messages function handles appending new messages
class AgentState(TypedDict):
    """State that tracks conversation messages"""

    # Annotated tells LangGraph to append messages instead of replacing them
    messages: Annotated[list, add_messages]


# Step 3: Create the LLM Node
# ----------------------------
def llm_node(state: AgentState) -> AgentState:
    """
    This node calls the LLM.
    The LLM can decide to either:
    - Respond directly to the user, OR
    - Call a tool to help answer
    """
    # Initialize the LLM with our tool
    llm = ChatAnthropic(model="claude-sonnet-4-5")
    llm_with_tools = llm.bind_tools([multiply])

    # Call the LLM with the conversation history
    response = llm_with_tools.invoke(state["messages"])

    # Return the LLM's response (will be added to messages)
    return {"messages": [response]}


# Step 4: Create a Router
# ------------------------
# This function decides what to do next
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Determines whether to call tools or end the conversation.

    If the last message has tool_calls, we route to the tools node.
    Otherwise, we end.
    """
    last_message = state["messages"][-1]

    # Check if the LLM wants to call a tool
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("  🤔 LLM wants to use a tool...")
        return "tools"
    else:
        print("  ✅ LLM has the final answer!")
        return "end"


# Step 5: Build the Graph
# ------------------------
def create_agent():
    """Creates an agent that can use tools"""

    # Create the graph
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("llm", llm_node)
    # ToolNode automatically executes tools the LLM requests
    graph.add_node("tools", ToolNode([multiply]))

    # Define the flow
    graph.add_edge(START, "llm")

    # Add conditional routing
    # After the LLM, decide whether to use tools or end
    graph.add_conditional_edges(
        "llm",  # Start from llm node
        should_continue,  # Use this function to decide
        {
            "tools": "tools",  # If returns "tools", go to tools node
            "end": END,  # If returns "end", finish
        },
    )

    # After tools execute, go back to the LLM
    graph.add_edge("tools", "llm")

    return graph.compile()


# Step 6: Run the Agent
# ----------------------
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Make sure you have your API key set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Please set your ANTHROPIC_API_KEY environment variable")
        print("   Option 1: Create a .env file with: ANTHROPIC_API_KEY=your-key-here")
        print("   Option 2: Export it: export ANTHROPIC_API_KEY='your-key-here'")
        exit(1)

    print("\n" + "=" * 60)
    print("🤖 Agent with Tool - Calculator Agent")
    print("=" * 60 + "\n")

    # Create the agent
    agent = create_agent()

    # Test 1: Simple question (no tool needed)
    print("Test 1: Simple greeting")
    print("-" * 60)
    result = agent.invoke(
        {"messages": [HumanMessage(content="Hello! What can you help me with?")]}
    )
    print(f"Agent: {result['messages'][-1].content}\n")

    # Test 2: Math question (tool will be used!)
    print("\nTest 2: Math question (should use the multiply tool)")
    print("-" * 60)
    result = agent.invoke(
        {"messages": [HumanMessage(content="What is 234 times 567?")]}
    )
    print(f"Agent: {result['messages'][-1].content}\n")

    # Test 3: Another math question
    print("\nTest 3: Another calculation")
    print("-" * 60)
    result = agent.invoke(
        {"messages": [HumanMessage(content="Calculate 12.5 multiplied by 8")]}
    )
    print(f"Agent: {result['messages'][-1].content}\n")

    print("=" * 60)
    print("✨ Notice how the agent:")
    print("   1. Receives your question")
    print("   2. Decides if it needs a tool")
    print("   3. Calls the multiply tool if needed")
    print("   4. Uses the result to answer your question")
    print("=" * 60 + "\n")
