import os


class PathManager:
    def __init__(self, current_dir):
        self.current_dir = current_dir
        self.resources_dir = os.path.join(self.current_dir, 'src/backend/Resources')
        self.backend_dir = os.path.join(self.current_dir, 'src/backend')

    def get_service_path(self, service_name):
        return os.path.join(self.backend_dir, f"Services/{service_name}.php")

    def get_handler_path(self, entity_name, button_name):
        return os.path.join(self.current_dir, f"src/client/src/handlers/{entity_name}/{button_name}-handler.js")

    def get_api_action_path(self, entity_name, action_name):
        return os.path.join(self.backend_dir, f"Api/{entity_name}/{action_name}.php")

    def get_hook_path(self, entity_name, hook_name):
        return os.path.join(self.backend_dir, f"Hooks/{entity_name}/{hook_name}.php")

    def get_backend_mass_action_path(self, entity_name, mass_action_name):
        return os.path.join(self.backend_dir, f"MassAction/{entity_name}/{mass_action_name}.php")

    def get_controller_path(self, controller_name):
        return os.path.join(self.backend_dir, f"Controllers/{controller_name}.php")

    def get_entity_path(self, entity_name):
        return os.path.join(self.backend_dir, f"Entities/{entity_name}.php")

    def get_entity_defs_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/entityDefs/{entity_name}.json")

    def get_scopes_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/scopes/{entity_name}.json")

    def get_record_defs_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/recordDefs/{entity_name}.json")

    def get_client_defs_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/clientDefs/{entity_name}.json")

    def get_i18n_path(self, entity_name=None, language_code=None):
        if language_code is None:
            return os.path.join(self.resources_dir, "i18n")
        return os.path.join(self.resources_dir, f"i18n/{language_code}/{entity_name}.json")

    def get_item_path(self, item_type, item_name):
        return os.path.join(self.backend_dir, f"{item_type}/{item_name}.php")
