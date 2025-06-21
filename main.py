import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def ask_the_guy():
    if len(sys.argv) < 2:
        print("You did not provide a prompt.")
        sys.exit(1)
    else:
        prompt =  sys.argv[1]
        messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]
        response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages
        )

        if  "--verbose" in sys.argv:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(response.text)
        else:
            print(response.text)


ask_the_guy()