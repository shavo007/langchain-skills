# Skills Agent: SQL Assistant with Progressive Disclosure

This is a LangChain agent implementation that demonstrates **progressive disclosure** - a context management technique where an agent loads specialized skills (instructions) on-demand rather than all upfront.

The agent is configured to help write SQL queries across different business domains (sales analytics, inventory management) by loading only the relevant database schema and business logic when needed.

## Project Structure

```
src/skills_agent/
├── __init__.py          # Package exports
├── skills.py            # Skill definitions and load_skill tool
├── middleware.py        # SkillMiddleware for system prompt injection
└── agent.py             # Agent factory functions
main.py                  # Example script
pyproject.toml          # Project dependencies (uv-compatible)
```

## Quick Start

### 1. Install with `uv`

If you don't have `uv` installed, install it first:
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (using PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Clone or navigate to this repository, then install dependencies:

**For OpenAI (recommended):**
```bash
uv sync
uv add "langchain[openai]"
```

**For Anthropic:**
```bash
uv sync
uv add "langchain[anthropic]"
```

**For other providers, see:**
- [LangChain integrations](https://python.langchain.com/docs/integrations/chat)

### 2. Set up your LLM API Key

Export your API key as an environment variable:

```bash
# For OpenAI
export OPENAI_API_KEY="sk-..."

# For Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or create a `.env` file in the project root:
```env
OPENAI_API_KEY=sk-...
```

Then load it in your shell:
```bash
source .env
```

### 3. Run the Example

```bash
uv run main.py
```

Expected output: The agent will receive a query about customers with high-value orders. It will recognize the need for sales analytics, call `load_skill("sales_analytics")`, and then generate a SQL query based on the loaded schema and business logic.

## How It Works

1. **System Prompt Injection**: `SkillMiddleware` injects lightweight skill descriptions into the agent's system prompt
2. **On-Demand Loading**: When the agent needs details, it calls `load_skill(skill_name)` to get the full database schema and business logic
3. **Context Efficiency**: Only relevant skills are loaded, reducing token usage compared to loading all schemas upfront

```bash
  # Example System Prompt Structure:
  [
    {
      'type': 'text',
      'text': 'You are a SQL query assistant that helps users write queries against business databases.'
    },
    {
      'type': 'text',
      'text': '## Available Skills\n\n
        - **sales_analytics**: Database schema and business logic for sales data analysis...
        - **inventory_management**: Database schema and business logic for inventory tracking...\n\n
        Use the load_skill tool when you need detailed information about handling a specific type of request.'
    }
  ]
```

## Defining Custom Skills

Edit `src/skills_agent/skills.py` to add new skills:

```python
SKILLS: list[Skill] = [
    {
        "name": "your_skill_name",
        "description": "Brief 1-2 sentence description shown to the agent upfront",
        "content": "Full detailed content: database schemas, business logic, examples, etc.",
    },
]
```

## Using the Agent Programmatically

```python
from langchain_openai import ChatOpenAI
from src.skills_agent import create_skills_agent

model = ChatOpenAI(model="gpt-4o-mini", api_key="sk-...")
agent = create_skills_agent(model, system_prompt="Your custom prompt...")

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Your query here..."}
        ]
    },
    {"configurable": {"thread_id": "unique-id"}}
)

for message in result["messages"]:
    print(message)
```

## Advanced Features

### Custom State & Constraints

For more control, you can track loaded skills and enforce constraints (e.g., "load skill before using a tool"):
- See the optional **Advanced: Add constraints with custom state** section in the original tutorial
- Implement a custom state schema extending `AgentState`
- Modify `load_skill` to update state when a skill is loaded

### Monitoring with LangSmith

Set environment variables to enable tracing:
```bash
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

Then all agent invocations will be logged to [LangSmith](https://smith.langchain.com) for inspection and debugging.

## References

- [LangChain Skills Pattern Tutorial](https://docs.langchain.com/docs/langchain_community_docs/tutorials)
- [Progressive Disclosure Guide](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
