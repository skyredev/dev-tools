<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder};

use Espo\Core\Hook\Hook\BeforeSave;
use Espo\ORM\EntityManager;
use Espo\ORM\Entity;
use Espo\ORM\Repository\Option\SaveOptions;

class {HookNamePlaceHolder} implements beforeSave
{
    const DEBUG_PREFIX = '[{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder}\{HookNamePlaceHolder}]';

    public function __construct(
        private Log $log
    ) {}

    private function debug($message, array $context = []): void
    {
        $this->log->debug(self::DEBUG_PREFIX . ' ' . $message, $context);
    }

    public function beforeSave (Entity $entity, SaveOptions $options): void
    {

    }
}
