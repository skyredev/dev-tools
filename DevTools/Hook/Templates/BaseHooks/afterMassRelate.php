<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder};

use Espo\Core\Hook\Hook\AfterMassRelate;
use Espo\ORM\EntityManager;
use Espo\ORM\Entity;
use Espo\Core\Utils\Log;
use Espo\ORM\Repository\Option\SaveOptions;
use Espo\ORM\Repository\Option\MassRelateOptions;
use Espo\ORM\Query\Select;

class {HookNamePlaceholder} implements afterMassRelate
{
    const DEBUG_PREFIX = '[{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder}\{HookNamePlaceholder}]';

    public function __construct(
        private Log $log
    ) {}

    private function debug($message, array $context = []): void
    {
        $this->log->debug(self::DEBUG_PREFIX . ' ' . $message, $context);
    }

    public function afterMassRelate (Entity $entity, string $relationName, Select $query, array $columnData, MassRelateOptions $options): void
    {
        // Your code here
    }
}
