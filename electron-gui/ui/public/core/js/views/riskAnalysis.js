var APP = APP || {};

APP.RiskTabHeadView = Backbone.View.extend({
    template: _.template($('#risk-tabHead-tpl').html()),

    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
        this.$el.append(this.template(this.model.toJSON()))
        return this;
    }

});

APP.RiskAnalysisView = Backbone.View.extend({
    template: _.template($('#riskanalysis-view-tpl').html()),

    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
        var riskTabHeadView = new APP.RiskTabHeadView({ el: '#TabHead', model: this.model });
        riskTabHeadView.render();

        this.$el.append(this.template(this.model.toJSON()));

        // render portfolio charts
        var chartdata = this.model.get('timeseries').data.map(function (d) {
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
