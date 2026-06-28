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

    uploaded_image = st.file_uploader(
        "📷 Upload an Image",
        type=["png", "jpg", "jpeg"]
    )

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

    if instruction.strip() == "" or uploaded_image is None:

        st.warning("Please upload an image and enter an instruction.")

    else:

        try:

            # ============================================
            # Generate Robot Plan
            # ============================================

            with st.spinner("🤖 Gemini Vision is analyzing the image..."):

                plan = generate_robot_plan(
                    instruction,
                    uploaded_image
                )

            st.session_state.plans_generated += 1

            st.success("✅ Robot Plan Generated")

            st.divider()

            # ============================================
            # Objects Detected
            # ============================================

            if "objects_detected" in plan:

                st.header("👀 Objects Detected")

                cols = st.columns(len(plan["objects_detected"]))

                for col, obj in zip(cols, plan["objects_detected"]):

                    with col:
                        st.success(obj)

                st.divider()

            # ============================================
            # Image + Task Summary
            # ============================================

            left, right = st.columns([2, 1])

            with left:

                st.subheader("📷 Uploaded Environment")

                st.image(
                    uploaded_image,
                    use_container_width=True
                )

            with right:

                st.subheader("📋 Task Summary")

                st.metric(
                    "📦 Task",
                    plan.get("task", "N/A")
                )

                st.metric(
                    "📍 Source",
                    plan.get("source", "N/A")
                )

                st.metric(
                    "🎯 Destination",
                    plan.get("destination", "N/A")
                )

            st.divider()

            # ============================================
            # Execution Steps
            # ============================================

            st.header("🤖 Execution Steps")

            for i, step in enumerate(plan["steps"], start=1):

                with st.container():

                    st.info(f"""
### Step {i}

🤖 **Action:** {step.get("action", "-")}

📦 **Object:** {step.get("object", "-")}

📍 **Location:** {step.get("location", "-")}
""")

                    if step.get("target_location"):

                        st.write(
                            f"🎯 **Target:** {step['target_location']}"
                        )

                    st.divider()

            # ============================================
            # Save JSON
            # ============================================

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

# ============================================
# Footer
# ============================================

st.divider()

st.caption(
    "🤖 Built with ❤️ using Python • Streamlit • Gemini 2.5 Flash"
)