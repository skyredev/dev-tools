import os
import sys
import shutil
import subprocess


def check_prompt_toolkit():
    try:
        import prompt_toolkit
        return True
    except ImportError:
        return False


def check_paramiko():
    try:
        import paramiko
        return True
    except ImportError:
        return False


def check_dotenv():
    try:
        import dotenv
        return True
    except ImportError:
        return False


def get_user_input(question):
    while True:
        user_input = input(question + " (y/n): ").lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def copy_files(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)


def add_alias(alias, file_path):
    with open(file_path, 'a') as file:
        file.write(f'\n{alias}\n')


def main():
    home_dir = os.path.expanduser('~')
    apertia_dir = os.path.join(home_dir, '.apertia', 'apertia-tool')
    apertia_tool_path = os.path.join(apertia_dir, "apertia-tool.py")
    apertia_tool_path = apertia_tool_path.replace('\\', '/')

    if sys.platform == 'win32':
        alias = f'alias apertia-tool="winpty python \\"{apertia_tool_path}\\""'
    else:
        alias = f'alias apertia-tool="python \\"{apertia_tool_path}\\""'

    bashrc_path = os.path.join(home_dir, '.bashrc')

    if not check_prompt_toolkit():
        print("prompt_toolkit is not installed.")
        if get_user_input("Do you want to install prompt_toolkit?"):
            install_package("prompt_toolkit")
        else:
            print("prompt_toolkit is required. Exiting.")
            return

    if not check_paramiko():
        print("paramiko is not installed.")
        if get_user_input("Do you want to install paramiko?"):
            install_package("paramiko")
        else:
            print("paramiko is required. Exiting.")
            return

    if not check_dotenv():
        print("dotenv is not installed.")
        if get_user_input("Do you want to install dotenv?"):
            install_package("python-dotenv")
        else:
            print("dotenv is required. Exiting.")
            return

    if get_user_input(
            "Do you want to copy the dev tool home directory and overwrite all in the destination directory?"):
        copy_files('DevTools', os.path.join(apertia_dir, 'DevTools'))
        shutil.copy('apertia-tool.py', apertia_dir)

    if get_user_input("Do you want to add the alias to the bashrc file?"):
        add_alias(alias, bashrc_path)

    if sys.platform == 'win32' and get_user_input("Do you want to add the alias to the PowerShell profile?"):
        profile_path = os.path.join(home_dir, 'Documents', 'WindowsPowerShell', 'Microsoft.PowerShell_profile.ps1')
        powershell_alias = f"function apertia-tool {{ python '{apertia_tool_path}' }}"
        add_alias(powershell_alias, profile_path)


if __name__ == '__main__':
    main()
    print("Installation completed.")
