from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Json_Array(Base):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "jsonArray"
        }

    availableOptions = {

    }
