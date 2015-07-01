var APP = APP || {};

APP.MVOTabHeadView = Backbone.View.extend({
    template: _.template($('#mvo-tabHead-tpl').html()),

    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
        this.$el.append(this.template(this.model.toJSON()))
        return this;
    }

});

APP.MVOView = Backbone.View.extend({
    template: _.template($('#mvo-view-tpl').html()),

    initialize: function () {
        _.bindAll(this, 'render');

        Backbone.sync('create', this.model, {
            url: '/api/mvofrontier'
        });
        
        //this.listenTo(this.model, 'change', this.render);
    },

    render: function (data) {
        var mvoTabHeadView = new APP.MVOTabHeadView({ el: '#TabHead', model: this.model });
        mvoTabHeadView.render();

        this.$el.append(this.template(this.model.toJSON()));

        return this;
    }

});
