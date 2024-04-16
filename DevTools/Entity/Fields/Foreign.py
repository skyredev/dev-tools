from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Foreign(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "foreign"
        }

    availableOptions = {
        "link": ValidationOptions.String,
        "field": ValidationOptions.String,
        "view": ValidationOptions.String,

    }
