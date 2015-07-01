var APP = APP || {};

APP.ConstraintView = Backbone.View.extend({

    tagName: 'tr',

    template: _.template($('#constraintsdata-tpl').html()),

    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});