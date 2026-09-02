import os
import anthropic
from app.prompts import SYSTEM_PROMPT

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def get_response(messages: list) -> str:
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        thinking={"type": "disabled"},  # chat sin herramientas: no necesita razonamiento extendido
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return next(block.text for block in message.content if block.type == "text")
