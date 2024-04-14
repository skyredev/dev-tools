<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder};

use Espo\Core\Hook\Hook\AfterRelate;
use Espo\ORM\EntityManager;
use Espo\ORM\Entity;
use Espo\ORM\Repository\Option\RelateOptions;

class {HookNamePlaceHolder} implements afterRelate
{
    const DEBUG_PREFIX = '[{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder}\{HookNamePlaceHolder}]';

    public function __construct(
        private Log $log
    ) {}

    private function debug($message, array $context = []): void
    {
        $this->log->debug(self::DEBUG_PREFIX . ' ' . $message, $context);
    }

    public function afterRelate (Entity $entity, string $relationName, Entity $relatedEntity, array $columnData, RelateOptions $options): void
    {

    }
}
