---
name: langchain-patterns
description: LangChain/LangGraph patterns — chains, agents, tools, memory, retrieval, graph workflows
domain: core
tags:
- ai-agent
- infrastructure
- langchain
- memory
- patterns
- self-improvement
- workflow
---

## Overview

LangChain is the most widely used framework for building LLM applications. LangGraph adds stateful, multi-actor workflows with cycles. Together they provide chains, agents, retrieval, memory, and complex workflow orchestration.

## Capabilities

- Build chains with LCEL (LangChain Expression Language)
- Create agents with tool use and reasoning
- Implement RAG with vector stores and retrievers
- Manage conversation memory and context
- Build graph-based workflows with LangGraph
- Integrate with 100+ LLM providers and tools

## When to Use

- Building LLM-powered applications (chatbots, RAG, agents)
- Needing structured chains for multi-step LLM workflows
- Building stateful agent workflows with branching logic
- Implementing retrieval-augmented generation
- Wanting a mature ecosystem with many integrations

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### LCEL Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}"),
])

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"input": "Explain quantum computing in simple terms."})
```

### RAG Pipeline

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough

# Build vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(["doc1 content...", "doc2 content..."], embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# RAG chain
rag_prompt = ChatPromptTemplate.from_template("""
Answer based on context:
{context}

Question: {question}
""")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the return policy?")
```

### Agent with Tools

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

llm = ChatOpenAI(model="gpt-4o")
tools = [search_web, calculator]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = executor.invoke({"input": "What's the square root of the US population?"})
```

### Conversation Memory

```python
from langchain_community.chat_message_history import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

result = with_memory.invoke(
    {"input": "My name is Alice"},
    config={"configurable": {"session_id": "user-123"}},
)
```

### LangGraph State Machine

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]
    next_step: str

def researcher(state: State):
    # Do research
    return {"messages": [("assistant", "Research complete")]}

def writer(state: State):
    # Write content
    return {"messages": [("assistant", "Draft complete")]}

def reviewer(state: State):
    # Review
    return {"messages": [("assistant", "Review done")], "next_step": "end"}

# Build graph
graph = StateGraph(State)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.add_node("reviewer", reviewer)

graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "reviewer")
graph.add_conditional_edges(
    "reviewer",
    lambda s: s["next_step"],
    {"end": END, "writer": "writer"},
)

app = graph.compile()
result = app.invoke({"messages": [], "next_step": ""})
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| LCEL `\|` chain | Simple sequential processing |
| `create_tool_calling_agent` | Agent with function calling |
| `FAISS.from_texts` | Local vector store for RAG |
| `RunnableWithMessageHistory` | Add chat history to chains |
| `StateGraph` | Complex multi-step workflows |
| `add_conditional_edges` | Branching logic in graphs |
| `AgentExecutor` | Run agent with tool loop |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `OutputParserException` | LLM output doesn't match format | Use `StrOutputParser` or fix prompt |
| Agent infinite loop | No valid tool call | Set `max_iterations` on executor |
| Vector store empty | No documents indexed | Check ingestion pipeline |
| Token limit | Context too long | Reduce retriever k or summarize |

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |