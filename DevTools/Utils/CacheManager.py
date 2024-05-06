import os
import json
import paramiko
from dotenv import load_dotenv


class CacheManager:

    def __init__(self, FileManager):
        load_dotenv()
        self.hostname = os.getenv('SSH_HOST')
        self.username = os.getenv('SSH_USER')
        self.password = os.getenv('SSH_PASSWORD')
        self.ssh_client = None
        self.FileManager = FileManager

    def ensure_connection(self):
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password)

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

    @staticmethod
    def get_local_file_names(directory, return_type='files'):
        items = []
        if "*" in directory:
            base_dir = directory.replace("/*", "")
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    file_name, file_extension = os.path.splitext(file)
                    items.append((root, file_name, file_extension))
        else:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_name, file_extension = os.path.splitext(file)
                    if return_type == 'files':
                        items.append((root, file_name, file_extension))
                    elif return_type == 'directories':
                        items.append(root)
        return items

    def get_instance_file(self, file_directory, file_name):
        command = f'cat ~/public_html/{file_directory}/{file_name}'
        print(command)
        output = self.execute_command(command)
        if file_name.endswith('.json'):
            return json.loads(output)
        else:
            return output