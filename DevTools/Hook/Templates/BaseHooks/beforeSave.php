<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder};

use Espo\Core\Hook\Hook\BeforeSave;
use Espo\ORM\EntityManager;
use Espo\ORM\Entity;
use Espo\ORM\Repository\Option\SaveOptions;

use Espo\Modules\CustomAccounting\Tools\Vies;

class {HookNamePlaceHolder} implements {HookTypePlaceHolder}
{
    const DEBUG_PREFIX = '[{ModuleNamePlaceholder}\Hooks\{EntityNamePlaceholder}\{HookNamePlaceHolder}]';

    public function __construct(
    ) {}

    private function debug($message, array $context = []): void
    {
        $this->log->debug(self::DEBUG_PREFIX . ' ' . $message, $context);
    }

    public function {FunctionNamePlaceHolder} (Entity $entity, SaveOptions $options): void
    {

    }
}
