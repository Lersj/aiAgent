import os
import sys

from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("No prompt provided.")
        sys.exit(1)

    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=f'{user_prompt}\nUse one paragraph maximum.'
)

    usage = response.usage_metadata
    print(response.text)
    print("Prompt tokens:", usage.prompt_token_count)
    print("Response tokens:", usage.candidates_token_count)


if __name__ == "__main__":
    main()
