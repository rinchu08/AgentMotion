ROBOT_PROMPT = """
You are an expert robotics task planner.

Convert the following instruction into structured JSON.

Return ONLY valid JSON.

Use EXACTLY this format.

{
    "task":"",
    "source":"",
    "destination":"",
    "steps":[
        {
            "action":"",
            "object":"",
            "location":""
        }
    ]
}

Rules:

- Return ONLY JSON.
- Every step must be a JSON object.
- Never return explanations.

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