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

    var w = "auto";
    var daw = true;

    if (window.matchMedia("(max-width: 967px)").matches){
        w = false;
        daw = false;

        function formatArticle (article) {
            var el = $(article.element[0]);
            var subtitle = el.attr("data-subtitle") !== "" ? "(" + el.attr("data-subtitle")  + ")" : '';
            return '<span style="font-size: 1.5rem; font-weight: bold;color: #337ab7">' + el.attr("data-maintitle")+ '</span> '+
                '<span style="color: #337ab7;font-size: 1.3rem;">'+ subtitle +'</span>';
        }

        var moptions = {
            placeholder: 'Select an option',
            closeOnSelect: true,
            dropdownAutoWidth : daw,
            width: w,
            theme: "flat",
            minimumResultsForSearch: 20,
            formatSelection: formatArticle,
            formatResult: formatArticle,
            containerCssClass : "mobile-select-article"
        };

        if($.fn.select2 !== undefined){
            if($("#mobile-select-article option[selected='selected']").length == 0 ){
                $("#mobile-select-article").prepend('<option selected="selected" value="choose" ' +
                    'data-maintitle="Choose..." data-subtitle="">Choose section</option>');
            }

            $("#mobile-select-article").select2(moptions);

            $("#mobile-select-article").one("select2-selecting", function (ev){
                document.location.href =  ev.choice.id;
            });

            $("#mobile-select-article").on("select2-open", function (ev){
                if($("#mobile-select-article option[selected='selected']").length == 0 ){
                    $(".select2-highlighted").css({
                        "background": "transparent",
                        //"color": ""
                    });
                }
            });

        }
    }
});