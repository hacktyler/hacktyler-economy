var treemap;

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

$(function init() {
    treemap = new $jit.TM.Squarified({
        injectInto: 'infovis',
        titleHeight: 30,
        animate: true,
        offset: 1,
        duration: 1000,
        Tips: {
            enable: true,
            offsetX: 20,
            offsetY: 20,
            onShow: show_tooltip
        },
        onCreateLabel: create_label 
    });

    treemap.loadJSON(DATA);
    treemap.refresh();

    $(window).resize(function() {
        treemap.refresh();
    });
});
