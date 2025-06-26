from typing import List
from dotenv import load_dotenv
import os
from openai import OpenAI
from pydantic import BaseModel
from pprint import pprint
import json
from xml.dom.minidom import Attr

class EntitiesModel(BaseModel):
    attributes: List[str]
    colors: List[str]
    animals: List[str]

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with client.responses.stream(
    model="gpt-4.1",
    input=[
        {"role": "system", "content": "Extract entities from the input text"},
        {
            "role": "user",
            "content": "The quick brown fox jumps over the lazy dog with piercing blue eyes",
        },
    ],
    text_format=EntitiesModel,
) as stream:
    for event in stream:
        if event.type == "response.refusal.delta":
            print(event.delta, end="")
        elif event.type == "response.output_text.delta":
            print(event.delta, end="")
        elif event.type == "response.error":
            print(event.error, end="")
        elif event.type == "response.completed":
            print("\n")
            print("=" * 50)
            print("Completed")
            print("=" * 50)
            print("\n")
            pprint(json.dumps(event.response.output[0].model_dump(), indent=2))
            print("=" * 50)

    final_response = stream.get_final_response()
    
    # Extract the structured Pydantic model instance
    parsed_model = final_response.output[0]
    
    # Pretty-print as indented JSON
    print("=" * 50)
    print(json.dumps(parsed_model.model_dump(), indent=2))
    print("=" * 50)
