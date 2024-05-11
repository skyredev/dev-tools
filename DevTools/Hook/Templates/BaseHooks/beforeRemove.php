<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder};

use Espo\Core\Hook\Hook\BeforeRemove;
use Espo\ORM\EntityManager;
use Espo\ORM\Entity;
use Espo\Core\Utils\Log;
use Espo\ORM\Repository\Option\RemoveOptions;

class {HookNamePlaceholder} implements beforeRemove
{
    const DEBUG_PREFIX = '[{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder}\{HookNamePlaceholder}]';

    public function __construct(
        private Log $log
    ) {}

    private function debug($message, array $context = []): void
    {
        $this->log->debug(self::DEBUG_PREFIX . ' ' . $message, $context);
    }

    public function beforeRemove (Entity $entity, RemoveOptions $options): void
    {
        // Your code here
    }
}
