import os
from google.genai import types

def write_file(working_directory, file_path, content):

    joined_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_dir = os.path.abspath(working_directory)
    if not joined_path.startswith(abs_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:

        target_dir = os.path.dirname(joined_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
   
        with open(joined_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite file. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to where the file is located, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The new contents of the file.",
            ),
        },
    ),
)