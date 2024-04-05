def get_php_template(module, hook_type, name, entity):
    save_options = ""
    method_signature = ""

    if hook_type == "beforeSave" or hook_type == "afterSave":
        save_options = "use Espo\\ORM\\Repository\\Option\\SaveOptions;"
        method_signature = "(Entity $entity, SaveOptions $options): void"
    elif hook_type == "beforeRemove" or hook_type == "afterRemove":
        save_options = "use Espo\\ORM\\Repository\\Option\\RemoveOptions;"
        method_signature = "(Entity $entity, RemoveOptions $options): void"
    elif hook_type == "afterRelate":
        save_options = "use Espo\\ORM\\Repository\\Option\\RelateOptions;"
        method_signature = "(Entity $entity, string $relationName, Entity $relatedEntity, array $columnData, RelateOptions $options): void"
    elif hook_type == "afterUnrelate":
        save_options = "use Espo\\ORM\\Repository\\Option\\UnrelateOptions;"
        method_signature = "(Entity $entity, string $relationName, Entity $relatedEntity, UnrelateOptions $options): void"
    elif hook_type == "afterMassRelate":
        save_options = "use Espo\\ORM\\Repository\\Option\\MassRelateOptions;\nuse Espo\\ORM\\Query\\Select;"
        method_signature = "(Entity $entity, string $relationName, Select $query, array $columnData, MassRelateOptions $options): void"

    return f"""<?php
namespace Espo\\Modules\\{module}\\Hooks\\{entity};

use Espo\\ORM\\Entity;
use Espo\\Core\\Hook\\Hook\\{hook_type[0].upper() + hook_type[1:]};
{save_options}

class {name} implements {hook_type}
{{
    public function __construct(
        // Define needed dependencies.
    ) {{}}

    public function {hook_type}{method_signature}
    {{

    }}
}}
"""