import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    joined_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_dir = os.path.abspath(working_directory)
    if not joined_path.startswith(abs_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    
    try:
        with open(joined_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) >= MAX_CHARS:
            return f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a file, up to 10000 characters. Constrained to the working directory.",
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