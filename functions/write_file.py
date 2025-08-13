import os

from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content into a file. If the file and/or directory doesn't exist, it creates them.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to which the function writes the content parameter.",
            ),
		    "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is to be written into target file_path."
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    if absolute_path.startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(absolute_path) == False:
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    with open(absolute_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
