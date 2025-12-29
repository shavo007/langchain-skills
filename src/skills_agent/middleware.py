import logging
from typing import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.messages import SystemMessage

from .skills import SKILLS, load_skill

logger = logging.getLogger(__name__)


class SkillMiddleware(AgentMiddleware):
    """Middleware that injects skill descriptions into the system prompt and
    registers the `load_skill` tool with the agent."""

    tools = [load_skill]

    def __init__(self):
        skills_list = [f"- **{s['name']}**: {s['description']}" for s in SKILLS]
        self.skills_prompt = "\n".join(skills_list)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        skills_addendum = (
            f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n"
            "Use the load_skill tool when you need detailed information "
            "about handling a specific type of request."
        )

        if request.system_message is None:
            new_system_message = SystemMessage(content=skills_addendum)
        else:
            content_blocks = getattr(request.system_message, "content_blocks", [])
            new_content = list(content_blocks) + [
                {"type": "text", "text": skills_addendum}
            ]
            new_system_message = SystemMessage(content=new_content)

        logger.debug("System prompt:\n%s", new_system_message.content)

        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)
