import os

from DevTools.Base.BaseCommand import BaseCommand


class SyncCommand(BaseCommand):
    def __init__(self, local):
        super().__init__(command_file=__file__)
        self.local = local

    def run(self):
        if self.local:
            self.cache_local_files()
        else:
            self.get_entities()
            self.get_i18n()
            self.get_controller()
        self.CacheManager.disconnect()
        print(self.colorization("green", "Sync completed!"))

    def cache_local_files(self):
        self.cache_files(self.CacheManager.get_local_file_names(self.i18n_dir + "/*", return_type='files'), "i18n", rollback_folders=1, is_local=True)
        self.cache_files(self.CacheManager.get_local_file_names(self.entity_defs_dir, return_type='files'), "entityDefs", is_local=True)
        self.cache_files(self.CacheManager.get_local_file_names(self.controllers_dir, return_type='files'), "Controllers/Local Controllers", is_local=True)

    def get_controller(self):
        target_dir = "Controllers"
        paths_Espo = [
            f"application/Espo/{target_dir}",
        ]
        paths_Custom = [
            f"custom/Espo/Custom/{target_dir}",
        ]
        paths_Espo_Modules = [
            f"application/Espo/Modules/*/{target_dir}",
        ]
        paths_Custom_Modules = [
            f"custom/Espo/Modules/*/{target_dir}",
        ]

        espo_controllers = self.fetch_files(paths_Espo)
        custom_controllers = self.fetch_files(paths_Custom)

        espo_modules_controllers = self.fetch_files(paths_Espo_Modules)
        custom_modules_controllers = self.fetch_files(paths_Custom_Modules)

        self.cache_files(espo_controllers, f"{target_dir}/{os.path.dirname(paths_Espo[0]).replace('/', '.')}")

        self.cache_files(custom_controllers, f"{target_dir}/{os.path.dirname(paths_Custom[0]).replace('/', '.')}")

        for full_path, file_name, file_extension in espo_modules_controllers + custom_modules_controllers:
            segments = full_path.split('/')
            main_subfolder = '.'.join(segments[:-2])
            module_name = segments[-2]
            self.cache_files([(full_path, file_name, file_extension)], f"{target_dir}/{main_subfolder}/{module_name}/")

        local_controllers = self.CacheManager.get_local_file_names(self.controllers_dir, return_type='files')
        self.cache_files(local_controllers, "Controllers/Local Controllers", is_local=True)

    def get_i18n(self):
        target_dir = "Resources/i18n"
        target_languages = ["en_US", "cs_CZ"]
        paths = [
            [f"application/Espo/{target_dir}", target_languages],
            [f"custom/Espo/Custom/{target_dir}", target_languages],
        ]

        instance_i18n = self.fetch_files(paths)
        self.cache_files(instance_i18n, "i18n", rollback_folders=1)

        local_i18n = self.CacheManager.get_local_file_names(self.i18n_dir + "/*", return_type='files')
        self.cache_files(local_i18n, "i18n", rollback_folders=1, is_local=True)

    def get_entities(self):
        target_dir = "Resources/metadata/entityDefs"
        paths = [
            f"application/Espo/{target_dir}",
            f"custom/Espo/Custom/{target_dir}",
            f"application/Espo/Modules/*/{target_dir}",
            f"custom/Espo/Modules/*/{target_dir}"
        ]

        instance_entities = self.fetch_files(paths)
        self.cache_files(instance_entities, "entityDefs")

        local_entities = self.CacheManager.get_local_file_names(self.entity_defs_dir, return_type='files')
        for ent in local_entities:
            print(ent)
        self.cache_files(local_entities, "entityDefs", is_local=True)

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

    def cache_files(self, files_with_details, cache_folder, rollback_folders=0, is_local=False):
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

            if file_extension == '.json':
                if not os.path.isfile(final_cache_path):
                    data = self.FileManager.read_file(
                        f"{full_path}/{file_name}{file_extension}") if is_local else self.CacheManager.get_instance_file(
                        full_path, file_name + file_extension)
                    self.FileManager.write_file(final_cache_path, data)
                    print(f"File cached: {file_name}")
                else:
                    existing_data = self.FileManager.read_file(final_cache_path)
                    new_data = self.FileManager.read_file(
                        f"{full_path}/{file_name}{file_extension}") if is_local else self.CacheManager.get_instance_file(
                        full_path, file_name + file_extension)
                    merged_data = self.FileManager.merge_json(existing_data, new_data)
                    self.FileManager.write_file(final_cache_path, merged_data)
                    print(f"File updated: {file_name}")
            else:
                data = self.FileManager.read_file(
                    f"{full_path}/{file_name}{file_extension}") if is_local else self.CacheManager.get_instance_file(
                    full_path, file_name + file_extension)
                self.FileManager.write_file(final_cache_path, data)
                print(f"File {'updated' if os.path.isfile(final_cache_path) else 'cached'}: {file_name}")
