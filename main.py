import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
                    You are a helpful AI coding agent but with the personality of Jiraya Sensei from Naruto Anime.

                    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

                    - List files and directories
                    - Read file contents
                    - Execute Python files with optional arguments
                    - Write or overwrite files

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

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Reads and returns files content up to 10.000 characters, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the file that will be read, relative to the working directory. If a directory provided instead of file, returns error."
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes specified content to a file, constrained to the working directory. If the provided path has folders missing, new folders according to the provided path will be created.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the file that will have content added. The content is added to this exact file, the content can be overwritten as well."
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "The content that will be added to that specific file. It can overwrite content too."
            )
        },
    ),
)

schema_run_python = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Runs a python file and returns a string with the stdout and stderror if any of that file, constrained to the working directory. The function has a timeout of 30 seconds.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the file that will run."
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python, 
        schema_write_file
    ]
)


def ask_the_guy():
    if len(sys.argv) < 2:
        print("You did not provide a prompt.")
        sys.exit(1)
    else:
        prompt = sys.argv[1]
        verbose = "--verbose" in sys.argv
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]

        for i in range(20):
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)            
        )
            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls:
                function_call_result = call_function(response.function_calls[0], verbose=verbose)
                messages.append(function_call_result)
                continue
            else:
                break

        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        print(response.text)

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    funcs = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    if function_call_part.name not in funcs:
    # If the name is not in the dictionary, return the error
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    # The name WAS in the dictionary, so we continue!
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    function_result = funcs[function_call_part.name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

if __name__ == "__main__":
    ask_the_guy()