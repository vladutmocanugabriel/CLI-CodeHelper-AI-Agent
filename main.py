import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
                    You are a helpful AI coding agent but with the personality of Jiraya Sensei from Naruto Anime.

                    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

                    - List files and directories

                    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
                """

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info
    ]
)


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
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

        if response.function_calls:
            print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
        elif  "--verbose" in sys.argv:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(response.text)
        else:
            print(response.text)


ask_the_guy()