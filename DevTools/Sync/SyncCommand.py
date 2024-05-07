import os

from DevTools.Base.BaseCommand import BaseCommand


class SyncCommand(BaseCommand):
    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        self.get_controllers()
        self.get_entities()
        self.get_i18n()
        self.CacheManager.disconnect()
        print(self.colorization("green", "Sync completed!"))

    def get_controllers(self):
        target_dir = "Controllers"
        paths = [
            f"application/Espo/{target_dir}",
            f"custom/Espo/Custom/{target_dir}",
            f"application/Espo/Modules/*/{target_dir}",
            f"custom/Espo/Modules/*/{target_dir}"
        ]

        self.fetch_paths(paths, target_dir, "Controllers")

    def get_i18n(self):
        target_dir = "Resources/i18n"
        target_languages = ["en_US", "cs_CZ"]
        paths = [
            [f"application/Espo/{target_dir}", target_languages],
            [f"custom/Espo/Custom/{target_dir}", target_languages],
        ]

        self.fetch_paths(paths, target_dir, "i18n", rollback_folders=1)

    def get_entities(self):
        target_dir = "Resources/metadata/entityDefs"
        paths = [
            f"application/Espo/{target_dir}",
            f"custom/Espo/Custom/{target_dir}",
            f"application/Espo/Modules/*/{target_dir}",
            f"custom/Espo/Modules/*/{target_dir}"
        ]

        self.fetch_paths(paths, target_dir, "entityDefs")

    def fetch_paths(self, paths, target_dir, cache_dir, rollback_folders=0):
        target_segments_count = len(target_dir.split('/'))
        for path in paths:
            files_with_details = self.fetch_files([path])
            for full_path, file_name, file_extension in files_with_details:
                segments = full_path.split('/')
                if 'Modules' in segments:
                    module_index = segments.index('Modules') + 1
                    module_name = segments[module_index]
                    cache_folder = f"{cache_dir}/{'.'.join(segments[:module_index])}/{module_name}"
                else:
                    cache_folder = f"{cache_dir}/{'.'.join(segments[:-(target_segments_count + rollback_folders)])}"
                self.cache_files([(full_path, file_name, file_extension)], cache_folder, rollback_folders=rollback_folders)

    def fetch_files(self, paths):
        files_with_details = []

        def process_path(path):
            nonlocal files_with_details
            if isinstance(path, str) and '*' in path:
                base_dir, _, sub_paths = path.partition('*')
                base_dir = base_dir.rstrip('/').replace('\\', '/')
                directories = self.CacheManager.get_instance_file_names(base_dir, return_type='directories')
                for directory in directories:
                    new_path = os.path.join(base_dir, directory) + sub_paths
                    process_path(new_path.replace('\\', '/'))
            elif isinstance(path, str):
                path = path.replace('\\', '/')
                files = self.CacheManager.get_instance_file_names(path, return_type='files')
                files_with_details += files
            elif isinstance(path, list):
                base_dir = path[0].replace('\\', '/')
                target_dirs = path[1]
                for dir_name in target_dirs:
                    full_path = os.path.join(base_dir, dir_name).replace('\\', '/')
                    files = self.CacheManager.get_instance_file_names(full_path, return_type='files')
                    files_with_details += files

        for path in paths:
            process_path(path)

        return files_with_details

    def cache_files(self, files_with_details, cache_folder, rollback_folders=0):
        for full_path, file_name, file_extension in files_with_details:
            full_path = full_path.replace('\\', '/')
            print(full_path, file_name, file_extension)
            path_parts = full_path.split('/')
            if rollback_folders > 0:
                specific_folder = path_parts[-rollback_folders]
                final_cache_path = os.path.join(self.cache_path, cache_folder, specific_folder,
                                                file_name + file_extension).replace('\\', '/')
            else:
                final_cache_path = os.path.join(self.cache_path, cache_folder, file_name + file_extension).replace('\\',
                                                                                                                   '/')

            data = self.CacheManager.get_instance_file(full_path, file_name + file_extension)
            self.FileManager.write_file(final_cache_path, data)
