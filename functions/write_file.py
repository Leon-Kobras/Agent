import os
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([target_dir, working_dir_abs]) != working_dir_abs:
            return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"
        if os.path.isdir(target_dir) == True:
            return f'Error: Cannot write to {file_path} as it is a directory'
        else:
            parent = os.path.dirname(target_dir)
            os.makedirs(parent, exist_ok=True)
            f = open(target_dir, 'w')
            contents = f.write(content)
            if contents:
                return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
    except Exception as e:
        print(f'Error: {e}')
schema_write_file = types.FunctionDeclaration(
    name='write_file',
    description='Write or overwrite files',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='Write or overwrite contents of a file, relative to the working directory (default is the working directory itself)',
            ), 'content': types.Schema(
                type=types.Type.STRING,
                description='Write or overwrite contents of a file, relative to the working directory (default is the working directory itself)')
        },
    ),
)
