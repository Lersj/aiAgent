import os

from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))

    if absolute_path.startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(absolute_path) == False:
        return f'Error: "{directory}" is not a directory'

    if os.path.isdir(absolute_path) == True:
        files_info = []
        for file in os.listdir(absolute_path):
            file_path = os.path.join(absolute_path, file)
            is_dir = os.path.isdir(file_path)
            size = os.path.getsize(file_path)
            files_info.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
