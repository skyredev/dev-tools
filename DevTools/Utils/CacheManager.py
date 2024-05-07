import os
import json
import paramiko
from dotenv import load_dotenv


class CacheManager:

    def __init__(self, FileManager):
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
        self.hostname = os.getenv('SSH_HOST')
        self.username = os.getenv('SSH_USER')
        self.password = os.getenv('SSH_PASSWORD')
        self.ssh_key_path = os.getenv('SSH_KEY_PATH')
        self.ssh_client = None
        self.FileManager = FileManager

    def ensure_connection(self):
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if not self.username or not self.hostname:
                raise Exception('SSH_HOST and SSH_USER environment variables must be set.')
            if self.password is None and self.ssh_key_path is None:
                raise Exception('Either SSH_PASSWORD or SSH_KEY_PATH environment variable must be set.')
            if self.password is None:
                self.ssh_client.connect(
                    self.hostname, username=self.username, key_filename=self.ssh_key_path
                )
            else:
                self.ssh_client.connect(
                    self.hostname, username=self.username, password=self.password
                )

    def disconnect(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None

    def execute_command(self, command):
        self.ensure_connection()
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.read().decode('utf-8')

    def get_instance_file_names(self, directory, return_type='files'):
        command = f'ls -l ~/public_html/{directory}'
        output = self.execute_command(command)
        lines = output.strip().split('\n')
        items = []

        for line in lines:
            parts = line.split()
            if len(parts) > 0:
                type_and_permissions = parts[0]
                name = parts[-1]
                if type_and_permissions[0] == 'd' and return_type == 'directories':
                    items.append(name)
                elif type_and_permissions[0] == '-' and return_type == 'files':
                    file_name, file_extension = os.path.splitext(name)
                    items.append((directory, file_name, file_extension))

        return items

    def fetch_cache(self, directory, extensions: list):

        self.FileManager.create_directory(directory)

        items = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                if file_extension in extensions:
                    full_path = os.path.join(root, file)
                    items.append((full_path, file_name, file_extension))
        return items

    def get_instance_file(self, file_directory, file_name):
        command = f'cat ~/public_html/{file_directory}/{file_name}'
        print(command)
        output = self.execute_command(command)
        if file_name.endswith('.json'):
            return json.loads(output)
        else:
            return output
