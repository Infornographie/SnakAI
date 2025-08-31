import os
from google.genai import types

def get_file_content(working_directory, file_path):
    path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Ensure the path is within the working directory
    if not path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read and return the file content (up to MAX_CHARS)
    try:
        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                return f'{file_content_string[:-1]}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
    
# Schema for the function declaration
schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of the specified file, constrained to the working directory. If the file exceeds a certain length, it will be truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)