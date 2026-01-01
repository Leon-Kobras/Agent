import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([target_dir, working_dir_abs]) != working_dir_abs:
            return f"Error: Cannot execute '{file_path}' as it is outside the permitted working directory"
        if not os.path.isfile(target_dir):
            return f"Error: '{file_path}' does not exist or is not a regular file"
        if not target_dir.endswith('.py'):
            return f"Error: '{file_path}' is not a Python file"
        command = ['python', target_dir]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return 'Process exited with code X'
        if result.stdout == None and result.stderr == None:
            return 'No output produced'
        else:
            if result.stdout:
                return f'STDOUT: {result.stdout}'
            if result.stderr:
                return f'STDERR: {result.stderr}'
        return result
    except Exception as e:
        return f'Error: executing Python file: {e}'
schema_run_python_file = types.FunctionDeclaration(
    name='run_python_file',
    description='Execute Python files with optional arguments',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='Execute Python files with optional arguments, relative to the working directory (default is the working directory itself)',
            ), 'args': types.Schema(type=types.Type.ARRAY, description='Execute Python files with optional arguments, relative to the working directory (default is the working directory itself)'), 'args': types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description='Execute Python files with optional arguments, relative to the working directory (default is the working directory itself)')
        },
    ),
)
