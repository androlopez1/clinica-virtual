import os
import anthropic
from app.prompts import SYSTEM_PROMPT

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def get_response(messages: list) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return message.content[0].text
