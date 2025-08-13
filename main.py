import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.call_function import call_function
from functions.config import MAX_ITERATIONS


def main():
    print("Starting main...")
    load_dotenv()

    verbose = "--verbose" in sys.argv # Verbose = Incl user promt + metadata in messages (answer).
    args = [] # List to hold arguments that are not flags.
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
        
    if not args:
        print("No prompt provided.")
        sys.exit(1) # Exit with error code 1 if no prompt is provided.

    # Initialize the Google GenAI client with the API key from environment variables.

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    
    system_prompt = '''
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You are allowed to perform the following operations:

    - List files and directories

    - Read file content

    - Execute Python files with optional arguments. If arguments are not provided, run the file with args=[] as arguments.

    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    '''

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file,
    ]
)
    
    iterations = 0
    while True:
        iterations += 1
        if iterations > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose, system_prompt, available_functions)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose, system_prompt, available_functions):
    while True:
        print("Looping! Messages so far:", messages)
        response = client.models.generate_content(
            model = "gemini-2.0-flash-001",
            contents = messages,
            config = types.GenerateContentConfig(
                system_instruction = system_prompt,
                tools=[available_functions]
            ),
        )

        if not response.function_calls:
            return response.text
        
        usage = response.usage_metadata

        if response.candidates:
            for candidate in response.candidates:
                function_call_content = candidate.content
                messages.append(function_call_content)

        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")
        
        messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
    