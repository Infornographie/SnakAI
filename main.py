import os, sys, argparse, textwrap 
from dotenv import load_dotenv 
from google import genai 
from google.genai import types

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

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

# Print the response
if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print("")
    print(response.text)
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)