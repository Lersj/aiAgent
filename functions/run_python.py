import subprocess
import os

from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified Python file as a standalone script with OPTIONAL arguments passed to it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the Python file.",
		    ),
		    "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="OPTIONAL: A list of optional arguments passed to the Python file.",
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(absolute_path) == False:
        return f'Error: File "{file_path}" not found.'
    if not absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    new_args = ["python", file_path] + args
    completed_process = subprocess.run(new_args, capture_output=True, timeout=30, cwd=working_directory, text=True)
    
    stdout_content = completed_process.stdout
    stderr_content = completed_process.stderr
    exit_code = completed_process.returncode

    if not stdout_content.strip() and not stderr_content.strip():
        return "No output produced."
    output = f"STDOUT:\n{stdout_content}\n\nSTDERR:\n{stderr_content}"
    if exit_code != 0:
        return output + f"\n\nProcess exited with code {exit_code}"
    return output
    