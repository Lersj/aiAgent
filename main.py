import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
        
        
    if not args:
        print("No prompt provided.")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    full_prompt = f"{user_prompt}\nUse one paragraph maximum and as few words as possible."

    messages = [
    types.Content(role="user", parts=[types.Part(text=full_prompt)]),
]
    
    generate_content(client, messages, verbose, user_prompt)
def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages
)
    usage = response.usage_metadata
    if verbose:
        print(response.text)
        print("User prompt:", user_prompt)
        print("Prompt tokens:", usage.prompt_token_count)
        print("Response tokens:", usage.candidates_token_count)
    else:
        print(response.text)

if __name__ == "__main__":
    main()
    