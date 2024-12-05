import subprocess
import os
import re
from concurrent.futures import ThreadPoolExecutor

def extract_missing_packages(error_text):
    """Extract missing package names from error messages"""
    missing_packages = []
    
    # Common error patterns
    patterns = [
        r"No module named '(.+?)'",  # Most common error
        r"ModuleNotFoundError: No module named '(.+?)'",
        r"ImportError: No module named (.+)",
        r"ImportError: Failed to import (.+?) because",
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, error_text)
        for match in matches:
            package = match.group(1)
            # Clean up package name (get base package)
            base_package = package.split('.')[0]
            if base_package not in missing_packages:
                missing_packages.append(base_package)
    
    return missing_packages

def wrap_code_with_try_except(code_text):
    # Split the original code into lines
    code_lines = code_text.split('\n')
    
    # Properly indent each line, ignoring empty lines
    indented_lines = []
    for line in code_lines:
        if line.strip():  # Only indent non-empty lines
            indented_lines.append('    ' + line)
        else:
            indented_lines.append(line)
    
    # Join the indented lines
    indented_code = '\n'.join(indented_lines)
    
    # Wrap the indented code in try-except block
    wrapped_code = f"""try:
    from youtube_surfer import search_youtube
    from access_gmail import check_new_mail,list_mail_accounts,switch_accounts
    from feedback_mechanisms import get_clarification
    from home_automation import ac_control
{indented_code}
except ImportError as e:
    print(f"ImportError: {{str(e)}}")
except Exception as e:
    print(f"Error: {{str(e)}}")"""
    
    return wrapped_code

def run_process(code_text):
    end_backtick = code_text.find('```')
    if end_backtick != -1:
        code_text = code_text[:end_backtick]
    
    wrapped_code = wrap_code_with_try_except(code_text)
    script_path = "temp_execute.py"
    
    with open(script_path, 'w') as file:
        file.write(wrapped_code)
    
    try:
        python_path = os.path.join(os.environ['CONDA_PREFIX'], 'python.exe')
        process = subprocess.Popen(
            [python_path, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        result = {
            'output': [],     # For normal printed output
            'errors': [],     # For errors including missing packages
            'type': 'success' # Can be 'success', 'error', or 'missing_packages'
        }
        
        # Handle normal output first
        if stdout:
            # Split stdout into lines and filter empty lines
            printed_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
            
            # Separate error messages from normal output
            normal_output = []
            error_output = []
            
            for line in printed_lines:
                if "Error:" in line:
                    error_output.append(line)
                else:
                    normal_output.append(line)
            
            # Store normal output
            if normal_output:
                result['output'] = normal_output
                print("Program output:", '\n'.join(normal_output))
            
            # If there were error messages in stdout
            if error_output:
                result['type'] = 'error'
                result['errors'].extend(error_output)
        
        # Handle stderr and missing packages
        if stderr:
            print("Errors:", stderr)
            missing_packages = extract_missing_packages(stderr)
            if missing_packages:
                result['type'] = 'missing_packages'
                result['errors'] = missing_packages
            else:
                result['type'] = 'error'
                result['errors'].append(stderr.strip())

        # Special case for pip commands
        if "pip " in code_text:
            result['type'] = 'package_installation_success'
            result['errors'] = []
        
        return result
            
    except Exception as e:
        print("There was an error in running the code")
        print(e)
        return {
            'output': [],
            'errors': [str(e)],
            'type': 'error'
        }




def exec_python(code_text):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(run_process, code_text)
        return future.result()
