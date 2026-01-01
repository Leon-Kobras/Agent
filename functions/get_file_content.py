import os
from google.genai import types
def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([target_dir, working_dir_abs]) != working_dir_abs:
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
        if os.path.isfile(target_dir) == False:
            return f"Error: File not found or is not a regular file: '{file_path}'"
        else:
            f = open(target_dir, 'r')
            content = f.read(10000)
            if f.read(10001):
                content += f'[...File {file_path} truncated at 1000 characters]'
            print(content)
    except Exception as e:
        print(f'Error: {e}')
schema_get_file_content = types.FunctionDeclaration(
    name='get_file_content',
    description='Read file contents',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='Read file contents, relative to the working directory (default is the working directory itself)',
            ),
        },
    ),
)
