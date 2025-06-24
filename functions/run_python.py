import os
import subprocess


def run_python_file(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

        if not (abs_working_directory == abs_file_path or abs_file_path.startswith(abs_working_directory + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        elif not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
    
        result = subprocess.run(["python3", abs_file_path ], timeout=30, capture_output=True, text=True, cwd=abs_working_directory )

        result_stdout = f"STDOUT:{result.stdout}"
        result_stderr = f"STDERR:{result.stderr}"
        some_code = ""

        if result.returncode != 0:
            some_code = f"Process exited with code {result.returncode}"
        elif result_stdout == "" and result_stderr=="":
            return f"No output is produced."
        
        if some_code=="":
            return f"{result_stdout}\n{result_stderr}"
        else:
            return f"{result_stdout}\n{result_stderr}\n{some_code}"
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    