from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Attachment_Multiple(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "attachmentMultiple",
            "previewSize": "medium",
            "sourceList": [],
            "accept": []
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "sourceList": ValidationOptions.Array,
        "maxFileSize": ValidationOptions.Float,
        "previewSize": ValidationOptions.Array,
        "accept": ValidationOptions.Array,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "optionsPath": ValidationOptions.String

    }

    linkDefs = {
        "type": "hasChildren",
        "entity": "Attachment",
        "foreign": "parent",
        "layoutRelationshipsDisabled": True,
        "relationName": "attachments",
        "utility": True
    }
