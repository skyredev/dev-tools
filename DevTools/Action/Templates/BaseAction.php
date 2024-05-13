<?php
namespace Espo\Modules\{ModuleNamePlaceholder}\Api\{EntityNamePlaceholder};

use Espo\Core\Api\Action;
use Espo\Core\Api\Request;
use Espo\Core\Api\Response;
use Espo\Core\Api\ResponseComposer;

class {ActionNamePlaceholder} implements Action
{
    public function __construct() {}

    public function process(Request $request): Response
    {
        $data = $request->getRouteParam('text');
        $data = $request->getParsedBody();

        return ResponseComposer::json($data);
    }
}
