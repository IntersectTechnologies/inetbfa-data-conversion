var APP = APP || {};

APP.InvestmentView = Backbone.View.extend({

    tagName: 'tr',

    template: _.template($('#investmentdata-template').html()),

    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.attr('id', this.model.get('asset').ticker);
        return this;
    }
});
