$(document).ready(function() {
    $.getJSON('/get-alpha-lambda', function(data){
        $('#alpha').val(data.alpha).next().html(data.alpha);
        $('#lambda').val(data.lambd).next().html(data.lambd);
    });

    var rangeSlider = function(){
        var slider = $('.range-slider'),
            range = $('.range-slider__range'),
            value = $('.range-slider__value');

        slider.each(function(){

            value.each(function(){
                var value = $(this).prev().attr('value');
                $(this).html(value);
            });

            range.on('input', function(){
                $(this).next(value).html(this.value);
            });
        });
    };

    rangeSlider();

    var nodes, links, nodes_dict, restart, timestamp, path, circle, svg, t;
    var width  = 5000,
        height = 800,
        colors = d3.scale.category10();
    var paused = true;
    var init = function(data) {
        console.log(data);
        timestamp = data.timestamp;
        nodes = data.nodes;
        nodes_dict = new Object();
        $.each(nodes, function(index, node){
            nodes_dict[node.id] = node;
        });
        links = data.edges;
        $.each(links, function(index, link){
            link.source = nodes_dict[link.source];
            link.target = nodes_dict[link.target];
        });

        svg = d3.select('#d3')
          .append('svg')
          .attr('oncontextmenu', 'return false;')
          .attr('width', width)
          .attr('height', height);



        var force = d3.layout.force()
            .nodes(nodes)
            .links(links)
            .size([width, height])
            .linkDistance(100)
            .charge(-500)
            .on('tick', tick);

        svg.append('svg:defs').append('svg:marker')
            .attr('id', 'end-arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 6)
            .attr('markerWidth', 3)
            .attr('markerHeight', 3)
            .attr('orient', 'auto')
          .append('svg:path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', '#000');

        svg.append('svg:defs').append('svg:marker')
            .attr('id', 'start-arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 4)
            .attr('markerWidth', 3)
            .attr('markerHeight', 3)
            .attr('orient', 'auto')
          .append('svg:path')
            .attr('d', 'M10,-5L0,0L10,5')
            .attr('fill', '#000');

        path = svg.append('svg:g').selectAll('path');
        circle = svg.append('svg:g').selectAll('g');


        function tick() {
          path.attr('d', function(d) {
            var deltaX = d.target.x1 - d.source.x1,
                deltaY = d.target.y1 - d.source.y1,
                dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
                normX = deltaX / dist,
                normY = deltaY / dist,
                sourcePadding = d.left ? 17 : 12,
                targetPadding = d.right ? 17 : 12,
                sourceX = d.source.x1 + (sourcePadding * normX),
                sourceY = d.source.y1 + (sourcePadding * normY),
                targetX = d.target.x1 - (targetPadding * normX),
                targetY = d.target.y1 - (targetPadding * normY);
            return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;
          });

          circle.attr('transform', function(d) {
            return 'translate(' + d.x1 + ',' + d.y1 + ')';
          });
        }
        restart = function() {
          path = path.data(links);

          path.classed('selected', function(d) { return d === selected_link; })
            .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
            .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; });


          path.enter().append('svg:path')
            .attr('class', 'link')
            .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
            .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; })


          path.exit().remove();


          circle = circle.data(nodes, function(d) { return d.id; });


          circle.selectAll('circle')
            .style('fill',  function(d) { return (d.user_created) ? d3.rgb("#d62728"): d3.rgb("#1f77b4"); })
            .classed('reflexive', function(d) { return d.reflexive; });

          // add new nodes
          var g = circle.enter().append('svg:g');

          g.append('svg:circle')
            .attr('class', 'node')
            .attr('r', 12)
            .style('fill', function(d) { return (d.user_created) ? d3.rgb("#d62728"): d3.rgb("#1f77b4"); })
            .style('stroke', function(d) { return (d.user_created) ?  d3.rgb("#d62728").darker().toString(): d3.rgb("#1f77b4").darker().toString(); })
            .classed('reflexive', function(d) { return d.reflexive; })

          g.append('svg:text')
              .attr('x', 0)
              .attr('y', 4)
              .attr('class', 'id')
              .text(function(d) { return d.id; });


          circle.exit().remove();
          force.start();
        };

        restart();
        t = setTimeout(update, 1000);
    };

    var update = function() {
        $.getJSON('/get_graph', {'timestamp': timestamp}, function(data) {
            console.log(data);
            if(data.flag) {
                timestamp = data.timestamp;
                $.merge(nodes, data.nodes);
                $.each(data.nodes, function(index, node){
                    nodes_dict[node.id] = node;
                });
                $.each(data.edges, function(index, link){
                    link.source = nodes_dict[link.source];
                    link.target = nodes_dict[link.target];
                });
                $.merge(links, data.edges);
                path = svg.append('svg:g').selectAll('path');
                circle = svg.append('svg:g').selectAll('g');
                restart();
             }
             t = setTimeout(update, 1000);
        });
    };
    var pause = function(){
        paused = !paused;
        $('#pause > i').toggleClass('fa-play fa-pause');
        $.post('/pause');
    }


    $('#pause').click(pause);
    $('#reset').click(function(){
        clearTimeout(t);
        if(!paused) {
            pause();
        }
        $.post('/reset', function() {
            $('#d3').html("");

            $.getJSON('/get_graph', init);
        });
    });

    $('#alpha').change(function() {
        $.post('/update-alpha', {'alpha': $('#alpha').val()});
    });

    $('#lambda').change(function() {
        $.post('/update-lambda', {'lambd': $('#lambda').val()});
    });

    $('#add').click(function() {
        $.post('/add');
    });

    $.getJSON('/get_graph', init);
});
