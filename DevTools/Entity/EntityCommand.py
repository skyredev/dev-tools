from DevTools.Base.BaseCommand import BaseCommand


class EntityCommand(BaseCommand):
    ENTITY_TYPES = {
        "1": "Base",
        "2": "BasePlus",
        "3": "Event",
        "4": "Person",
        "5": "Company"
    }

    def run(self):
        module = self.get_module()
        entity_type = self.TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the Entity type:", self.ENTITY_TYPES),
            self.ENTITY_TYPES)
        entity_name = self.get_entity_name()

        self.FileManager.create_entity_files(module, entity_name, entity_type)
