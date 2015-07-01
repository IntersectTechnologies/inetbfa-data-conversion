var APP = APP || {};

APP.AppView = Backbone.View.extend({

    events: {
       
    },

    initialize: function () {
        _.bindAll(this, 'render');
        APP.OpenTabs = [];
        this.addContextMenu();
    },

    render: function () {
        return this;
    },

    addContextMenu: function () {
        context.init({
            fadeSpeed: 100,
            filter: function ($obj) { },
            above: 'auto',
            preventDoubleContext: true,
            compress: true
        });

        var header = { header: "Header" };
        var divider = { divider: true };
        var del = { text: "Delete" };
        var ed = { text: 'Edit' };

        var menuObjects = [del];

        context.attach('.nav-tabs li', menuObjects);
    },
});