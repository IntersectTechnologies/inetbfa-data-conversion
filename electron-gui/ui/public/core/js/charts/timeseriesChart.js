// timeseries definition
/// pieChart definition
var APP = APP || {};

APP.timeseries = function (tag, data, options) {

    var containerElement = tag,
        w = options.width,
        h = options.height,
        data = data;

    var that = {};
    
    var draw = function () {
        var margin = { top: 20, right: 80, bottom: 30, left: 80 },
            width = w / 2 - margin.left - margin.right,
            height = h / 2 - margin.top - margin.bottom;

        var parseDate = d3.time.format("%Y-%m-%d").parse;

        var x = d3.time.scale()
            .range([0, width]);

        var y = d3.scale.linear()
            .range([height, 0]);

        var color = d3.scale.category10();

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom');

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient('left');

        var line = d3.svg.line()
            .interpolate('basis')
            .x(function (d) { return x(d.date); })
            .y(function (d) { return y(d.value); });

        var svg = d3.select(containerElement)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
        
        var render = function (data) {
            color.domain(d3.keys(data[0]).filter(function (key) { return key !== Date; }));

            data.forEach(function (d) {
                d.date = parseDate(d.date.substring(0, 10));
                d.value = +d.value;
            });

            x.domain(d3.extent(data, function (d) { return d.date; }));
            y.domain(d3.extent(data, function (d) { return d.value; }));

            svg.append('g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,' + height + ')')
                .call(xAxis);

            svg.append('g')
                .attr('class', 'y axis')
                .call(yAxis)
                .append('text')
                .attr('transform', 'translate('+margin.left+',0)')
                .attr('y', 6)
                .attr('dy', '.71em')
                .style('text-anchor', 'end')
                .text('Price (c)');

            svg.append('path')
                .datum(data)
                .attr('class', 'line')
                .attr('d', line);

        };

        render(data);
    };

    that.draw = draw;
    return that;
};