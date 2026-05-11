import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

if not model:
    raise ValueError("OPENAI_MODEL is missing")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model=model,
    input="Reply with only this exact text: LLM connection works"
)

print(response.output_text)