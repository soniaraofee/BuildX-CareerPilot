import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is not set."
    )


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def ask_agent(prompt):

    response = client.chat.completions.create(
        model="apodex/apodex-1.1-mini:free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content