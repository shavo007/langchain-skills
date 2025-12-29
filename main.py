#!/usr/bin/env python3
"""Example: Run the skills agent with a sample query."""

import logging
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # or your LLM of choice

from src.skills_agent import create_skills_agent, example_run

# Load environment variables from .env file
load_dotenv()

# Configure logging to see system prompts
logging.basicConfig(level=logging.WARNING, format="%(name)s - %(message)s")
logging.getLogger("src.skills_agent.middleware").setLevel(logging.DEBUG)


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
    agent = create_skills_agent(model)

    result = example_run(agent)

    print("\n=== Final Result ===\n")
    for message in result["messages"]:
        if hasattr(message, "pretty_print"):
            message.pretty_print()
        else:
            print(f"{message.type}: {message.content}")


if __name__ == "__main__":
    main()
