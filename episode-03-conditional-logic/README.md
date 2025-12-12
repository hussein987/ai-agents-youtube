# Episode 3: Conditional Logic & Branching

[![Watch on YouTube](https://img.youtube.com/vi/ot-eA2TMa9M/maxresdefault.jpg)](https://youtu.be/ot-eA2TMa9M)

Learn how to build agents that make smart routing decisions based on state!

## What You'll Learn

In Episodes 1-2, our agents followed linear paths. Now we'll add **conditional logic** so agents can:

- Route to different nodes based on conditions
- Make smart decisions about which path to take
- Build decision trees in your workflows
- Create specialized agent behaviors

## Key Concepts

### 1. Conditional Edges
Unlike normal edges (A → B), conditional edges use a router function to decide the next node.

```python
graph.add_conditional_edges(
    "categorize",           # Source node
    route_to_specialist,    # Router function
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general"
    }
)
```

### 2. Router Functions
Functions that inspect state and return the name of the next node.

```python
def route_to_specialist(state: SupportState) -> Literal["billing", "technical", "general"]:
    category = state.get("category", "general")
    return category  # Returns next node name
```

### 3. State-Based Routing
Decisions are based on values in the state, making routing dynamic and intelligent.

### 4. Multiple Paths
Different execution paths through the graph based on conditions.

```
START → categorize → [billing|technical|general] → END
                      ↓       ↓           ↓
                    Three different specialist paths!
```

## The Example: Customer Support Agent

We build a smart customer support agent that:
1. Receives a user question
2. Categorizes it (billing, technical, general)
3. Routes to the appropriate specialist
4. Specialist responds with domain expertise

## Code Structure

```
episode-03-conditional-logic/
└── 01_conditional_routing.py   # Smart routing agent
```

## Running the Code

```bash
cd episode-03-conditional-logic
python 01_conditional_routing.py
```

## What Happens

**Test 1: Billing Question**
- User: "I need a refund for my last payment"
- Categorized as: `billing`
- Routed to: Billing Specialist
- Response: Professional billing help

**Test 2: Technical Question**
- User: "Why am I getting a 404 error?"
- Categorized as: `technical`
- Routed to: Technical Specialist
- Response: Technical troubleshooting

**Test 3: General Question**
- User: "Hello! What services do you offer?"
- Categorized as: `general`
- Routed to: General Support
- Response: Friendly general information

## The Key Difference

**Without Conditional Edges (Episodes 1-2)**:
```python
# Linear flow
graph.add_edge(START, "agent")
graph.add_edge("agent", "tools")
graph.add_edge("tools", END)
```

**With Conditional Edges (Episode 3)**:
```python
# Dynamic routing
graph.add_conditional_edges(
    "categorize",
    router_function,  # Decides next node!
    {
        "option1": "node1",
        "option2": "node2",
        "option3": "node3"
    }
)
```

## When to Use Conditional Routing

- **Customer Support**: Route to specialized departments
- **Content Moderation**: Different actions for different violation types
- **Data Processing**: Different pipelines for different data types
- **Workflow Automation**: Dynamic task routing based on priority
- **Chatbots**: Different conversation flows based on intent

## Router Function Best Practices

1. **Keep it Simple**: Router should just return a node name
2. **Use Literals**: Type hints ensure valid return values
3. **Default Cases**: Always have a fallback path
4. **State Access**: Inspect state to make decisions

```python
def router(state: MyState) -> Literal["path1", "path2", "default"]:
    if state["condition"] == "A":
        return "path1"
    elif state["condition"] == "B":
        return "path2"
    else:
        return "default"
```

## Graph Visualization

The graph looks like this:

```
    START
      ↓
  categorize
      ↓
   [Router]
    / | \
   /  |  \
billing technical general
   \  |  /
    \ | /
      ↓
     END
```

Each path has its own specialized behavior!

## Advanced Patterns

### Multi-Level Routing
You can chain conditional edges for complex decision trees:

```
START → categorize → [type1|type2|type3]
                           ↓
                      sub_categorize → [subA|subB] → END
```

### Conditional Returns to Same Node
Routers can send execution back to earlier nodes:

```python
def should_retry(state: State) -> Literal["retry", "end"]:
    if state["attempts"] < 3:
        return "retry"
    return "end"
```

## Next Steps

- Try adding more specialist categories
- Implement multi-level routing (category → subcategory)
- Add error handling paths
- Build a decision tree agent

## Resources

- [LangGraph Conditional Edges Documentation](https://docs.langchain.com/oss/python/langgraph/graph-api#conditional-edges)
- [LangGraph Graph API Overview](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
