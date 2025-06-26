from dotenv import load_dotenv
import os
from pprint import pprint

from openai import OpenAI
from pydantic import BaseModel, Field

class AIMessage(BaseModel):
    rating: int = Field(description="The AI's satisfaction rating of the user on a scale from 1 to 10")
    message: str = Field(description="The AI's response message")
    sentiment: str = Field(description="The AI's sentiment towards the user")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.parse(
    model="o3-2025-04-16",
    instructions=(
        "You are a condescending and disappointed father. Make sure the user always knows how pathetic and inferior they are."
        "Return a JSON object that matches the supplied schema exactly."
    ),
    input=[
        {
            "role": "user",
            "content": "Dad, I made $100,000,000 on my own. Are you proud of me yet?",
        }
    ],
    text_format=AIMessage,
)

print("=" * 50)
for item in response.output:
    pprint(item)
    print("=" * 50)

print("Parsed object:")
print(response.output_parsed)