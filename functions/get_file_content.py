import os

from .config import MAX_CHARS
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of the file, truncated to 10000 characters if the file is longer than 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file from which you want to read the content.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    if absolute_path.startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(absolute_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(absolute_path) as f:
        data = f.read()

        if len(data) > MAX_CHARS:
            return data[:MAX_CHARS] + f'... File "{file_path}" truncated at {MAX_CHARS} characters'
    return data