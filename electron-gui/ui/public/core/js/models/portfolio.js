var APP = APP || {};

APP.Portfolio = Backbone.RelationalModel.extend({
    urlRoot: '/api/portfolio',
    idAttribute: '_id',
    relations: [
        {
            type: Backbone.HasMany,
            key: 'investments',
            relatedModel: 'APP.Investment',
            collectionType: 'APP.InvestmentCollection',
            reverseRelation: {
                key: 'isIn',
                includeInJSON: 'id',
            },
        },
        {
            type: Backbone.HasMany,
            key: 'constraints',
            relatedModel: 'APP.Constraint',
            collectionType: 'APP.ConstraintCollection',
            reverseRelation: {
                key: 'isIn',
                includeInJSON: 'id',
            },
        }
    ],
    defaults: {
        doctype: 'portfolio',
        user_id: '',
        name: 'myportfolio',
        NAV: 1000000,
        exposure: 1000000,
        universe: { name: 'JSE Equities', url: '/api/asset/collection/jse_equities'},
        benchmark: { ticker: 'J203', exchange: 'JSE', _id: null },

        constraints: [],
        returnModel: { name: '', _id: ''},
        riskModel: { name: '', _id: ''},

        timeseries: [],
        metrics: []

    },
    update: function () {
        var total = this.get('exposure');

        this.get('investments').forEach(function (i) {
            if (total) {
                var weight = i.get('exposure') / total;
                i.set('weight', weight);
            }
            else {
                i.set('weight', 0);
            }
        });

    }
});

APP.PortfolioCollection = Backbone.Collection.extend({
    url: '/api/portfolio',
    model: APP.Portfolio,
});