from dotenv import load_dotenv
load_dotenv()
import os
import requests
from google import genai
from google.genai import types

client = genai.Client()

# 1. Fetch the binary bytes of the image
image_url = "https://plus.unsplash.com/premium_photo-1677706394411-d3f06c3c2458?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8anBlZ3xlbnwwfHwwfHx8MA%3D%3D"
image_response = requests.get(image_url)

if image_response.status_code == 200:
    image_bytes = image_response.content
    
    # 2. Package it using the official Google GenAI schema structure
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            "Generate a Caption for the image in about 50 words",
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ]
    )
    print(response.text)
else:
    print("Failed to download image from the provided URL.")