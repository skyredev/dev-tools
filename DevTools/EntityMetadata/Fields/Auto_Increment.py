from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Auto_Increment(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "autoincrement",
            "autoincrement": True,
            "unique": True
        }

    availableOptions = {

    }
