define('{ModuleNamePlaceholder}:handlers/{EntityNamePlaceholder}/{ButtonNamePlaceholder}-handler', [], function () {

  var {FunctionNamePlaceholder}Handler = function (view) {
    this.view = view;
  };

  _.extend({FunctionNamePlaceholder}Handler.prototype, {

    init{FunctionNamePlaceholder} () {
      // called when the list view is loaded
    },

    action{FunctionNamePlaceholder} (data) {
      console.log(data); // data to be sent to the back-end
    }

  });

  return {FunctionNamePlaceholder}Handler;
});