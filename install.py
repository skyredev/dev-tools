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


def get_user_input(question):
    while True:
        user_input = input(question + " (y/n): ").lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def install_prompt_toolkit():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "prompt_toolkit"])


def copy_files(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)


def add_alias(alias, file_path):
    with open(file_path, 'a') as file:
        file.write(f'\n{alias}\n')


def main():
    if sys.platform == 'win32':
        username = os.getenv('USERNAME')
        home_dir = os.path.join('C:\\Users', username)
        bashrc_path = os.path.join(home_dir, '.bashrc')
    else:
        username = os.getenv('USER')
        home_dir = os.path.expanduser('~')
        bashrc_path = os.path.join(home_dir, '.bashrc')

    apertia_dir = os.path.join(home_dir, '.apertia', 'apertia-tool')
    alias = f'alias apertia-tool="python {os.path.join(apertia_dir, "apertia-tool.py")}"'

    if not check_prompt_toolkit():
        print("prompt_toolkit is not installed.")
        if get_user_input("Do you want to install prompt_toolkit?"):
            install_prompt_toolkit()
        else:
            print("prompt_toolkit is required. Exiting.")
            return

    if get_user_input(
            "Do you want to copy the dev tool home directory and overwrite all in the destination directory?"):
        copy_files('DevTools', os.path.join(apertia_dir, 'DevTools'))
        shutil.copy('apertia-tool.py', apertia_dir)

    if get_user_input("Do you want to add the alias to the bashrc file?"):
        add_alias(alias, bashrc_path)


if __name__ == '__main__':
    main()
