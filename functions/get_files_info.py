import os
from google.genai import types
def get_files_info(working_directory, directory='.'):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs:

            if not os.path.isdir(target_dir):
                return f"Error: '{directory}' is not a directory"
            items = os.listdir(target_dir)
            fil = []
            for item in items:
                direct = os.path.join(target_dir, item)
                lif = f'- {item}: file_size={os.path.getsize(direct)}, is_dir={os.path.isdir(direct)}'
                fil.append(lif)
            mov = '\n'.join(fil)
            return mov
        if os.path.commonpath([target_dir, working_dir_abs]) != working_dir_abs:
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    except Exception as e:
        print(f'Error: {e}')
schema_get_files_info = types.FunctionDeclaration(
    name='get_files_info',
    description='Lists files in a specified directory relative to the working directory, providing file size and directory status',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'directory': types.Schema(
                type=types.Type.STRING,
                description='Directory path to list files from, relative to the working directory (default is the working directory itself)',
            ),
        },
    ),
)
