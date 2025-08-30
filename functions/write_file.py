import os

def write_file(working_directory, file_path, content):
    path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Ensure the path is within the working directory
    if not path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        os.mknod(path)
    
    # Write content to the file
    try:
        with open(path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"