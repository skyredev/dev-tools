from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Duration(Base):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "duration"
        }

    availableOptions = {
        "default": ValidationOptions.Integer,
        "options": ValidationOptions.ArrayInt

    }
