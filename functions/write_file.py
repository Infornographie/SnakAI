import os
from google.genai import types

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

# Schema for the function declaration
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to a file, constrained to the working directory. If the file does not exist, it will be created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)