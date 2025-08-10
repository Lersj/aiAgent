import os

from .config import MAX_CHARS

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