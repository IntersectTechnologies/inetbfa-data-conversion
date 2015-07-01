var APP = APP || {};

APP.PortfolioListView = Backbone.View.extend({

    events: {
        'click #saveportfolio': 'onSaveNewPortfolio',
        'click #del-portf-btn': 'onDeletePortfolio'
    },

    initialize: function () {

        this.$input = this.$('#newportfolioname');

        _.bindAll(this, 'render', 'renderPortfolioSummary', 'onPortfolioSaved', 'onSaveNewPortfolio', 'onError',
            'newPortfolio', 'editPortfolio', 'addContextMenu', 'onDeletePortfolio');

        this.model.bind('sync', this.render);
        this.model.bind('change', this.render);
        this.model.bind('remove', this.render);

        this.addContextMenu();
    },

    render: function () {
        this.$('#portfoliolist .portfolio').remove();
        this.model.each(this.renderPortfolioSummary);

        return this;
    },

    renderPortfolioSummary: function (portfolio) {
        var summaryView = new APP.PortfolioSummaryView({ model: portfolio });
        $('#portfoliolist').append(summaryView.render().el);
    },

    navigateApp: function (portfolio) {
        var pid = portfolio.get('_id');
        APP.app.navigate('portfolio/' + pid + '/', { trigger: true });
    },

    newPortfolio: function() {
        return {
            name: this.$input.val().trim()==='' ? 'myportfolio' : this.$input.val().trim()
        }
    },

    addContextMenu: function () {
        context.init({
            fadeSpeed: 100,
            filter: function ($obj) { },
            above: 'auto',
            preventDoubleContext: true,
            compress: true
        });

        var header = { header: "Header" };
        var divider = { divider: true };
        var del = {
            text: 'Delete',
            action: this.deletePortfolio
        };
        var ed = { 
            text: 'Edit', 
            action: this.editPortfolio
        };

        var menuObjects = [del, ed];

        context.attach('li.active .portfolio-item', menuObjects);
    },

    onSaveNewPortfolio: function (e) {
        var portfolio = new APP.Portfolio(this.newPortfolio());

        portfolio.save({}, {
            success: this.onPortfolioSaved,
            error: this.onError,
            headers: { 'Authorization': 'Basic ' + btoa($('#username').text().trim() + ':PASSWORD') }
        });
    },

    editPortfolio: function (e) {
        this.removeEditTab();

        if ($('li.active .portfolio-item').length > 0) {
            this.addEditTab();
            // select portfolio edit tab
            $('#tab-edit-head').click();

            var id = ($('li.active .portfolio-item').attr('id'));
            var portf = this.model.get(id);

            var portf_editView = new APP.PortfolioEditView({ el: '#tab-edit-body', model: portf });
            portf_editView.render();
        }
    },

    removeEditTab: function() {
        $('#tab-edit-head').remove();
        $('#tab-edit-body').remove();
    },

    addEditTab: function() {
        $('#TabHead').append('<li><a href="#tab-edit-body" data-toggle="tab" id="tab-edit-head">Portfolio Edit</a></li>');
        $('#TabBody').append('<div class="tab-pane" id="tab-edit-body"> </div>');
    },

    updatePortfolio: function (e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if (code == 13) { //Enter keycode
            var id = e.currentTarget.parentElement.parentElement.id;
            var name = this.$('.item-edit input').val();
            this.model.get(id).set('name', name);
            this.$('.item-edit').prop('hidden', true);
            this.$('#' + id + ' .item-view').prop('hidden', false);

            // now update portfolio on server also
        }
    },

    deletePortfolio: function (e) {
        var id = ($('li.active .portfolio-item').attr('id'));

        $('#delportfolio').modal('show');
        $('#delportfolio').data('id', id);
    },

    onDeletePortfolio: function(e) {
        var id = $('#delportfolio').data('id');
        var portf = this.model.get(id);
        portf.destroy();
    },

    onPortfolioSaved: function (portfolio, response) {
        this.model.add(portfolio, { silent: true });
        this.$input.val('');
    },

    onError: function (model, response) {
        var error = $.parseJSON(response.responseText);
    }
});