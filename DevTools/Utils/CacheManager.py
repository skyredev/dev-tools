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

    def get_instance_file_names(self, directory):
        command = f'ls ~/public_html/{directory}'  # Pass directory starting after public_html without / (e.g. 'custom/Espo...')
        output = self.execute_command(command)
        file_names = [name.strip('.json\n') for name in output.split()]
        return file_names

    def get_instance_file(self, directory, file_name):
        command = f'cat ~/public_html/{directory}/{file_name}.json'
        output = self.execute_command(command)
        return json.loads(output)
