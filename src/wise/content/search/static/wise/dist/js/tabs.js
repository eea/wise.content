function setupTabsInit(){var a=$("ul.nav:not(.topnav) > li"),b=a.length;if(b>1){var c=2===b?35:Math.floor((100-b)/b);a.css("width",c+"%");var d=$("ul.nav").width(),e=Math.floor(d/100);$(a).css({"margin-left":0,"margin-right":e/2+"px"})}else $(a).css({"margin-left":0});var f="#tabs-wrapper";if($.each($(".tabs-wrapper"),function(a,b){if(0===$(b).find("ul").length)return!0}),1===$(f+" ul li").length){$("#tabContents").removeClass("tab-content"),$(f+" ul").attr("class",""),$(f+" ul li").css({"background-color":"transparent","float":"none"});var g=$(f+" ul li a").text();$(f+" ul li").append("<h4>"+g+"</h4>"),$(f+" ul li a").remove(),$(f+" .tab-pane").removeClass("fade")}var h=$(" ul.topnav li").length||"0",i=100/h-1;$(".topnav li").css({width:i+"%"})}function clickFirstTab(){$("#tabs-wrapper ul li:first-child a").trigger("click"),$(".tabs-wrapper ul li:first-child a").trigger("click")}setupTabs=function(){setupTabsInit(),clickFirstTab()},jQuery(document).ready(function(a){function b(b){var c=a(b.element[0]),d=""!==c.attr("data-subtitle")?"("+c.attr("data-subtitle")+")":"";return'<span style="font-size: 1.5rem; font-weight: bold;color: #337ab7">'+c.attr("data-maintitle")+'</span> <span style="color: #337ab7;font-size: 1.3rem;">'+d+"</span>"}setupTabs();var c="auto",d=!0;if(window.matchMedia("(max-width: 967px)").matches){c=!1,d=!1;var e={placeholder:"Select an option",closeOnSelect:!0,dropdownAutoWidth:d,width:c,theme:"flat",minimumResultsForSearch:20,formatSelection:b,formatResult:b,containerCssClass:"mobile-select-article"};void 0!==a.fn.select2&&(0==a("#mobile-select-article option[selected='selected']").length&&a("#mobile-select-article").prepend('<option selected="selected" value="choose" data-maintitle="Choose..." data-subtitle="">Choose section</option>'),a("#mobile-select-article").select2(e),a("#mobile-select-article").one("select2-selecting",function(a){document.location.href=a.choice.id}),a("#mobile-select-article").on("select2-open",function(b){0==a("#mobile-select-article option[selected='selected']").length&&a(".select2-highlighted").css({background:"transparent"})}))}});
//# sourceMappingURL=tabs.js.map