import json

from DevTools.Base.BaseCommand import BaseCommand
from DevTools.Entity.Fields.BaseField import BaseField
from DevTools.Entity.Fields.TextField import TextField
from DevTools.Entity.Fields.VarcharField import VarcharField


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

    def createNewEntityBase(self):

        fieldName = VarcharField("name")
        fieldName.set_value('required', 'true')
        fieldName.set_value('pattern', '$noBadCharacters')

        fieldDescription = TextField("description")

        return json.dumps({
            "fields": {
                fieldName.name: fieldName.data,
                fieldDescription.name: fieldDescription.data
            }
        }, indent=4)