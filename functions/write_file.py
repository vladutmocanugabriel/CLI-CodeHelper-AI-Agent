import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

        file_path_location = os.path.dirname(abs_file_path)

        if not os.path.exists(file_path_location):
            os.makedirs(file_path_location, exist_ok=True)

        if not (abs_working_directory == abs_file_path or abs_file_path.startswith(abs_working_directory+ os.sep) ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        with open(abs_file_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"
    
