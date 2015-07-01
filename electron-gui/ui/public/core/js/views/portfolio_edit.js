var APP = APP || {};

APP.PortfolioEditTabHeadView = Backbone.View.extend({
    template: _.template($('#portfolioEdit-tabHead-tpl').html()),

    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
        this.$el.append(this.template(this.model.toJSON()))
        return this;
    }

});

APP.PortfolioEditView = Backbone.View.extend({

    template: _.template($('#portfolioEdit-tpl').html()),

    events: {
        'click #savePortfolioEdit-btn': 'savePortfolio'
    },

    initialize: function () {
        
        _.bindAll(this, 'render', 'handleFileSelect', 'parseCsvHtml', 'parseCols', 'handleRadiobtn');

        // Get assets
        var asset_collection = new APP.AssetCollection([], {
            url: '/api/asset/collection/indices'
        });

        asset_collection.fetch({
            headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') },
            error: this.onError
        });

        this.universe = asset_collection;

    },
    render: function () {
        var peditTabHeadView = new APP.PortfolioEditTabHeadView({ el: '#TabHead', model: this.model });
        peditTabHeadView.render();

        this.$el.append(this.template(this.model.toJSON()));
        this.dropzone();

        this.$searchinp = this.$('#benchmark');

        // register autocomplete functionality
        this.searchAutoComplete(this.universe);

        return this;
    },

    savePortfolio: function(){
        var name = this.$('#portfolio-name').val();
        this.model.set('name', name);

        var nav = this.$('#portfolio-nav').val();
        this.model.set('NAV', nav);

        // remove tab and stuff
        $('#tab-edit-head').remove();
        $('#tab-edit-body').remove();

        $('#portfolio-tab-head').click();

        this.model.save({}, {
            success: this.onSuccess,
            error: this.onError,
            headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') }
        });
    },

    searchAutoComplete: function (model) {

        var options = {
            source: function (query, process) {
                var assets = model.map(function (a) { return a.get('ticker') + ' - ' + a.get('name'); });
                process(assets);
            },
            updater: function (item) {
                return item;
            }
        };

        // register event for all items with 
        this.$searchinp.typeahead(options);
    },

    dropzone: function() {
        // Setup the dnd listeners.

        $('#file_dropzone').on('dragover', this.handleDragOver);
        $('#file_dropzone').on('drop', this.handleFileSelect);
    },
        
    handleFileSelect: function (e) {
        
        e.stopPropagation();
        e.preventDefault();

        var files = e.originalEvent.dataTransfer.files; // FileList object.
        var output = [];

        if (files.length > 1)
            APP.notify({ message: 'Too many files - please only upload one file - the first one will be selected automatically...', type: 'error' });

        var f = files[0];
        if (f.size > 10000)
            APP.notify({ message: 'File too large!', type: 'error' });

        else {
            output.push('<i class="icon-file"></i><strong> ', escape(f.name), '</strong>');

            $('#file_dropzone').html(output.join(''));
            var reader = new FileReader();

            reader.onprogress = function (e) {
                $('#readprogress').prop('hidden', false);
                var pct = Math.round((e.loaded / e.total) * 100);

                $('#readprogress .bar').css('width', pct + '%');
            },

            reader.onload = function (e) {
                $('#readprogress .bar').css('width', '100%');
            };

            var parseCsv = this.parseCsvHtml;
            var handleRadiobtn = this.handleRadiobtn;

            reader.onloadend = function (e) {
                var data = e.target.result;
                
                $('#filehead').html('');
                $('#filedata').html('');

                var file = parseCsv(data);

                $('#filehead').append(file.html.header);
                $('#filedata').append(file.html.body);

                var datacol = 0, datecol = 0;
                handleRadiobtn(data, datecol, datacol);

                $('.checkbox').change(function (e) {
                    if (this.checked) {
                        handleRadiobtn(data, datecol, datacol);
                    }
                });
            };

            reader.readAsText(f);
        }
    },

    parseCols: function (cols) {
        var datacol, datecol;

        cols.forEach(function (c) {
            var ids = c.split('-');

            if (ids[0] === 'datacol')
                datacol = ids[1];
            else if (ids[0] === 'datecol')
                datecol = ids[1];
        });

        return { data: datacol, date: datecol };
    },

    handleRadiobtn: function(data, datecol, datacol) {
        var cols = [$('.checkbox:checked')[0].id, $('.checkbox:checked')[1].id];
        var parsedCols = this.parseCols(cols);
        datacol = parsedCols.data;
        datecol = parsedCols.date;

        if (datacol === datecol)
            APP.notify({ message: 'Something fishy in selection...', type: 'error' });

        var ts = this.getTimeSeries(data, datecol, datacol);

        this.model.set('timeseries', ts);
    },

    handleDragOver: function (e) {
        $('#readprogress .bar').css('width', '0%');
        e.stopPropagation();
        e.preventDefault();
        e.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
    },

    onError: function (model, response) {
        //var error = $.parseJSON(response.responseText);
    },

    onSuccess: function (model, response) {
        console.log('Successfully updated portfolio...');
    },

    getTimeSeries: function(data, datecol, datacol) {
        var rows = data.split('\n');
        var ts = [];
        var header, data;
        rows.forEach(function (r, i) {
            var line = r.split(',');
            if (i === 0) {
                header = { date: line[datecol], value: line[datacol] };
            }
            else {
                if (line[datecol] && line[datacol]) {
                    data = { date: line[datecol], value: line[datacol] };
                    ts.push(data);
                }
            }
        });

        return { name: header.value, data: ts };
    },

    parseCsvHtml: function (data) {
        var lines = data.split('\n');

        var header = [];
        var body = [];
        
        var line1 = [];
        var line2 = [];
        var head = [];

        lines.forEach(function (r, i) {
            // forEach line
            var d = r.split(',');
            if (i === 0) {
                // the first line of the csv file contains the header info
                line1.push('<tr><th>Date/Time Column</th>');
                line2.push('<tr><th>Data Column</th>');
                head.push('<th></th>');
                d.forEach(function (td, i) {
                    if (i === 0) {
                        line1.push('<th><input class="checkbox" id="datecol-' + i + '" name="datecol" type="radio" checked/></th>');
                        line2.push('<th><input class="checkbox" id="datacol-' + i + '" name="datacol" type="radio"/></th>');
                        head.push('<th>' + td + '</th>')
                    }
                    else {
                        line1.push('<th><input class="checkbox" id="datecol-' + i + '" name="datecol" type="radio"/></th>');
                        line2.push('<th><input class="checkbox" id="datacol-' + i + '" name="datacol" type="radio" checked/></th>');
                        head.push('<th>' + td + '</th>')
                    }
                });
                line1.push('</tr>');
                line2.push('</tr>');
                head.push('</tr>');

                header.push(line1.join(''));
                header.push(line2.join(''));
                header.push(head.join(''));
            }
            else {
                body.push('<tr><td></td>');
                d.forEach(function (td, i) {
                    if (td)
                        body.push('<td>' + td + '</td>')
                });
                body.push('<tr>');
            }
        });

        return {
            html: {
                header: header.join(''),
                body: body.join('')
            }
        };
    }
});