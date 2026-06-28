import os
import json

from dotenv import load_dotenv
from google import genai

from prompts import ROBOT_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_robot_plan(instruction):

    prompt = ROBOT_PROMPT.replace(
    "{instruction}",
    instruction
)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    json_text = response.text.strip()

    if json_text.startswith("```json"):
        json_text = json_text.replace("```json", "").replace("```", "").strip()

    elif json_text.startswith("```"):
        json_text = json_text.replace("```", "").strip()

    plan = json.loads(json_text)

    return plan