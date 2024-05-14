from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Link_Multiple(Base):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "linkMultiple"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "sortable": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "default": ValidationOptions.String,
        "createButton": ValidationOptions.TrueFalse,
        "autocompleteOnEmpty": ValidationOptions.TrueFalse

    }
