var treemap = null;
var node_template = null;
var tooltip_template = null;
var current_datum = null;

function show_tooltip(tip, node, isLeaf, domElement) {
    tip.innerHTML = tooltip_template(node);
}

function create_label(domElement, node) {
    domElement.innerHTML = node_template(node);
    
    if (node.getSubnodes().length > 2) {
        domElement.className += " clickable";
    }
}

function recurse_reshape(node, datum) {
    node["data"]["$area"] = node["data"][datum];

    _.each(node["children"], function(child) {
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

    current_datum = datum;
    update_hash();
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
                        update_hash();
                    } else if (node.getSubnodes().length > 2) {
                        treemap.enter(node);
                        update_hash();
                    }
                }
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

function update_hash(){
    if (treemap.clickedNode) {
        id = treemap.clickedNode.id;
    } else {
        id = null;
    }

    window.location.hash = [current_datum, id].join(",");
}

function parse_hash() {
    hash = window.location.hash;

    if (!hash) {
        return;
    }

    hash = hash.replace('#','');

    parts = hash.split(',');

    if (parts) {
        datum = parts[0];
        id = parts[1];

        if (id) {
            node = treemap.graph.getNode(id);
            treemap.enter(node);
        }

        if (datum) {
            reshape_treemap(datum);
        }
    }
}

$(function init() {
    node_template = _.template($("#node-template").html());
    tooltip_template = _.template($("#tooltip-template").html());
    
    current_datum = "annual_payroll";
    $("button.annual_payroll").attr('disabled', 'disabled');

    create_treemap(DATA);
    parse_hash();

    $(window).resize(function() {
        treemap = null;
        $("#infovis").html("");
        create_treemap(DATA);
        parse_hash();
    });
});
