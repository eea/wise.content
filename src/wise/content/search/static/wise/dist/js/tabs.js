function clickFirstTab(){$("#tabs-wrapper ul li:first-child a").trigger("click"),$(".tabs-wrapper ul li:first-child a").trigger("click")}setupTabs=function(a){function b(a){var b=$("ul.nav:not(.topnav) > li"),c=b.length;if(c>1){var d=2===c?35:Math.floor((100-c)/c);b.css("width",d+"%");var e=$("ul.nav").width(),f=Math.floor(e/100);$(b).css({"margin-left":0,"margin-right":f/2+"px"})}else $(b).css({"margin-left":0})}function c(a){var a=a||"#mainform-tabs";b(a);var c=function(){var a=$(" ul.topnav li").length||0;if(0===a)return!1;var b=100/a-1,c=100-b*a-1,d=c/a;$(".topnav li").css({width:b+"%","margin-right":d+"%"})};if(1===$(a+" ul li").length){$("#tabContents").removeClass("tab-content"),$(a+" ul").attr("class",""),$(a+" ul li").css({"background-color":"transparent","float":"none"});var d=$(a+" ul li a").text();$(a+" ul li").append("<h4>"+d+"</h4>"),$(a+" ul li a").remove(),$(a+" .tab-pane").removeClass("fade")}c()}c(a),clickFirstTab()},jQuery(document).ready(function(a){function b(b){var c=a(b.element[0]),d=""!==c.attr("data-subtitle")?"("+c.attr("data-subtitle")+")":"";return'<span style="font-size: 1.5rem; font-weight: bold;color: #337ab7">'+c.attr("data-maintitle")+'</span> <span style="color: #337ab7;font-size: 1.3rem;">'+d+"</span>"}setupTabs();var c="auto",d=!0;if(window.matchMedia("(max-width: 967px)").matches){c=!1,d=!1;var e={placeholder:"Select an option",closeOnSelect:!0,dropdownAutoWidth:d,width:c,theme:"flat",minimumResultsForSearch:20,formatSelection:b,formatResult:b,containerCssClass:"mobile-select-article"};void 0!==a.fn.select2&&(0==a("#mobile-select-article option[selected='selected']").length&&a("#mobile-select-article").prepend('<option selected="selected" value="choose" data-maintitle="Choose..." data-subtitle="">Choose section</option>'),a("#mobile-select-article").select2(e),a("#mobile-select-article").one("select2-selecting",function(a){document.location.href=a.choice.id}),a("#mobile-select-article").on("select2-open",function(b){0==a("#mobile-select-article option[selected='selected']").length&&a(".select2-highlighted").css({background:"transparent"})}))}});
//# sourceMappingURL=tabs.js.map