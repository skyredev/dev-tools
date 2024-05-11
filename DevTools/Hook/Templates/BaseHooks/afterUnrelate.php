<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder};

use Espo\Core\Hook\Hook\AfterUnrelate;
use Espo\ORM\EntityManager;
use Espo\ORM\Entity;
use Espo\Core\Utils\Log;
use Espo\ORM\Repository\Option\UnrelateOptions;

class {HookNamePlaceholder} implements afterUnrelate
{
    const DEBUG_PREFIX = '[{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder}\{HookNamePlaceholder}]';

    public function __construct(
        private Log $log
    ) {}

    private function debug($message, array $context = []): void
    {
        $this->log->debug(self::DEBUG_PREFIX . ' ' . $message, $context);
    }

    public function afterUnrelate (Entity $entity, string $relationName, Entity $relatedEntity, UnrelateOptions $options): void
    {
        // Your code here
    }
}
