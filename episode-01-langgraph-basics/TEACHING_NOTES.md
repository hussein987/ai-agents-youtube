# Teaching Notes - Episode 1: LangGraph Basics

## Video Structure (10-15 minutes)

### Opening (1-2 min)
**Hook**: "By the end of this video, you'll build an AI agent that can solve math problems by deciding when to use a calculator - all in less than 50 lines of code."

**What is an AI Agent?**
- Not just a chatbot that responds
- An agent that can USE TOOLS
- Can make DECISIONS
- Can take ACTIONS

**Show the end result first**: Run `02_agent_with_tool.py` to show what we're building

---

### Part 1: Core Concepts (2-3 min)

**Slide 1**: The 4 Core Concepts (use Gamma.app for this)
```
┌─────────────────────────────────────┐
│  🔷 GRAPH = Workflow                │
│  🔷 NODE = Function (does work)     │
│  🔷 EDGE = Connection (flow)        │
│  🔷 STATE = Data (shared memory)    │
└─────────────────────────────────────┘
```

**Analogy**: "Think of it like a factory assembly line"
- State = the product moving through
- Nodes = workers doing specific tasks
- Edges = conveyor belts
- Graph = the entire factory layout

---

### Part 2: Build Simple Agent (3-4 min)

**Open `01_simple_agent.py` in your editor**

**Talk through each step as you show the code:**

1. **State Definition** (Line 19-21)
   - "State is just a dictionary"
   - "Think of it as shared memory"
   - Show the TypedDict

2. **Create a Node** (Line 25-35)
   - "A node is just a Python function"
   - "Takes state in, returns state out"
   - Show the greeting_node function

3. **Build the Graph** (Line 39-53)
   - "Now we connect everything"
   - Show: StateGraph → add_node → add_edge → compile
   - "It's like connecting LEGO blocks"

4. **Run it** (Line 57-73)
   - Execute the script
   - Show the output
   - "That's it! You've built an agent!"

**Key Takeaway**: "This is the foundation. Every complex agent follows this same pattern."

---

### Part 3: Add Real AI + Tools (4-5 min)

**Open `02_agent_with_tool.py`**

**Progressive explanation:**

1. **The Tool** (Line 27-40)
   - "A tool is just a function with @tool decorator"
   - "The LLM can 'see' this and call it when needed"
   - Show the multiply function

2. **The LLM Node** (Line 54-70)
   - "Instead of hardcoded logic, we call Claude"
   - Show: llm.bind_tools([multiply])
   - "We're giving the AI access to our tool"

3. **The Router** (Line 76-89)
   - "This is the decision maker"
   - "Does the LLM want to use a tool? Or answer directly?"
   - Show the conditional logic

4. **The Graph Structure** (Line 95-119)
   - **Draw this live or show a slide:**
   ```
   START → LLM → [Router]
              ↓         ↓
           TOOLS      END
              ↓
           (back to LLM)
   ```
   - "Notice the LOOP - that's the key!"
   - "LLM → Tools → LLM → Answer"

5. **Run it** (Line 124-164)
   - **RUN THE SCRIPT LIVE**
   - Show test 1: Simple greeting (no tool)
   - Show test 2: Math question (uses tool!)
   - Point out the prints: "🤔 LLM wants to use a tool..."

**The Magic Moment**: When the multiply tool gets called
- "See that? The LLM decided it needed help"
- "It called the tool on its own"
- "Then used the result to answer"
- "That's an AI agent!"

---

### Part 4: What Just Happened? (2-3 min)

**Explain the flow with a real example:**

```
User: "What is 234 times 567?"
  ↓
LLM Node: "Hmm, I need to calculate this"
  ↓
Router: "LLM has tool_calls → go to TOOLS"
  ↓
Tools Node: multiply(234, 567) = 132,678
  ↓
Back to LLM: "The answer is 132,678!"
  ↓
END
```

**Why this architecture matters:**
- Scalable: Add more tools easily
- Flexible: LLM decides when to use them
- Powerful: Foundation for complex agents

---

### Closing (1-2 min)

**Recap:**
- ✅ Learned 4 core concepts (Graph, Node, Edge, State)
- ✅ Built a simple agent
- ✅ Built an agent with tools
- ✅ Saw how LLMs make decisions

**Challenge**: "Try adding a divide tool - can you do it?"

**Next Episode Teaser**:
"Next time, we'll build an agent that can:
- Use MULTIPLE tools
- Remember conversation history
- Handle errors gracefully
- And we'll explore conditional branching"

**Call to Action**:
- "Code is in the description"
- "Questions in the comments"
- "Subscribe for the next episode"

---

## Presentation Tips

### DO's:
- ✅ Run code LIVE (not just screenshots)
- ✅ Make mistakes and fix them (shows real development)
- ✅ Use print statements to show what's happening
- ✅ Zoom in on key code sections
- ✅ Use analogies (factory, LEGO, assembly line)

### DON'Ts:
- ❌ Read the documentation word-for-word
- ❌ Spend too long on setup/installation
- ❌ Assume viewers know LangChain already
- ❌ Skip running the actual code
- ❌ Make it too theoretical

### Energy Points:
- **Start HIGH**: Show the end result to hook them
- **Middle STEADY**: Clear explanations, one concept at a time
- **End HIGH**: The "aha!" moment when they see it work

---

## Slide Recommendations (Gamma.app)

**Slide 1**: Title
- "Episode 1: Your First AI Agent with LangGraph"
- Subtitle: "From Zero to Working Agent in 15 Minutes"

**Slide 2**: What is an AI Agent?
- Simple diagram: User → Agent → Tools → Answer

**Slide 3**: The 4 Core Concepts
- Graph, Node, Edge, State with icons/visuals

**Slide 4**: The Agent Loop
- Flow diagram: LLM → Router → Tools → LLM

**Slide 5**: Next Episode Teaser
- Bullets of what's coming

---

## Common Questions (anticipate these)

**Q: "Why LangGraph instead of just using the OpenAI API?"**
A: "Great question! LangGraph gives you CONTROL over the workflow. With just API calls, you're manually managing everything. LangGraph handles the loop for you."

**Q: "Can I use OpenAI instead of Claude?"**
A: "Absolutely! Just swap the import - I'll show you in the README."

**Q: "What if I want to add more tools?"**
A: "Just create more @tool functions and add them to the bind_tools list. We'll do exactly that in Episode 2!"

**Q: "Do I need to know Python well?"**
A: "Basic Python helps, but I'm explaining everything. If you can write functions, you're good!"

---

## Code Demo Checklist

Before recording:
- [ ] Test both scripts work
- [ ] API key is set
- [ ] Terminal is clean and readable
- [ ] Code editor font is large enough
- [ ] No sensitive info in terminal history
- [ ] Have the README open in a browser
- [ ] Test the "challenge" yourself (add divide tool)

During demo:
- [ ] Zoom in on code
- [ ] Highlight key lines
- [ ] Run each script
- [ ] Show the output clearly
- [ ] Point out the prints that show agent thinking

---

## Timing Breakdown

| Section | Time | Focus |
|---------|------|-------|
| Hook + Intro | 1-2 min | Show end result, promise |
| Core concepts | 2-3 min | 4 concepts with analogy |
| Simple agent | 3-4 min | Code walkthrough + run |
| Agent with tools | 4-5 min | Progressive build + run |
| Explanation | 2-3 min | What happened? Why? |
| Closing | 1-2 min | Recap + challenge + teaser |
| **TOTAL** | **13-19 min** | **Aim for 15 min** |

---

## Episode Variants

If your audience is more advanced:
- Skip the simple agent, go straight to tools
- Add more advanced concepts (checkpointing, streaming)
- Show how to visualize the graph

If your audience is complete beginners:
- Spend more time on Python basics (TypedDict, decorators)
- Show pip install step by step
- Explain API keys more thoroughly

**Recommendation**: Aim for the middle - accessible but not boring for advanced folks.
