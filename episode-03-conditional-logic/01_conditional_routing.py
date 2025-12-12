"""
Episode 3: Conditional Logic & Branching
==========================================
Smart Routing Based on State

In Episodes 1-2, we built linear agents (A → B → C).
Now we'll add CONDITIONAL LOGIC so agents can make smart routing decisions!

Key Concepts:
- Conditional edges: Routes that depend on state
- Router functions: Decision logic
- Multiple paths: Different flows based on conditions
"""

import os
from typing import Annotated, Literal
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


# Step 1: Define State
# ---------------------
class SupportState(TypedDict):
    """State for our customer support agent"""
    messages: Annotated[list, add_messages]
    category: str  # Will store: "billing", "technical", or "general"


# Step 2: Categorization Node
# ----------------------------
def categorize_request(state: SupportState) -> SupportState:
    """
    Analyzes the user's message and categorizes it.
    This is our decision-making node.
    """
    llm = ChatAnthropic(model="claude-sonnet-4-5")

    # Get the user's last message
    user_message = state["messages"][-1].content

    # Ask LLM to categorize
    categorization_prompt = f"""
    You are a customer support router. Categorize this request into ONE category:
    - "billing" (payments, invoices, refunds, pricing)
    - "technical" (bugs, errors, how-to questions, features)
    - "general" (greetings, general questions, other)

    User message: {user_message}

    Respond with ONLY ONE WORD: billing, technical, or general
    """

    response = llm.invoke([HumanMessage(content=categorization_prompt)])
    category = response.content.strip().lower()

    print(f"  🔍 Categorized as: {category}")

    return {"category": category}


# Step 3: Specialist Nodes
# -------------------------
def billing_specialist(state: SupportState) -> SupportState:
    """Handles billing-related questions"""
    llm = ChatAnthropic(model="claude-sonnet-4-5")

    system_message = SystemMessage(
        content="You are a billing specialist. Help with payments, invoices, refunds, and pricing questions. Be professional and helpful."
    )

    response = llm.invoke([system_message] + state["messages"])

    print("  💰 Billing specialist responding...")
    return {"messages": [response]}


def technical_specialist(state: SupportState) -> SupportState:
    """Handles technical questions"""
    llm = ChatAnthropic(model="claude-sonnet-4-5")

    system_message = SystemMessage(
        content="You are a technical support specialist. Help with bugs, errors, how-to questions, and feature explanations. Be technical but clear."
    )

    response = llm.invoke([system_message] + state["messages"])

    print("  🔧 Technical specialist responding...")
    return {"messages": [response]}


def general_support(state: SupportState) -> SupportState:
    """Handles general questions"""
    llm = ChatAnthropic(model="claude-sonnet-4-5")

    system_message = SystemMessage(
        content="You are a friendly general support agent. Handle greetings, general questions, and route to specialists if needed."
    )

    response = llm.invoke([system_message] + state["messages"])

    print("  👋 General support responding...")
    return {"messages": [response]}


# Step 4: Router Function (THE KEY!)
# -----------------------------------
def route_to_specialist(state: SupportState) -> Literal["billing", "technical", "general"]:
    """
    This function decides which specialist to route to.
    Based on the category in the state, return the next node name.
    """
    category = state.get("category", "general")

    print(f"  🔀 Routing to: {category} specialist")

    # Return the name of the next node
    if category == "billing":
        return "billing"
    elif category == "technical":
        return "technical"
    else:
        return "general"


# Step 5: Build the Graph with Conditional Edges
# -----------------------------------------------
def create_support_agent():
    """
    Creates a customer support agent with conditional routing.

    Flow:
    START → categorize → [billing|technical|general] → END
    """
    graph = StateGraph(SupportState)

    # Add all nodes
    graph.add_node("categorize", categorize_request)
    graph.add_node("billing", billing_specialist)
    graph.add_node("technical", technical_specialist)
    graph.add_node("general", general_support)

    # Define the flow
    graph.add_edge(START, "categorize")

    # THE MAGIC: Conditional edge!
    # After categorize, the router function decides which specialist to call
    graph.add_conditional_edges(
        "categorize",           # Source node
        route_to_specialist,    # Router function
        {
            "billing": "billing",       # If returns "billing" → go to billing node
            "technical": "technical",   # If returns "technical" → go to technical node
            "general": "general",       # If returns "general" → go to general node
        }
    )

    # All specialists go to END
    graph.add_edge("billing", END)
    graph.add_edge("technical", END)
    graph.add_edge("general", END)

    # Add memory
    checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)


# Step 6: Test the Agent
# -----------------------
if __name__ == "__main__":
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Please set your ANTHROPIC_API_KEY environment variable")
        exit(1)

    print("\n" + "=" * 70)
    print("🤖 Customer Support Agent with Conditional Routing")
    print("=" * 70 + "\n")

    agent = create_support_agent()
    config = {"configurable": {"thread_id": "support-demo"}}

    # Test 1: Billing question
    print("Test 1: Billing Question")
    print("-" * 70)
    print("👤 User: I need a refund for my last payment")
    result = agent.invoke(
        {"messages": [HumanMessage(content="I need a refund for my last payment")]},
        config=config
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    # Test 2: Technical question
    print("\nTest 2: Technical Question")
    print("-" * 70)
    print("👤 User: Why am I getting a 404 error?")
    result = agent.invoke(
        {"messages": [HumanMessage(content="Why am I getting a 404 error?")]},
        config=config
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    # Test 3: General question
    print("\nTest 3: General Question")
    print("-" * 70)
    print("👤 User: Hello! What services do you offer?")
    result = agent.invoke(
        {"messages": [HumanMessage(content="Hello! What services do you offer?")]},
        config=config
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    print("=" * 70)
    print("✨ Notice how the agent:")
    print("   1. Categorizes each request")
    print("   2. Routes to the appropriate specialist")
    print("   3. Different specialists have different expertise")
    print("   4. All happens automatically based on state!")
    print("=" * 70 + "\n")
