import os

from DevTools.Base.Base_Command import BaseCommand


class Helpers(BaseCommand):
    def __init__(self, values):
        super().__init__(command_file=__file__)
        self.values = values

    def get_cache_path(self, value_name):
        existing_values = []
        for value in self.values:
            if value[1] == value_name:
                existing_values.append(value)
        return existing_values

    def set_cleaner_paths_dict(self, existing_values_list, value_folder):
        cleaner_paths_dict = {}
        for value in existing_values_list:
            if self.cache_dir in value[0]:
                cleaner_paths_dict[value[0]] = value[0].replace(self.cache_dir, "").replace("\\",
                                                                                             "/").replace(
                    f"/{value_folder}/", "")
            else:
                cleaner_paths_dict[value[0]] = value[0].replace(self.current_dir, "").replace("\\",
                                                                                              "/").lstrip(
                    "/")
        return cleaner_paths_dict

    def get_new_value_name(self, local_dir, validator, extension, value_name):
        new_value_name = self.TerminalManager.get_user_input(
            f"Enter the NEW {value_name} name",
            validator=self.Validators.new_name_validator
        )
        while self.file_exists_local_folder(new_value_name, local_dir, extension):
            print(self.colorization("yellow",
                                    f"{value_name.capitalize()} with the same name already exists locally. Please type a different name."))
            new_value_name = self.TerminalManager.get_user_input(
                f"Enter the NEW {value_name} name",
                validator=validator
            )
        return new_value_name

    @staticmethod
    def get_real_value_path(cleaner_paths_dict, extending_value):
        return list(cleaner_paths_dict.keys())[list(cleaner_paths_dict.values()).index(extending_value)]