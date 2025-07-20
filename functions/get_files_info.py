import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory=None):
    joined_dir = os.path.abspath(os.path.join(working_directory, directory))
    abs_dir = os.path.abspath(working_directory)
    if not joined_dir.startswith(abs_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(joined_dir):
        return f'Error: "{directory}" is not a directory'

    dir_contents = os.listdir(joined_dir)
    file_info_list = []

    try:
        for item in dir_contents:
            file_path = os.path.join(joined_dir, item)
            file_info = f"- {item}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}"
            file_info_list.append(file_info)
        dir_info = "\n".join(file_info_list)
    except Exception as e:
        return f"Error: {str(e)}"
    
    return dir_info

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