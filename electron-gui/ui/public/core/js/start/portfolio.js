var APP = APP || {};

APP.app = null;
APP.PortfolioList = {};

APP.bootstrap = function () {
    APP.app = new APP.Router();
    Backbone.history.start({ pushState: true });
};

$(function () {
    
    APP.Socket = io.connect('localhost', {
        port: 4000,
        transports: ['websocket']
    });

    APP.Socket.on('connect', function () {
        console.log('Client has connected to the server!');
        APP.bootstrap();
    });

});

