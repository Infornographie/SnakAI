from config import WORKING_DIRECTORY
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

# Create a unified structure that contains both the function and its schema
FUNCTION_REGISTRY = {
    "get_files_info": {
        "function": get_files_info,
        "schema": schema_get_files_info
    },
    "get_file_content": {
        "function": get_file_content,
        "schema": schema_get_file_content
    },
    "run_python_file": {
        "function": run_python_file,
        "schema": schema_run_python_file
    },
    "write_file": {
        "function": write_file,
        "schema": schema_write_file
    }
}

# Generate available_functions from the registry
available_functions = types.Tool(
    function_declarations=[entry["schema"] for entry in FUNCTION_REGISTRY.values()]
)

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name

    # Handle unknown function
    if function_name not in FUNCTION_REGISTRY:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    func = FUNCTION_REGISTRY[function_call_part.name]["function"] # Get the function from the registry
    kwargs = {"working_directory": WORKING_DIRECTORY, **function_call_part.args} # Inject working directory

    # Call the function with the provided arguments
    if verbose:
        print(f" - Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    function_result = func(**kwargs)
    
    # Return the function result in a format compatible with the GenAI API
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )