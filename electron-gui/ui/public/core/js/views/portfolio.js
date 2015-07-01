var APP = APP || {};

APP.PortfolioView = Backbone.View.extend({

    template: _.template($('#portfolio-tpl').html()),

    events: {
        'click td a.asset': 'viewAsset'
    },

    addEvents: function () {
        $('a.edit-btn').click(this.onEditInvestment);
        $('a.delete-btn').click(this.onDeleteInvestment);

        $('#riskanalysis-btn').click(this.viewRiskAnalysis);
        $('#mvo-btn').click(this.viewMVO);
        $('#portfolio-settings-btn').click(this.editPortfolio);
    },

    initialize: function () {
        this.$data = this.$('#tabledata');
        this.$foot = this.$('#tablefoot');
        this.$constraintdata = this.$('#constraintdata');
        this.$addbtn = this.$('#add-asset');
        this.$delinv_confirmbtn = $('#del-inv-btn');
        this.$updinv_confirmbtn = $('#upd-inv-btn');
        this.$searchinp = this.$('#search-input');

        _.bindAll(this, 'render', 'render_investment', 'render_constraint', 'searchAutoComplete', 'addAsset', 'onAssetAdded', 'onError', 'onSuccess',
            'updateInvestment', 'deleteInvestment', 'onEditInvestment', 'onDeleteInvestment', 'addEvents', 'viewRiskAnalysis', 'viewMVO', 'editPortfolio');

        // add click event handler - NOTE: done manully without using backbone events in order to fix problem with multiple event handlers registered to same event which cannot be deregistered afik
        this.$addbtn.click(this.addAsset);
        this.$delinv_confirmbtn.click(this.deleteInvestment);
        this.$updinv_confirmbtn.click(this.updateInvestment);
        
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'sync', this.render);
        this.listenTo(this.model, 'add:investments', this.render);

        // Get assets
        var asset_collection = new APP.AssetCollection([], {
            url: this.model.get('universe').url
        });

        asset_collection.fetch({
            headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') },
            error: this.onError
        });

        this.universe = asset_collection;
        
    },

    render: function () {

        var holdings = 0;
        this.model.get('investments').each(function (p) {
            holdings += parseFloat(p.get('exposure'));
        });

        this.model.set('exposure', holdings);

        // activate selected item in UI
        $('#portfoliolist li').removeClass('active');
        $('#' + this.model.get('_id')).parent('li').addClass('active');

        // register autocomplete functionality
        this.searchAutoComplete(this.universe);

        // enable autocomplete search
        this.$searchinp.prop('disabled', false);
        // enable add-asset button
        this.$addbtn.prop('disabled', false);

        // render portfolio data in table
        this.$data.html('');
        this.model.update();
        this.model.get('investments').forEach(this.render_investment);

        this.model.get('constraints').forEach(this.render_constraint);

        this.$foot.html(this.template(this.model.toJSON()));

        // render portfolio charts
        var chartdata = this.model.get('investments').map(function (d) {
            return { weight: d.get('weight'), ticker: d.get('asset').ticker }
        });;

        // clear chart area
        $('#pie-chart').html('');

        // draw chart
        var pie = APP.pie('#pie-chart', chartdata, { width: 500, height: 500, margin: {}});
        pie.draw();

        this.addEvents();

        return this;
    },

    render_investment: function (investment) {
        var investment_view = new APP.InvestmentView({ model: investment });
        this.$data.append(investment_view.render().el);
    },

    render_constraint: function (constraint) {
        console.log('Rendering constraints...');
        var constraint_view = new APP.ConstraintView({ model: constraint });
        this.$constraintdata.append(constraint_view.render().el);
    },

    newInvestment: function (portfolio, asset) {
        return {
            isIn: portfolio,
            asset: {
                _id: asset.id,
                ticker: asset.get('ticker'),
                name: asset.get('name'),
                exchange: asset.get('exchange'),
                currency: asset.get('currency'),
                price: asset.get('price')
            }
        };
    },

    addAsset: function () {
        var selected = this.$searchinp.val();

        if (selected) {
            var asset = this.universe.find(function (a) {
                if (a.get('ticker') === selected.split(' - ')[0])
                    return a;
            });

            var f = this.model.get('investments').find(function (i) {
                // make matching criteria more specific - not only ticker
                return i.get('asset').ticker === asset.get('ticker');
            });

            // check if new asset already present in portfolio
            if (f) {
                // found

                // render message to user
            }
            else {
                // add to portfolio
                var newinv = this.newInvestment(this.model, asset);
                var inv = new APP.Investment(newinv);

                this.model.save({}, {
                    success: this.onAssetAdded,
                    error: this.onError,
                    headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') }
                });
            }
        }
        else
            this.onError();
    },

    onAssetAdded: function() {
        this.$searchinp.val('');
        //APP.app.navigate('/portfolio');
    },

    viewMVO: function () {
        var mod = this.model;

        var alreadyOpen = _.find(APP.OpenTabs, function (id) {
            if (id === mod.get('_id')+'-mvo')
                return true;
        });
        if (!alreadyOpen) {
           
            // api called on initialization
            var mvoView = new APP.MVOView({ el: '#TabBody', model: this.model });

            console.log('Waiting for job result...');

            // Create new tab
            APP.Socket.on('finjobs', function (data) {
                console.log('Received message via socket.io...');
                
                APP.OpenTabs.push(mod.get('_id') + '-mvo');
                mvoView.render(JSON.parse(data));
            });
        }
    },

    viewRiskAnalysis: function () {
        
        var mod = this.model;

        var alreadyOpen = _.find(APP.OpenTabs, function (id) {
            if (id === mod.get('_id') + '-risk')
                return true;
        });
        if (!alreadyOpen) {
            // Create new tab
            var riskView = new APP.RiskAnalysisView({ el: '#TabBody', model: this.model });
            APP.OpenTabs.push(this.model.get('_id')+'-risk');

            riskView.render();
        }
    },

    viewAsset: function (e) {
        var ticker = e.currentTarget.parentElement.parentElement.id;

        var asset = this.universe.find(function (a) {
            if (a.get('ticker') === ticker)
                return a;
        });
        
        var alreadyOpen = _.find(APP.OpenTabs, function (id) {
            if (id === asset.get('_id'))
                return true;
        });
        if (!alreadyOpen) {
            // Create new tab
            APP.OpenTabs.push(asset.get('_id'));
            var assetView = new APP.AssetView({ el: '#TabBody', model: asset });

            asset.fetch({
                headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') },
                error: this.onError
            });
        }
    },

    editPortfolio: function (e) {
        var portf = this.model;
        var alreadyOpen = _.find(APP.OpenTabs, function (id) {
            if (id === portf.get('_id') + '-edit')
                return true;
        });
        if (!alreadyOpen) {
            // Create new tab
            APP.OpenTabs.push(this.model.get('_id') + '-edit');
            var portfEditView = new APP.PortfolioEditView({ el: '#TabBody', model: this.model });

            portfEditView.render();
        }
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

    onEditInvestment: function (e) {
        var ticker = e.currentTarget.parentElement.parentElement.id;

        var inv = this.model.get('investments').find(function (i) { return i.get('asset').ticker === ticker; });
        $('#inv-name').data('id', ticker);
        $('#inv-name').text(inv.get('asset').name);

        $('#inv-exposure').val(inv.get('exposure'));
    },

    onDeleteInvestment: function (e) {
        var ticker = e.currentTarget.parentElement.parentElement.id;

        var inv = this.model.get('investments').find(function (i) { return i.get('asset').ticker === ticker; });
        $('#del-inv').data('id', ticker);
    },

    deleteInvestment: function (e) {
        var ticker = $('#del-inv').data('id');
        var inv = this.model.get('investments').find(function (i) { return i.get('asset').ticker === ticker; });

        inv.destroy();

        this.model.save({}, {
            success: this.onSuccess,
            error: this.onError,
            headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') }
        });
    },

    updateInvestment: function(e) {
        var newquant = $('#inv-exposure').val();
        var ticker = $('#inv-name').data('id');
        var inv = this.model.get('investments').find(function (i) { return i.get('asset').ticker === ticker; });
        inv.set('exposure', newquant);

        this.model.save({}, {
            success: this.onSuccess,
            error: this.onError,
            headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') }
        });
    },

    onError: function (model, response) {
        var error = $.parseJSON(response.responseText);
    },

    onSuccess: function(model, response) {
        APP.notify({ type: 'success', message: "Portfolio successfully updated" });
    }
});