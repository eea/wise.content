function setupTabsInit(){var a=$("ul.nav:not(.topnav) > li"),b=a.length;if(b>1){var c=2===b?35:Math.floor((100-b)/b);a.css("width",c+"%");var d=$("ul.nav").width(),e=Math.floor(d/100);$(a).css({"margin-left":0,"margin-right":e/2+"px"})}else $(a).css({"margin-left":0});var f="#tabs-wrapper";if($.each($(".tabs-wrapper"),function(a,b){if(0===$(b).find("ul").length)return!0}),1===$(f+" ul li").length){$("#tabContents").removeClass("tab-content"),$(f+" ul").attr("class",""),$(f+" ul li").css({"background-color":"transparent","float":"none"});var g=$(f+" ul li a").text();$(f+" ul li").append("<h4>"+g+"</h4>"),$(f+" ul li a").remove(),$(f+" .tab-pane").removeClass("fade")}var h=$(" ul.topnav li").length||"0",i=100/h-1;$(".topnav li").css({width:i+"%"})}function clickFirstTab(){$("#tabs-wrapper ul li:first-child a").trigger("click"),$(".tabs-wrapper ul li:first-child a").trigger("click")}setupTabs=function(){setupTabsInit(),clickFirstTab()},jQuery(document).ready(function(a){setupTabs()});
//# sourceMappingURL=tabs.js.map