import os
import json

from dotenv import load_dotenv
from google import genai
from PIL import Image

from prompts import ROBOT_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_robot_plan(instruction, uploaded_image):

    prompt = ROBOT_PROMPT.replace(
        "<INSTRUCTION>",
        instruction
    )

    image = Image.open(uploaded_image)

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=[
            image,
            prompt
        ]

    )

    json_text = response.text.strip()

    if json_text.startswith("```json"):
        json_text = json_text.replace("```json", "").replace("```", "").strip()

    elif json_text.startswith("```"):
        json_text = json_text.replace("```", "").strip()

    return json.loads(json_text)
    