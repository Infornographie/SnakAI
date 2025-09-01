import os, sys, subprocess
from time import time
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Security check: Ensure the path is within the working directory and is a .py file
    if not path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not file_path.endswith(".py"):
        return f'Error: "{path}" is not a Python file.'
    
    try:
        cmd = [sys.executable, path, *args]
        completed = subprocess.run(cmd, cwd=working_directory, timeout=30, capture_output=True, text=True)
        if completed.returncode != 0:
            return f"Error: Process exited with code {completed.returncode}\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
        if len(completed.stdout) == 0 and len(completed.stderr) == 0:
            return "Error: No output produced."
        return f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
# Schema for the function declaration
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located within the working directory and returns its output. The file must have a .py extension.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python script.",
            ),
        },
    ),
)