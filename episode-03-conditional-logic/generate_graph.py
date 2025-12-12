"""
Generate the graph visualization for Episode 3
Shows the conditional routing architecture
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


# Define State
class SupportState(TypedDict):
    """State for our customer support agent"""
    messages: Annotated[list, add_messages]
    category: str


# Simplified nodes for visualization
def categorize_request(state: SupportState) -> SupportState:
    return {"category": "billing"}


def billing_specialist(state: SupportState) -> SupportState:
    return state


def technical_specialist(state: SupportState) -> SupportState:
    return state


def general_support(state: SupportState) -> SupportState:
    return state


def route_to_specialist(state: SupportState) -> Literal["billing", "technical", "general"]:
    category = state.get("category", "general")
    if category == "billing":
        return "billing"
    elif category == "technical":
        return "technical"
    else:
        return "general"


def create_support_agent():
    """Creates a customer support agent with conditional routing"""
    graph = StateGraph(SupportState)

    # Add all nodes
    graph.add_node("categorize", categorize_request)
    graph.add_node("billing", billing_specialist)
    graph.add_node("technical", technical_specialist)
    graph.add_node("general", general_support)

    # Define the flow
    graph.add_edge(START, "categorize")

    # Conditional edge
    graph.add_conditional_edges(
        "categorize",
        route_to_specialist,
        {
            "billing": "billing",
            "technical": "technical",
            "general": "general",
        }
    )

    # All specialists go to END
    graph.add_edge("billing", END)
    graph.add_edge("technical", END)
    graph.add_edge("general", END)

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    load_dotenv()

    print("Generating conditional routing graph visualization...")

    # Create the agent
    agent = create_support_agent()

    # Generate the graph image
    try:
        png_data = agent.get_graph().draw_mermaid_png()

        output_path = "conditional_routing_graph.png"
        with open(output_path, "wb") as f:
            f.write(png_data)

        print(f"✓ Graph saved to: {output_path}")

    except Exception as e:
        print(f"Error generating graph: {e}")
        print("\nAlternative: ASCII representation:")
        print(agent.get_graph().draw_ascii())
