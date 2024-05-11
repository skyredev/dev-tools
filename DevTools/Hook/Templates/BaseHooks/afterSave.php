<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder};

use Espo\Core\Hook\Hook\AfterSave;
use Espo\ORM\EntityManager;
use Espo\ORM\Entity;
use Espo\Core\Utils\Log;
use Espo\ORM\Repository\Option\SaveOptions;

class {HookNamePlaceholder} implements afterSave
{
    const DEBUG_PREFIX = '[{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder}\{HookNamePlaceholder}]';

    public function __construct(
        private Log $log
    ) {}

    private function debug($message, array $context = []): void
    {
        $this->log->debug(self::DEBUG_PREFIX . ' ' . $message, $context);
    }

    public function afterSave (Entity $entity, SaveOptions $options): void
    {
        // Your code here
    }
}
