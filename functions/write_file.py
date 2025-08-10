import os


def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    if absolute_path.startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(absolute_path) == False:
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    with open(absolute_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
