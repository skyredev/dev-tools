from DevTools.EntityMetadata.Links.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class HasChildren(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "hasChildren"
        }

    availableOptions = {
        "foreign": ValidationOptions.String,
        "entity": ValidationOptions.String,
        "audited": ValidationOptions.TrueFalse,
        "relationName": ValidationOptions.String,
        "layoutRelationshipsDisabled": ValidationOptions.TrueFalse,
    }
