# Episode 2: Memory and State

[![Watch on YouTube](https://img.youtube.com/vi/XDi2Y1bhQEc/maxresdefault.jpg)](https://youtu.be/XDi2Y1bhQEc)

Learn how to give your AI agent a memory so it can remember conversations!

## What You'll Learn

In Episode 1, our agent answered questions but forgot everything immediately. Now we'll add **conversation memory** so the agent can:

- Remember what you told it earlier
- Reference previous calculations
- Maintain context across multiple turns
- Handle multiple separate conversations

## Key Concepts

### 1. Checkpointers
Think of a checkpointer like a save button for your agent. It stores the conversation state so nothing is forgotten.

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
agent = graph.compile(checkpointer=checkpointer)
```

### 2. Thread IDs
Each conversation needs a unique ID (like a session ID). Same thread ID = same conversation.

```python
config = {"configurable": {"thread_id": "conversation-1"}}
agent.invoke({"messages": [...]}, config=config)
```

### 3. Message History
The agent automatically maintains the full conversation history, so it always has context.

## Code Structure

```
episode-02-memory-and-state/
└── 01_agent_with_memory.py   # Agent that remembers conversations
```

## Running the Code

```bash
# Make sure you're in the project root with venv activated
cd episode-02-memory-and-state
python 01_agent_with_memory.py
```

## What Happens

1. **Turn 1**: You introduce yourself → Agent greets you
2. **Turn 2**: You ask for a calculation → Agent performs it
3. **Turn 3**: You ask "Do you remember my name?" → Agent does!
4. **Turn 4**: You reference the calculation → Agent remembers that too!
5. **New Thread**: Start fresh conversation → Agent has no memory of the first

## The Key Difference

**Without Memory (Episode 1)**:
```python
# Each call is isolated
agent.invoke({"messages": [...]})  # Forgets everything after this
agent.invoke({"messages": [...]})  # Has no context from before
```

**With Memory (Episode 2)**:
```python
config = {"configurable": {"thread_id": "chat-1"}}

agent.invoke({"messages": [...]}, config=config)  # Remembered
agent.invoke({"messages": [...]}, config=config)  # Remembers all previous
```

## When to Use Memory

- **Chatbots**: Multi-turn conversations
- **Customer Support**: Context across the conversation
- **Personal Assistants**: Remember user preferences and history
- **Tutoring Systems**: Track student progress

## Types of Checkpointers

LangGraph provides several checkpointers:

1. **MemorySaver**: In-memory (disappears when program stops)
2. **SqliteSaver**: Persistent storage using SQLite
3. **PostgresSaver**: Production-ready database storage

For this episode, we use `MemorySaver` to keep it simple!

## Next Steps

- Experiment with multiple conversations (different thread IDs)
- Try the different checkpointer types
- Build a chatbot with persistent memory across sessions

## Resources

- [LangGraph Checkpointers](https://langchain-ai.github.io/langgraph/how-tos/persistence/)
- [Memory Management Guide](https://langchain-ai.github.io/langgraph/concepts/#persistence)
