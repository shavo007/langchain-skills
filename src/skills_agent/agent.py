import uuid

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from .middleware import SkillMiddleware


def create_skills_agent(model, system_prompt: str | None = None):
    """Create an agent configured with SkillMiddleware and a checkpointer.

    Args:
        model: a LangChain chat model instance (e.g., ChatOpenAI or ChatAnthropic)
        system_prompt: optional base system prompt
    Returns:
        A configured agent instance
    """
    if system_prompt is None:
        system_prompt = (
            "You are a SQL query assistant that helps users "
            "write queries against business databases."
        )

    agent = create_agent(
        model,
        system_prompt=system_prompt,
        middleware=[SkillMiddleware()],
        checkpointer=InMemorySaver(),
    )
    return agent


def example_run(agent):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Write a SQL query to find all customers "
                        "who made orders over $1000 in the last month"
                    ),
                }
            ]
        },
        config,
    )

    return result
