# AI Agents YouTube Series

A comprehensive YouTube series teaching AI agents from scratch using LangGraph. From basic concepts to production-ready systems.

## Series Overview

This series covers everything you need to know about building AI agents:
- Core concepts and fundamentals
- Tool usage and decision making
- Multi-agent systems
- Production deployment and scaling
- Best practices and real-world applications

## Project Structure

```
ai-agents-youtube/
├── requirements.txt               # Shared dependencies for all episodes
├── episode-01-langgraph-basics/   # Episode 1: Your First AI Agent
├── episode-02-.../                # Future episodes
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

## Quick Start

### 1. Clone or Download

```bash
cd ai-agents-youtube
```

### 2. Create Virtual Environment (One Time Setup)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies (One Time Setup)

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

For episodes using LLMs, you'll need an API key. You can either:

**Option 1: Use a .env file (Recommended)**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=your-actual-key-here
```

**Option 2: Export environment variable**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Get your API key at: https://console.anthropic.com/

### 5. Run Any Episode

```bash
# Activate venv if not already active
source venv/bin/activate

# Navigate to episode folder
cd episode-01-langgraph-basics

# Run the code
python 01_simple_agent.py
python 02_agent_with_tool.py
```

## Episodes

### Episode 1: LangGraph Basics - Your First AI Agent
**Status**: ✅ Complete
**Topics**: Graph, Node, Edge, State, Tool usage
**Code**: `episode-01-langgraph-basics/`

Learn the fundamentals by building a simple agent that can use a calculator tool.

### Episode 2: Coming Soon
**Topics**: Multiple tools, conversation memory, error handling

More episodes coming soon!

## Requirements

- Python 3.8+
- Basic Python knowledge
- API key for LLM providers (Anthropic, OpenAI, etc.)

## Resources

- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [LangChain Tools](https://python.langchain.com/docs/integrations/tools/)
- [Anthropic API Docs](https://docs.anthropic.com/)

## Contributing

Found an issue or have a suggestion? Feel free to open an issue or submit a pull request!

## License

MIT License - feel free to use this code for learning and teaching.

## Follow Along

Subscribe to the YouTube channel for new episodes!
