define('{ModuleNamePlaceholder}:handlers/{EntityNamePlaceholder}/{HandlerNamePlaceholder}-handler', [], () => {

    class Handler {

        /**
         * @param {import('view').default} view
         */
        constructor(view) {
            this.view = view;
        }

        process() {
            this.listenTo(this.view, 'after:render', () => {
                // Do something with view after render.
            });
        }
    }

    // Establish event support.
    Object.assign(Handler.prototype, Backbone.Events);

    return Handler;
});
