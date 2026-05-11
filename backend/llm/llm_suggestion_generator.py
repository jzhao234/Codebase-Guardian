import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def generate_llm_suggestion(selected_context):
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key:
        return {
            "used_llm": False,
            "error": "OPENAI_API_KEY is not set."
        }

    if not model:
        return {
            "used_llm": False,
            "error": "OPENAI_MODEL is not set."
        }

    client = OpenAI(api_key=api_key)

    prompt = {
        "task": "Generate a safe codebase maintenance suggestion.",
        "rules": [
            "Return only valid JSON.",
            "Do not suggest editing files unless old_text and new_text are clear.",
            "Prefer minimal fixes.",
            "Do not invent file paths.",
            "If unsure, choose manual_review."
        ],
        "selected_context": selected_context,
        "required_json_shape": {
            "suggested_action": "string",
            "confidence": "low | medium | high",
            "file_to_edit": "string or null",
            "old_text": "string or null",
            "new_text": "string or null",
            "suggested_fix": "string",
            "reason": "string"
        }
    }

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You are a cautious repo maintenance agent. You generate structured, minimal, verifiable fix suggestions."
            },
            {
                "role": "user",
                "content": json.dumps(prompt)
            }
        ]
    )

    try:
        suggestion = json.loads(response.output_text)
    except json.JSONDecodeError:
        return {
            "used_llm": True,
            "error": "LLM did not return valid JSON.",
            "raw_output": response.output_text
        }

    suggestion["used_llm"] = True
    return suggestion