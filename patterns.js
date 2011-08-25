var treemap = null;
var node_template = null;
var tooltip_template = null;

function show_tooltip(tip, node, isLeaf, domElement) {
    tip.innerHTML = tooltip_template(node);
}

function create_label(domElement, node) {
    domElement.innerHTML = node_template(node);

    var style = domElement.style;
    style.display = '';
    style.border = '1px solid transparent';
    
    domElement.onmouseover = function() {
        style.border = '1px solid #9FD4FF';
    };
    
    domElement.onmouseout = function() {
        style.border = '1px solid transparent';
    };
}

function reshape_treemap(datum) {
    if (!_.isUndefined(datum)) {
        DATA['data']['$area'] = DATA['data'][datum];

        _.each(DATA['children'], function(child) {
            child['data']['$area'] = child['data'][datum];
        });
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
        titleHeight: 0,
        Events: {  
            enable: true,  
            onClick: function(node) {  
                if(node) {
                    treemap.enter(node);
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
