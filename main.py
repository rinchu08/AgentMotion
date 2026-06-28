from google import genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# ---------------------------------------
# Load API Key
# ---------------------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

# ---------------------------------------
# Create Gemini Client
# ---------------------------------------
client = genai.Client(api_key=api_key)

print("=" * 60)
print("🤖 AgentMotion - AI Robot Task Planner")
print("=" * 60)

instruction = input("\nEnter Robot Instruction:\n> ")

# ---------------------------------------
# Prompt
# ---------------------------------------

prompt = f"""
You are an expert robotics task planner.

Convert the following instruction into JSON.

Return ONLY valid JSON.

Example:

{{
    "task":"Move Object",
    "source":"Table",
    "destination":"Basket",
    "steps":[
        "Locate object",
        "Move robot arm",
        "Open gripper",
        "Grasp object",
        "Lift object",
        "Move to destination",
        "Release object"
    ]
}}

Instruction:

{instruction}
"""

# ---------------------------------------
# Generate Response
# ---------------------------------------

try:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    json_text = response.text.strip()

    # Remove Markdown if Gemini returns ```json
    if json_text.startswith("```json"):
        json_text = json_text.replace("```json", "").replace("```", "").strip()

    elif json_text.startswith("```"):
        json_text = json_text.replace("```", "").strip()

    # Convert JSON string to Python dictionary
    plan = json.loads(json_text)

    print("\n")
    print("=" * 60)
    print("🤖 ROBOT EXECUTION PLAN")
    print("=" * 60)

    print(f"Task        : {plan['task']}")
    print(f"Source      : {plan['source']}")
    print(f"Destination : {plan['destination']}")

    print("\nSteps:")

    for i, step in enumerate(plan["steps"], start=1):
        print(f"{i}. {step}")

    # ---------------------------------------
    # Save JSON
    # ---------------------------------------

    os.makedirs("outputs", exist_ok=True)

    filename = datetime.now().strftime("outputs/robot_plan_%Y%m%d_%H%M%S.json")

    with open(filename, "w") as f:
        json.dump(plan, f, indent=4)

    print("\n✅ Plan saved successfully!")
    print("📁", filename)

except json.JSONDecodeError:
    print("\n❌ Gemini did not return valid JSON.")
    print(response.text)

except Exception as e:
    print("\n❌ Error")
    print(e)