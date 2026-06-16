from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.config import settings
from app.prompts.system import SYSTEM_PROMPT
from app.prompts.features.example import EXAMPLE_PROMPT


@dataclass
class LLMResponse:
    content: str
    structured_data: dict | None = None


FEATURE_PROMPTS: dict[str, str] = {
    "example": EXAMPLE_PROMPT,
}


class LLMService:
    def __init__(self):
        self._llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.llm_api_key,
            temperature=0.7,
        )

    async def generate(
        self,
        feature: str,
        user_input: str,
        user_context: dict,
    ) -> LLMResponse:
        feature_prompt = FEATURE_PROMPTS.get(feature, "")

        messages = [
            SystemMessage(content=SYSTEM_PROMPT.format(user_context=user_context)),
        ]

        if feature_prompt:
            messages.append(SystemMessage(content=feature_prompt))

        messages.append(HumanMessage(content=user_input))

        result = await self._llm.ainvoke(messages)
        content = result.content if hasattr(result, "content") else str(result)

        return self._parse_response(content)

    def _parse_response(self, content: str) -> LLMResponse:
        structured_data = None
        text = content

        if "```json" in content:
            parts = content.split("```json")
            if len(parts) > 1:
                json_part = parts[1].split("```")[0].strip()
                import json
                try:
                    structured_data = json.loads(json_part)
                    text = parts[0].strip()
                except json.JSONDecodeError:
                    pass

        return LLMResponse(content=text, structured_data=structured_data)
