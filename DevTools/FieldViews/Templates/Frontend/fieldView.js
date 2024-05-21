define('{ModuleNamePlaceholder}:views/fields/{EntityNamePlaceholder}/{FieldTypePlaceholder}', ['views/fields/{FieldTypePlaceholder}'], function (Dep) {

   return Dep.extend({

        setup: function () {
            Dep.prototype.setup.call(this);
            // some initialization
        },

        afterRender: function () {
            Dep.prototype.afterRender.call(this);
            // your customizations executed after the field is rendered
        },
    });
});