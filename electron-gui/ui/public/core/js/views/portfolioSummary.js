var APP = APP || {};

APP.PortfolioSummaryView = Backbone.View.extend({

    tagName: 'li',
    className: 'portfolio',

    template: _.template( $('#item-template').html()),

    initialize: function () {
        _.bindAll(this, 'render', 'onClick');
        this.model.bind('change', this.render);
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    events: {
        'click': 'onClick',
    },

    onClick: function (e) {
        APP.app.navigate('portfolio/' + this.model.get('_id') + '/', { trigger: true });
    }
});