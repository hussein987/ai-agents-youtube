# Episode 1: LangGraph Basics - Your First AI Agent

Welcome to the first episode of the AI Agents series! In this episode, we'll build your first AI agent from scratch using LangGraph.

## What You'll Learn

By the end of this episode, you'll understand:

- **What is an AI Agent?** - A program that can make decisions and use tools
- **Core LangGraph Concepts:**
  - **Graph**: A workflow that defines how your agent operates
  - **Node**: A function that does specific work (like calling an LLM or running a tool)
  - **Edge**: Connections between nodes that define the flow
  - **State**: Shared data that flows through your agent
- **How to build a working agent** that can use tools to solve problems

## What We Build

We'll create TWO agents, progressively:

### Part 1: Simple Agent (`01_simple_agent.py`)
A basic agent that demonstrates the core concepts without any complexity:
- Defines state (a simple message)
- Creates a node (a greeting function)
- Builds a graph (connects everything)
- Runs the agent

**Perfect for**: Understanding the fundamentals

### Part 2: Agent with Tool (`02_agent_with_tool.py`)
A REAL agent that can:
- Use Claude AI (Anthropic's LLM)
- Call a calculator tool when needed
- Make decisions about when to use tools
- Answer math questions accurately

**Perfect for**: Seeing agents in action

## Setup

### 1. Create Virtual Environment (from root directory)

```bash
# From the ai-agents-youtube directory (root)
cd ..
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install from root-level requirements.txt
pip install -r requirements.txt
```

### 3. Set Your API Key

You'll need an Anthropic API key for Part 2. Choose one method:

**Option 1: Use .env file (Recommended)**
```bash
# From the root directory
cp .env.example .env
# Then edit .env and add your actual API key
```

**Option 2: Export environment variable**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Get your API key at: https://console.anthropic.com/

## Running the Code

### Part 1: Simple Agent

```bash
# Make sure venv is activated and you're in the episode folder
cd episode-01-langgraph-basics
python 01_simple_agent.py
```

Expected output:
```
==================================================
Agent Response:
==================================================
Hello! You said: 'Hi there!'. Nice to meet you!
==================================================
```

### Part 2: Agent with Tool

```bash
python 02_agent_with_tool.py
```

This will run 3 tests:
1. Simple greeting (no tool needed)
2. Math question: "What is 234 times 567?" (uses multiply tool)
3. Another calculation (uses multiply tool)

## Key Concepts Explained

### What is a Graph?

Think of a graph like a flowchart:
- **Nodes** are the boxes (steps in your process)
- **Edges** are the arrows (how data flows)
- **State** is the data moving through the flowchart

### How Does the Agent Decide?

In Part 2, the agent follows this loop:

1. **LLM Node**: The AI reads your question
2. **Router**: Decides "Do I need a tool?"
   - If YES → go to Tools Node
   - If NO → return answer and END
3. **Tools Node**: Executes the tool (multiply function)
4. **Back to LLM**: LLM sees the tool result and formulates final answer

### Why This Architecture?

This pattern is the foundation of ALL AI agents:
- **Perception** (LLM understands the question)
- **Decision** (Router determines next action)
- **Action** (Tool execution)
- **Reasoning** (LLM uses results to answer)

## Common Issues

**Import errors?**
Make sure you installed dependencies from the root directory: `pip install -r ../requirements.txt`

**"Please set your ANTHROPIC_API_KEY"?**
Set your API key: `export ANTHROPIC_API_KEY='sk-ant-...'`

**Want to use OpenAI instead?**
Replace:
```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
```

With:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4")
```

## Next Steps

In the next episode, we'll explore:
- Adding multiple tools
- Building more complex graphs
- Handling conversation history
- Error handling and retries

## Resources

- [LangGraph Official Documentation](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [LangChain Tools](https://python.langchain.com/docs/integrations/tools/)
- [Anthropic API](https://docs.anthropic.com/)

## Challenge

Try modifying `02_agent_with_tool.py` to add a new tool:
- Add a `divide(a, b)` tool
- Test it with: "What is 100 divided by 4?"

Can you make it work? This is the best way to learn!
