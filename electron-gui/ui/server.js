// Module dependencies.

var express = require('express')
  , app = express()
  , routes = require('./routes')
  , user = require('./auth/user')
  , server = require('http').createServer(app)
  , path = require('path')
  , util = require('util')
  , ejs = require('ejs');

ejs.open = '{{';
ejs.close = '}}';


// all environments
app.configure(function () {
    app.set('port', process.env.PORT || 80);
    app.set('views', __dirname + '/views');
    app.set('view engine', 'ejs');

    app.use(express.favicon());
    //app.use(express.logger());
    app.use(express.cookieParser());
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(express.session({ secret: 'cat' }));
    app.use(app.router);
    app.use(express.static(path.join(__dirname, 'public')));
});

//// development only
//if ('development' == app.get('env')) {
//    app.use(express.errorHandler());
//};

// BASIC ROUTES:
//
// 1. / - home page and login page
// 2. /portfolio - application page
// 3. /help - help documentation
//
// Redirection rules
// If active session automatically redirect to /portfolio
// If active session and /help is requested direct to /help
// If active session and /logout is requested --> /
// If session inactive and /portfolio is requested --> /login

// Get home page - 
app.get('/', routes.dashboard);
app.get('/trade', routes.trade);
app.get('/simulate', routes.simulate);
app.get('/help', routes.help);

// create proxy that listens for all requests

server.listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
