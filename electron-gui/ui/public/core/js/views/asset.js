var APP = APP || {};

APP.AssetView = Backbone.View.extend({
    template: _.template($('#asset-view-tpl').html()),

    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
        var assetTabHeadView = new APP.AssetTabHeadView({ el: '#TabHead', model: this.model });
        assetTabHeadView.render();

        this.$el.append(this.template(this.model.toJSON()));

        // render portfolio charts
        var chartdata = this.model.get('priceclose').map(function (d) {
            return d;
        });;

        var ticker = this.model.get('ticker');
        // clear chart area
        var chartid = ticker + '-tsChart';

        // draw chart
        var ts = APP.timeseries('#' + chartid, chartdata, { width: 1250, height: 500, margin: {} });
        ts.draw();

        return this;
    }
    
});

