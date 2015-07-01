/// pieChart definition
var APP = APP || {};

APP.pie = function(tag, data, options) {
    var containerElement = tag,
        w = options.width,
        h = options.height,
        data = data
        , h_offset = options.margin.left || options.width * 0.15
        , v_offset = options.margin.top || options.width * 0.15;

    // object to be returned
    var that = {};

    var draw = function () {
        var radius = Math.min(w, h) / 2;
        //var outerRadius = Math.min(w, h) / 3;
        var color = d3.scale.category20();

        var arc = d3.svg.arc().outerRadius(radius - 10).innerRadius(0);
        var pie = d3.layout.pie().sort(null).value(function (d) {
            return Math.abs(d.weight);
        });

        // create svg element
        var svg = d3.select(containerElement)
            .append('svg').attr('width', w+2*h_offset)
            .attr('height', h + 2*v_offset)
            .append('g')
            .attr('transform', 'translate(' + (radius + h_offset) + "," + (radius + v_offset) +')');

        // render chart in svg
        var render = function (data) {
            var hoverIndex = -1;

            // create arcs
            var g = svg.selectAll('.arc')
                .data(pie(data))
                .enter()
                .append('g')
                .attr('class', arc)
                .on("click", function (d, i) {
                    if (i != hoverIndex) {
                        hoverIndex = i;
                        repaint(i);
                    }
                })
                .on("mouseout", function (d, i) {
                    if (hoverIndex != -1) {
                        hoverIndex = -1;
                        reset();
                    }
                });

            // fill colors
            g.append('path')
                .attr('d', arc)
                .style('fill', function (d, i) {
                    return color(i);
                })
                .transition()
                .duration(100);

            // add text on the right places
            g.append('text')
                .attr('transform', function (d) {
                    return 'translate(' + arc.centroid(d)[0]*1.5 + ',' + arc.centroid(d)[1]*1.5+')';
                })
                .attr('dy', '.35em')
                .style('text-anchor', 'middle')
                .text(function (d, i) {
                    if (d.data.weight > 0) return d.data.ticker;
                });

            // animation - transalate slice of pie
            function repaint(ix) {
                g.data(pie(data))
				.transition(100)
				.attr("transform", function (d, i) {
				    if (i === ix) return "translate(" + arc.centroid(d)[0] / 2 + "," + arc.centroid(d)[1] / 2 + ")";
				})
            };

            function reset() {
                g.data(pie(data))
				.transition(100)
				.attr("transform", function (d, i) {
				    return "translate(" + 0 + "," + 0 + ")";
				});

            };
        };
        render(data);
    }

    // public member functions
    that.draw = draw;

    // return the newly created object with public member function draw
    return that;
};
