import os

from DevTools.Base.Base_Command import BaseCommand


class SyncCommand(BaseCommand):
    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        self.get_entities_metadata()
        self.get_i18n()
        self.get_tools()
        self.get_services()
        self.get_controllers()
        self.get_entities_php()
        self.CacheManager.disconnect()
        print(self.colorization("green", "Sync completed!"))

    def get_tools(self):
        target_dir = "Tools"
        paths = [
            f"application/Espo/{target_dir}/*",
            f"application/Espo/Modules/*/{target_dir}/*",
            f"custom/Espo/Modules/*/{target_dir}/*"
        ]

        self.fetch_paths(paths, target_dir, "Tools")

    def get_services(self):
        target_dir = "Services"
        paths = [
            f"application/Espo/{target_dir}",
            f"custom/Espo/Custom/{target_dir}",
            f"application/Espo/Modules/*/{target_dir}",
            f"custom/Espo/Modules/*/{target_dir}"
        ]

        self.fetch_paths(paths, target_dir, "Services")

    def get_controllers(self):
        target_dir = "Controllers"
        paths = [
            f"application/Espo/{target_dir}",
            f"custom/Espo/Custom/{target_dir}",
            f"application/Espo/Modules/*/{target_dir}",
            f"custom/Espo/Modules/*/{target_dir}"
        ]

        self.fetch_paths(paths, target_dir, "Controllers")

    def get_entities_php(self):
        target_dir = "Entities"
        paths = [
            f"application/Espo/{target_dir}",
            f"custom/Espo/Custom/{target_dir}",
            f"application/Espo/Modules/*/{target_dir}",
            f"custom/Espo/Modules/*/{target_dir}"
        ]

        self.fetch_paths(paths, target_dir, "Entities")

    def get_i18n(self):
        target_dir = "Resources/i18n"
        target_languages = self.languages
        paths = [
            [f"application/Espo/{target_dir}", target_languages],
            [f"custom/Espo/Custom/{target_dir}", target_languages],
        ]

        self.fetch_paths(paths, target_dir, "i18n")

    def get_entities_metadata(self):
        target_dir = "Resources/metadata/entityDefs"
        paths = [
            f"application/Espo/{target_dir}",
            f"custom/Espo/Custom/{target_dir}",
            f"application/Espo/Modules/*/{target_dir}",
            f"custom/Espo/Modules/*/{target_dir}"
        ]

        self.fetch_paths(paths, target_dir, "entityDefs")

    def fetch_paths(self, paths, target_dir, cache_dir):
        for path in paths:
            files_with_details = self.fetch_files([path])
            for full_path, file_name, file_extension in files_with_details:
                segments = full_path.split('/')
                target_dir_segments_count = len(target_dir.split('/'))

                if 'Modules' in segments:
                    try:
                        modules_index = segments.index('Modules') + 1
                        base_segments = segments[:modules_index]
                        module_name = segments[modules_index]
                        base_cache_path = '.'.join(base_segments).replace('/', '.') + f"/{module_name}"
                        relative_path = '/'.join(segments[
                                                 modules_index + 1 + target_dir_segments_count:])  # +1 for the module name, + target_dir_segments_count for target dir segments
                    except ValueError:
                        base_cache_path = '.'.join(segments).replace('/', '.')
                        relative_path = ''
                else:
                    try:
                        target_index = segments.index(target_dir.split('/')[0])
                        base_segments = segments[:target_index]
                        base_cache_path = '.'.join(base_segments).replace('/', '.')
                        relative_path = '/'.join(segments[target_index + target_dir_segments_count:])
                    except ValueError:
                        base_cache_path = '.'.join(segments).replace('/', '.')
                        relative_path = ''

                # Финальный путь кэша
                cache_folder = f"{cache_dir}/{base_cache_path}/{relative_path}"
                final_cache_path = os.path.join(self.cache_dir, cache_folder, file_name + file_extension).replace('\\',
                                                                                                                  '/')

                self.FileManager.create_directory(os.path.dirname(final_cache_path))
                data = self.CacheManager.get_instance_file(full_path, file_name + file_extension)
                self.FileManager.write_file(final_cache_path, data)

    def fetch_files(self, paths):
        files_with_details = []

        def process_path(path):
            print(self.colorization("magenta", f"Fetching files in path: {path}"))
            nonlocal files_with_details
            if isinstance(path, str) and '*' in path:
                base_dir, _, sub_paths = path.partition('*')
                base_dir = base_dir.rstrip('/').replace('\\', '/')
                root_files = self.CacheManager.get_instance_file_names(base_dir, return_type='files')
                files_with_details += root_files
                directories = self.CacheManager.get_instance_file_names(base_dir, return_type='directories')
                for directory in directories:
                    new_path = os.path.join(base_dir, directory) + sub_paths
                    process_path(new_path.replace('\\', '/'))
            elif isinstance(path, str):
                path = path.replace('\\', '/')
                files = self.CacheManager.get_instance_file_names(path, return_type='files')
                files_with_details += files
                directories = self.CacheManager.get_instance_file_names(path, return_type='directories')
                for directory in directories:
                    process_path(os.path.join(path, directory))
            elif isinstance(path, list):
                base_dir = path[0].replace('\\', '/')
                target_dirs = path[1]
                for dir_name in target_dirs:
                    full_path = os.path.join(base_dir, dir_name).replace('\\', '/')
                    files = self.CacheManager.get_instance_file_names(full_path, return_type='files')
                    files_with_details += files
                    directories = self.CacheManager.get_instance_file_names(full_path, return_type='directories')
                    for directory in directories:
                        process_path(os.path.join(full_path, directory))

        for path in paths:
            process_path(path)

        return files_with_details
