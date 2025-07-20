import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):

    joined_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_dir = os.path.abspath(working_directory)
    if not joined_path.startswith(abs_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_path):
        return f'Error: File "{file_path}" not found.'
    
    py_check = joined_path.split(".")
    if not py_check[-1] == "py":
        return f'Error: "{file_path}" is not a Python file.'
    
    target_dir = os.path.dirname(joined_path)
    
    try:
        result = subprocess.run(
            ["python3", joined_path],
            stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE,
            cwd = target_dir,
            timeout = 30)
        
        if len(result.stdout.decode()) < 1 and len (result.stderr.decode()) < 1:
            return "No output produced"
        if result.returncode != 0:
            return f"STDOUT:{result.stdout.decode()} \n STDERR:{result.stderr.decode()} \n Process exited with code {result.returncode}"
        return f"STDOUT:{result.stdout.decode()} \n STDERR:{result.stderr.decode()}"
       

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the designated Python file with optional arguments. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to where the file is located, relative to the working directory.",
            ),
        },
    ),
)