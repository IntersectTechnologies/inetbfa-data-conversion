var http = require('http')
    , _ = require('underscore');

exports.dashboard = function (req, res) {
    res.render('dashboard', {
        title: 'Dashboard'
    });

};

exports.simulate = function (req, res) {
    res.render('help', {
        title: 'Help',
        username: req.user.id
    });

};

exports.trade = function (req, res) {
    res.render('help', {
        title: 'Help',
        username: req.user.id
    });
};

exports.help = function (req, res) {
    res.render('help', {
        title: 'Help',
        username: req.user.id
    });
};

