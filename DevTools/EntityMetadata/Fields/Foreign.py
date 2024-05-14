from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Foreign(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "readOnly": True,
            "type": "foreign"
        }

    availableOptions = {
        "link": ValidationOptions.String,
        "field": ValidationOptions.String,
        "view": ValidationOptions.String,

    }
