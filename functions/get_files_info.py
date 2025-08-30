import os

def get_files_info(working_directory, directory="."):
    path = os.path.abspath(os.path.join(working_directory, directory))

    # Security check: Ensure the path is within the working directory
    if not path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    
    # List files and directories with their sizes and types
    try:
        files_info = []
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            if os.path.isfile(itempath):
                files_info.append(f"- {item}: file_size={os.path.getsize(itempath)} bytes, is_dir=False")
            elif os.path.isdir(itempath):
                files_info.append(f"- {item}: file_size={os.path.getsize(itempath)} bytes, is_dir=True")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: {str(e)}"