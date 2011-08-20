var treemap = null;

function show_tooltip(tip, node, isLeaf, domElement) {
    tip.innerHTML = "<div class=\"tip-title\">" + node.name + "</div><div class=\"tip-text\">";
}

function create_label(domElement, node) {
    domElement.innerHTML = node.name;

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

    /*treemap.op.morph(DATA, { 
        type: 'fade', 
        duration: 1000, 
        hideLabels: false, 
        transition: $jit.Trans.Quart.easeOut 
    });*/
}

function create_treemap(data) {
    treemap = new $jit.TM.Squarified({
        injectInto: 'infovis',
        titleHeight: 0,
        /*animate: true,*/
        duration: 1000,
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
    create_treemap(DATA);

    $(window).resize(function() {
        treemap = null;
        $("#infovis").html("");
        create_treemap(DATA);
    });
});
