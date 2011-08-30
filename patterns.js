var treemap = null;
var node_template = null;
var tooltip_template = null;

function show_tooltip(tip, node, isLeaf, domElement) {
    tip.innerHTML = tooltip_template(node);
}

function create_label(domElement, node) {
    domElement.innerHTML = node_template(node);
    
    if (node.getSubnodes().length > 1) {
        var style = domElement.style;

        style.cursor = 'default';
        
        domElement.onmouseover = function() {
            style.cursor = 'pointer';
        };
        
        domElement.onmouseout = function() {
            style.cursor = 'default';
        };
    }
}

function recurse_reshape(node, datum) {
    node['data']['$area'] = node['data'][datum];

    _.each(node['children'], function(child) {
        recurse_reshape(child, datum);
    });
}

function reshape_treemap(datum) {
    if (!_.isUndefined(datum)) {
        recurse_reshape(DATA, datum);
    }

    treemap.loadJSON(DATA);
    treemap.refresh();
    $(".controls button").removeAttr('disabled');
    $(".controls button." + datum).attr('disabled', 'disabled');
}

function create_treemap(data) {
    treemap = new $jit.TM.Squarified({
        injectInto: 'infovis',
        levelsToShow: 1,
        titleHeight: 35,
        Events: {  
            enable: true,  
            onClick: function(node) {  
                if(node) {
                    if (node == treemap.clickedNode) {
                        treemap.out();
                    } else if (node.getSubnodes().length > 1) {
                        treemap.enter(node);
                    }
                }
            },  
            onRightClick: function() {  
                treemap.out();  
            }  
        },   
        Tips: {
            enable: true,
            offsetX: 20,
            offsetY: 20,
            onShow: show_tooltip
        },
        onCreateLabel: create_label 
    });

    treemap.loadJSON(data);
    treemap.refresh();
}

$(function init() {
    node_template = _.template($("#node-template").html());
    tooltip_template = _.template($("#tooltip-template").html());

    create_treemap(DATA);
    $("button.establishments").attr('disabled', 'disabled');

    $(window).resize(function() {
        treemap = null;
        $("#infovis").html("");
        create_treemap(DATA);
    });
});
