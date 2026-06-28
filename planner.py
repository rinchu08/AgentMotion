import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def describe_image(uploaded_image):

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=[
            uploaded_image,
            """
            Describe everything you see in this image.

            Focus on:

            - Objects
            - Colors
            - Positions
            - Table
            - Bottles
            - Cups
            - Baskets
            - Chairs
            - Obstacles

            Return a clear paragraph.
            """
        ]

    )

    return response.text