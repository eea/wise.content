/* global setupTabs */

/*
* TABS
* */
function setupTabsInit() {
    var t = $("ul.nav:not(.topnav) > li");

    // top tabs width calculation
    var nrtabs = t.length;
    if(nrtabs > 1) {
        var tabLength = nrtabs === 2 ? 35 : Math.floor((100 - nrtabs) / nrtabs );

        t.css("width", tabLength + "%");
        var rest = 100 - tabLength * nrtabs;

        var totalL = $("ul.nav").width();
        var mrR = Math.floor( totalL /100 ) ;

        $(t).css({
            "margin-left": 0,
            "margin-right" : mrR/2 + "px"
        });

    } else {
        $(t).css({"margin-left": 0});
    }
    /* david commented
    if ($("#tabs-wrapper ul").find("li").length === 0){
        if( $("#tabs-wrapper").find("ul").length ===  0 ){ //return true;
        }
        //if($("#tabs-wrapper").find("ul li").length === 0) $("#tabs-wrapper").hide();
    } */
    var tabswrapper = "#tabs-wrapper";

    $.each( $( ".tabs-wrapper") , function (indx, item) {
        if($(item).find("ul").length ===  0){ return true;}
        //if($(item).find("ul li").length === 0) $(".tabs-wrapper").hide();
    });

    if( $( tabswrapper + " ul li").length === 1 ){
        $("#tabContents").removeClass("tab-content");
        $( tabswrapper + " ul").attr("class", "");
        $( tabswrapper + " ul li").css({
            "background-color": "transparent",
            "float" : "none"
        });
        var lt = $( tabswrapper + " ul li a").text();
        $( tabswrapper + " ul li").append("<h4>" + lt + "</h4>");
        $( tabswrapper + " ul li a").remove();
        $( tabswrapper + " .tab-pane").removeClass("fade");
    }

    //TODO: eliminate "#wise-search-form"
    var nrTabs = $( " ul.topnav li").length || "0";

    var wdth = (100/nrTabs) - 1;

    var rest = 100 - (wdth * nrTabs);

    $( ".topnav li").css({
        "width": wdth  + "%",
        //"margin-right": (rest/nrTabs)/nrTabs + "%"
    });

}

function clickFirstTab(){
    $("#tabs-wrapper ul li:first-child a").trigger('click');
    $(".tabs-wrapper ul li:first-child a").trigger('click');
}
/*
* TABS END
* */

setupTabs = function () {
    setupTabsInit();
    clickFirstTab();
}

jQuery(document).ready(function($){
    setupTabs();
});