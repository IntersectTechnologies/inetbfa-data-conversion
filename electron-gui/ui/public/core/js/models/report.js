var APP = APP || {};

APP.Report = Backbone.Model.extend({
    urlRoot: 'api/report',
    idAttribute: '_id',

    initialize: function () {
        for (var key in this.get('_attachments')) {
            var fn = key;
            console.log(key);
            this.set('filename', fn);
        }
    }
});

APP.ReportCollection = Backbone.Collection.extend({
    url: '/api/report',
    model: APP.Report,
});
