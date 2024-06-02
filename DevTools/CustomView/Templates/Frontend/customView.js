define('{ModuleNamePlaceholder}:views/{EntityNamePlaceholder}/{ViewPathPlaceholder}', ['views/{ViewPathPlaceholder}'], function (Dep) {

    return Dep.extend({

        {TemplatePlaceholder}
        {MiddleViewPlaceholder}
        {SideViewPlaceholder}
        {BottomViewPlaceholder}

        setup: function() {
            Dep.prototype.setup.call(this);

        },

        afterRender: function() {
            Dep.prototype.afterRender.call(this);

        },
    });
});
