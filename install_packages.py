import subprocess
import os
import re

def extract_package_names(pip_commands):
    """Extract package names from pip install commands"""
    commands = pip_commands.split('\n')
    package_names = []
    for command in commands:
        match = re.search(r'pip install (.+)', command)
        if match:
            package_name = match.group(1).strip()
            package_names.append(package_name)
    return package_names

def install_package_in_env(package_name):
    """Install a single package in the current conda environment"""
    try:
        # Get the pip path from the current conda environment
        pip_path = os.path.join(os.environ['CONDA_PREFIX'], 'Scripts', 'pip.exe')
        
        # Run pip install
        process = subprocess.Popen(
            [pip_path, 'install', package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            return True, f"Successfully installed {package_name}"
        else:
            return False, f"Failed to install {package_name}. Error: {stderr}"
            
    except Exception as e:
        return False, f"Error during installation: {str(e)}"

def process_pip_commands(pip_commands):
    """Process pip install commands and install packages"""
    # First extract package names
    packages = extract_package_names(pip_commands)
    
    # Install each package and collect results
    results = {}
    for package in packages:
        success, message = install_package_in_env(package)
        results[package] = {
            'success': success,
            'message': message
        }
    return results

# Example usage:
"""
# When LLM gives pip commands like:
pip_commands = '''pip install yfinance
pip install numpy'''

results = process_pip_commands(pip_commands)
"""
