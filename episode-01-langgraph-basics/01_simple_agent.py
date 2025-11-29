"""
Episode 1: LangGraph Basics - Part 1
=====================================
The Simplest Possible Agent

This script demonstrates the core concepts of LangGraph:
- Graph: A workflow that connects nodes
- Node: A function that does work
- Edge: A connection between nodes
- State: Data that flows through the graph

We'll build the simplest agent that just echoes back a greeting.
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


# Step 1: Define the State
# ------------------------
# State is just a dictionary that gets passed between nodes
# Think of it like a shared memory that all nodes can read and write to
class AgentState(TypedDict):
    """The state of our agent - just stores messages"""
    message: str


# Step 2: Create a Node (just a function!)
# -----------------------------------------
# A node is simply a Python function that:
# - Takes the current state as input
# - Returns updates to add to the state
def greeting_node(state: AgentState) -> AgentState:
    """
    This node creates a greeting response.
    It reads the input message and returns a friendly greeting.
    """
    user_message = state["message"]
    response = f"Hello! You said: '{user_message}'. Nice to meet you!"

    # Return the updated state
    return {"message": response}


# Step 3: Build the Graph
# ------------------------
# Now we connect everything together
def create_simple_agent():
    """Creates and returns a simple greeting agent"""

    # Create a new graph with our state type
    graph = StateGraph(AgentState)

    # Add our greeting node to the graph
    # The first argument is the function, second is optional name
    graph.add_node("greeter", greeting_node)

    # Define the flow: START -> greeter -> END
    graph.add_edge(START, "greeter")
    graph.add_edge("greeter", END)

    # Compile the graph (makes it ready to run)
    return graph.compile()


# Step 4: Run the Agent
# ----------------------
if __name__ == "__main__":
    # Create our agent
    agent = create_simple_agent()

    # Invoke it with an initial state
    result = agent.invoke({"message": "Hi there!"})

    # Print the result
    print("\n" + "="*50)
    print("Agent Response:")
    print("="*50)
    print(result["message"])
    print("="*50 + "\n")

    # Try another message
    result2 = agent.invoke({"message": "What's up?"})
    print("Another response:")
    print(result2["message"])
