import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# ============================================
# Load Environment Variables
# ============================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env")
    st.stop()

# ============================================
# Gemini Client
# ============================================

client = genai.Client(api_key=api_key)

# ============================================
# Streamlit Page
# ============================================

st.set_page_config(
    page_title="AgentMotion",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AgentMotion")
st.subheader("AI Robot Task Planner")

st.write(
    "Convert natural language instructions into structured robot execution plans."
)

instruction = st.text_area(
    "Enter Robot Instruction",
    placeholder="Example: Pick up the red bottle from the table and place it in the basket."
)

# ============================================
# Generate Button
# ============================================

if st.button("🚀 Generate Plan"):

    if instruction.strip() == "":
        st.warning("Please enter a robot instruction.")
        st.stop()

    prompt = f"""
You are an expert robotics task planner.

Convert the following instruction into structured JSON.

Return ONLY valid JSON.

Use EXACTLY this format.

{{
    "task":"",
    "source":"",
    "destination":"",
    "steps":[
        {{
            "action":"",
            "object":"",
            "location":""
        }}
    ]
}}

Rules:

- Return ONLY JSON.
- Every step must be a JSON object.
- Never return plain English explanations.

Possible actions:

detect_object
move_to_object
open_gripper
close_gripper
grasp_object
verify_grasp
lift_object
move_to_location
release_object
return_home

Instruction:

{instruction}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        json_text = response.text.strip()

        # Remove markdown if Gemini returns ```json
        if json_text.startswith("```json"):
            json_text = json_text.replace("```json", "").replace("```", "").strip()

        elif json_text.startswith("```"):
            json_text = json_text.replace("```", "").strip()

        plan = json.loads(json_text)

        st.success("✅ Robot Plan Generated")

        st.divider()

        # ============================================
        # Task Information
        # ============================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📦 Task", plan.get("task", "N/A"))

        with col2:
            st.metric("📍 Source", plan.get("source", "N/A"))

        with col3:
            st.metric("🎯 Destination", plan.get("destination", "N/A"))

        st.divider()

        # ============================================
        # Execution Steps
        # ============================================

        st.header("🤖 Execution Steps")

        for i, step in enumerate(plan["steps"], start=1):

            st.subheader(f"Step {i}")

            if isinstance(step, dict):

                st.write("**Action:**", step.get("action", "N/A"))

                if step.get("object"):
                    st.write("**Object:**", step["object"])

                if step.get("location"):
                    st.write("**Location:**", step["location"])

                if step.get("target_location"):
                    st.write("**Target Location:**", step["target_location"])

            else:

                st.write(step)

            st.divider()

        # ============================================
        # Save JSON
        # ============================================

        os.makedirs("outputs", exist_ok=True)

        filename = datetime.now().strftime(
            "outputs/robot_plan_%Y%m%d_%H%M%S.json"
        )

        with open(filename, "w") as f:
            json.dump(plan, f, indent=4)

        st.success(f"💾 Plan saved successfully!")

        with open(filename, "rb") as file:

            st.download_button(
                label="⬇ Download JSON",
                data=file,
                file_name=os.path.basename(filename),
                mime="application/json"
            )

    except json.JSONDecodeError:

        st.error("❌ Gemini did not return valid JSON.")

        st.code(response.text)

    except Exception as e:

        st.error(str(e))