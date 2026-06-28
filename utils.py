import json
import os
from datetime import datetime


def save_plan(plan):

    os.makedirs("outputs", exist_ok=True)

    filename = datetime.now().strftime(
        "outputs/robot_plan_%Y%m%d_%H%M%S.json"
    )

    with open(filename, "w") as file:

        json.dump(
            plan,
            file,
            indent=4
        )

    return filename