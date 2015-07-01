var APP = APP || {};

// Asset model
APP.Asset = Backbone.Model.extend({
    urlRoot: '/api/asset',
    idAttribute: '_id',

    defaults: {
        _id: '',
        doctype: 'asset',
        ticker: 'QQQ',
        name: 'QQQ',
        ISIN: '',
        sector: '',
        assetclass: 'equity',
        instrument: 'stock',
        exchange: 'JSE',
        industry: '',
        sector: '',
        metrics: [],
        currency: 'ZAR',
        proxy: { 
            _id: '',
            ticker: '',
            exchange: ''
        },

        priceclose: []
    },
    initialize: function () {
        
    }
});

APP.AssetCollection = Backbone.Collection.extend({
    url: '/api/asset',
    model: APP.Asset
});
