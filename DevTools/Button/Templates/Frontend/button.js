define('{ModuleNamePlaceholder}:handlers/{EntityNamePlaceholder}/{ButtonNamePlaceholder}-handler', ['action-handler'], function (Dep) {

  return class extends Dep {

    action{FunctionNamePlaceholder} (data, e) {
      Espo.Ajax
        .getRequest('{EntityNameUpperPlaceholder}/' + this.view.model.id)
        .then(response => {
          console.log(response);
        });
    }

    init{FunctionNamePlaceholder} () {
      // called when the list view is loaded
    }
  }
});