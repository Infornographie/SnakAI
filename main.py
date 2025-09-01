import os, sys, argparse, textwrap 
from dotenv import load_dotenv 
from google import genai 
from google.genai import types
from config import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

#Parsing command line arguments
class FriendlyParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(textwrap.dedent('''\
            Thank you for using SnakAI!
            --------------------------------
            You need to provide a prompt in order to get a response from the Gemini model.
            Example: python main.py "Write your question here"
            You can also add --verbose to get more detailed output.
        '''))
        sys.exit(2)

parser = FriendlyParser()
parser.add_argument("prompt", type=str, help='The question to ask the Gemini model. Should be enclosed in quotes.')
parser.add_argument("--verbose", action="store_true", help="Prints extra info (prompt and token count).")
args = parser.parse_args()

user_prompt = args.prompt
verbose = args.verbose

# Load API key from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Generate a response from the Gemini model
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

for i in range(20):
    try:
        # Call the Gemini model with the current messages and available functions
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
            )
        )
        
        # Print user prompt and token count if verbose
        if verbose and i == 0:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print("")

        # Append LLM's response to messages
        for c in response.candidates:
            messages.append(c.content)

        # If there are function calls in the response, call them
        # and append the results to messages
        # else, print the response text and exit the loop
        if response.function_calls:
            for function_call_part in response.function_calls:
                call = call_function(function_call_part, verbose)
                if not call.parts or not call.parts[0].function_response:
                    raise Exception("Fatal Error: No function response received.")
                part = call.parts[0]
                messages.append(types.Content(role="user", parts=[part]))
        elif response.text: # If there's text in the response, print it and exit
            if verbose:
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print("")
            print(response.text)
            break

    except Exception as e:
        print(f"Error: {e}")
        break