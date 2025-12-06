"""
Episode 2: Memory and State
============================
Agent with Conversation Memory

In Episode 1, our agent had no memory - each question was isolated.
Now we'll add MEMORY so the agent remembers the conversation!

Key Concepts:
- Checkpointers: Save state between turns
- Thread IDs: Separate conversations
- Message History: Context across multiple interactions
"""

import os
from typing import Annotated, Literal
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode


# Step 1: Create Some Simple Tools
# ---------------------------------
@tool
def add(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    result = a + b
    print(f"  🔧 Tool: add({a}, {b}) = {result}")
    return result


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
    print(f"  🔧 Tool: multiply({a}, {b}) = {result}")
    return result


# Step 2: Define State (Same as Episode 1)
# -----------------------------------------
class AgentState(TypedDict):
    """State that tracks conversation messages"""
    messages: Annotated[list, add_messages]


# Step 3: Create Agent with Memory
# ----------------------------------
def create_agent_with_memory():
    """
    Creates an agent that REMEMBERS conversations!

    The key difference: We add a checkpointer that saves state.
    """
    # Initialize LLM with tools
    llm = ChatAnthropic(model="claude-sonnet-4-5")
    llm_with_tools = llm.bind_tools([add, multiply])

    # Define the agent node
    def agent_node(state: AgentState) -> AgentState:
        """Call the LLM with the current message history"""
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    # Router function to decide next step
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Check if we need to call tools or end"""
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return "end"

    # Build the graph with proper tool execution
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode([add, multiply]))

    # Define edges
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )
    graph.add_edge("tools", "agent")

    # THE MAGIC: Add a checkpointer to save state!
    # MemorySaver stores conversation history in memory
    checkpointer = MemorySaver()

    # Compile with the checkpointer
    return graph.compile(checkpointer=checkpointer)


# Step 4: Using the Agent with Memory
# ------------------------------------
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Please set your ANTHROPIC_API_KEY environment variable")
        exit(1)

    print("\n" + "=" * 70)
    print("🧠 Agent with Memory - Remembering Conversations")
    print("=" * 70 + "\n")

    # Create agent with memory
    agent = create_agent_with_memory()

    # Each conversation needs a unique thread_id
    # Think of it like a conversation ID or session ID
    config = {"configurable": {"thread_id": "conversation-1"}}

    # Turn 1: Introduce yourself
    print("👤 User: Hi! My name is Alice.")
    print("-" * 70)
    result = agent.invoke(
        {"messages": [HumanMessage(content="Hi! My name is Alice.")]},
        config=config  # Pass the config to save state
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    # Turn 2: Ask a question
    print("👤 User: What's 25 + 17?")
    print("-" * 70)
    result = agent.invoke(
        {"messages": [HumanMessage(content="What's 25 + 17?")]},
        config=config  # Same thread_id = same conversation
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    # Turn 3: Reference earlier information
    print("👤 User: Do you remember my name?")
    print("-" * 70)
    result = agent.invoke(
        {"messages": [HumanMessage(content="Do you remember my name?")]},
        config=config  # Same thread_id = agent remembers!
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    # Turn 4: Reference calculation
    print("👤 User: Can you multiply that result by 2?")
    print("-" * 70)
    result = agent.invoke(
        {"messages": [HumanMessage(content="Can you multiply that result by 2?")]},
        config=config
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    print("=" * 70)
    print("✨ Key Takeaway:")
    print("   - MemorySaver stores conversation history")
    print("   - thread_id keeps conversations separate")
    print("   - Agent remembers context across multiple turns")
    print("   - Each invoke adds to the same conversation thread")
    print("=" * 70)

    # Bonus: Show a NEW conversation (different thread_id)
    print("\n" + "=" * 70)
    print("🆕 Starting a NEW Conversation")
    print("=" * 70 + "\n")

    new_config = {"configurable": {"thread_id": "conversation-2"}}

    print("👤 User: Do you know my name?")
    print("-" * 70)
    result = agent.invoke(
        {"messages": [HumanMessage(content="Do you know my name?")]},
        config=new_config  # Different thread_id = fresh conversation
    )
    print(f"🤖 Agent: {result['messages'][-1].content}\n")

    print("=" * 70)
    print("✨ Notice: With a different thread_id, the agent has no memory")
    print("   of the previous conversation!")
    print("=" * 70 + "\n")
