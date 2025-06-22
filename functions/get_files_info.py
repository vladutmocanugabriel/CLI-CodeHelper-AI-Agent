import os


def get_files_info(working_directory, directory=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_path = os.path.abspath(os.path.join(working_directory, directory))
    
        if not ( abs_path == abs_working_directory or abs_path.startswith(abs_working_directory + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(abs_path):
            return f'Error: "{directory}" is not a directory'
    
        directory_items = os.listdir(abs_path)
        directory_tree = {}
        showcase_list = []

        for item in directory_items:
            directory_tree[item] = {}
            file_path = os.path.join(abs_path, item)
            directory_tree[item]["file-size"] = os.path.getsize(file_path)
            directory_tree[item]["is_dir"] = os.path.isdir(file_path)

        for item in directory_tree:
            showcase_list.append(f"- {item}: file_size={directory_tree[item]['file-size']}, is_dir={directory_tree[item]['is_dir']}")

        return "\n".join(showcase_list)

    except Exception as e:
        return f"Error: {str(e)}"