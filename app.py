import streamlit as st
import os

from planner import generate_robot_plan
from utils import save_plan

# ============================================
# Streamlit Page Configuration
# ============================================

st.set_page_config(
    page_title="AgentMotion",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# Sidebar
# ============================================

with st.sidebar:

    st.title("🤖 AgentMotion")

    st.markdown("---")

    st.write("### AI Robot Task Planner")

    st.success("Powered by Gemini")

    st.info("Python + Streamlit")

    st.markdown("---")

    if "plans_generated" not in st.session_state:
        st.session_state.plans_generated = 0

    st.metric(
        "Plans Generated",
        st.session_state.plans_generated
    )

# ============================================
# Main Page
# ============================================

st.title("🤖 AgentMotion")

st.subheader("Convert Natural Language into Robot Execution Plans")

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

    else:

        try:

            # Generate Robot Plan
            plan = generate_robot_plan(instruction)

            # Increase Counter
            st.session_state.plans_generated += 1

            st.success("✅ Robot Plan Generated")

            st.divider()

            # ====================================
            # Task Information
            # ====================================

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📦 Task",
                    plan.get("task", "N/A")
                )

            with col2:
                st.metric(
                    "📍 Source",
                    plan.get("source", "N/A")
                )

            with col3:
                st.metric(
                    "🎯 Destination",
                    plan.get("destination", "N/A")
                )

            st.divider()

            # ====================================
            # Execution Steps
            # ====================================

            st.header("🤖 Execution Steps")

            for i, step in enumerate(plan["steps"], start=1):

                with st.container():

                    st.subheader(f"Step {i}")

                    if isinstance(step, dict):

                        st.write(
                            f"**Action:** {step.get('action', 'N/A')}"
                        )

                        if step.get("object"):
                            st.write(
                                f"**Object:** {step['object']}"
                            )

                        if step.get("location"):
                            st.write(
                                f"**Location:** {step['location']}"
                            )

                        if step.get("target_location"):
                            st.write(
                                f"**Target Location:** {step['target_location']}"
                            )

                    else:

                        st.write(step)

                    st.divider()

            # ====================================
            # Save JSON
            # ====================================

            filename = save_plan(plan)

            st.success("💾 Plan Saved Successfully!")

            with open(filename, "rb") as file:

                st.download_button(
                    label="⬇ Download JSON",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="application/json"
                )

        except Exception as e:

            st.error(f"❌ {e}")