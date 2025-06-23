import os

def get_file_content(working_directory, file_path):
    try:      
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

        if not (abs_working_directory == abs_file_path or abs_file_path.startswith(abs_working_directory + os.sep)):#WHY IS THAT os.sep, check!
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        max_file_chars = 10000
        truncated_message = f'[...File "{file_path}" truncated at {max_file_chars} characters]'

        with open(abs_file_path, "r") as file:
            full_file_content = file.read()
            if len(full_file_content) > max_file_chars:
                truncated_file_content = full_file_content[:max_file_chars]+truncated_message
            else:
                truncated_file_content = full_file_content


        return truncated_file_content
                
    except Exception as e:
        return f"Error: {str(e)}"