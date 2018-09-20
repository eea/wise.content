(function(window, document, $){
    var selectorFormContainer = ".wise-search-form-container";
    /*
    * SELECT2 functions
    * */
    function setupRightSelects2(selector){
        var forbiddenIDs = ["form-widgets-member_states-from", "form-widgets-member_states-to" ];
        var selectorFormCont = selector || selectorFormContainer;

        $( selectorFormCont + " select").each(function (ind, selectElement) {
            var selectedElementID = $(selectElement).attr("id");
            if( forbiddenIDs.indexOf(selectedElementID) !== -1 ){
                return false;
            }

            $(selectElement).addClass("js-example-basic-single");
            var lessOptions = $(selectElement).find("option").length < 10;

            var $wise_search_form = $(selectorFormCont);

            var options = {
                placeholder: 'Select an option',
                closeOnSelect: true,
                dropdownAutoWidth : true,
                width: '100%',
                theme: "flat"
            };
            if(lessOptions) options.minimumResultsForSearch = Infinity;

            $(selectElement).select2(options);

            /*$(selectElement).on("select2-selecting", function(ev) {

            });*/
        });
    }

    function initStyling(){
        //$("#form-buttons-continue").hide("fast");
        $(".button-field").addClass("btn");

    }

    function setupFormToggle2(){
        var $formToCollapse = $("#comp-national-descriptor");

        $formToCollapse.before("<div id='slide-up-form' data-toggle='collapse'" +
            " data-target='" + ".comp-national-descriptor-collapse" +
            "' class='panel-heading panel-title'>Show form</div>");

        $("#comp-national-descriptor")
            .addClass( "comp-national-descriptor-collapse")
            .addClass("collapse")
            .addClass("panel")
            .addClass("panel-default");

        var isCollapsed = function(){
            $("#slide-up-form").removeClass("form-collapsed");
            $("#slide-up-form").text("Show form");
        };

        var notCollapsed = function(){
            $("#slide-up-form").addClass("form-collapsed");

            $("#slide-up-form").text("Hide form");
            $formToCollapse.css({
                "border-top-left-radius" : "0",
                "border-top-right-radius" : "0"
            });
        };

        $("#slide-up-form").on("click", function (ev) {
            $formToCollapse.collapse();

        });

        $formToCollapse.on("hidden.bs.collapse",function(){
            isCollapsed();
        });
        $formToCollapse.on("show.bs.collapse",function(){
            notCollapsed();
        });

        $formToCollapse.collapse('show');

    }

    function setupFormToggle(){
        var accordeons = $("[data-toggle='collapse']");

        $.each(accordeons , function(idx, accordion){
            var target = $(accordion).attr("data-target");
            var $target = $(target);
            var $accordion = $(accordion);

            $(accordion).on("click", function (ev) {
                ev.preventDefault();
                $target.collapse();
            });
            var isCollapsed = function(){
                $accordion.removeClass("form-collapsed");
                $accordion.text("Show form");
            };

            var notCollapsed = function(){
                $accordion.addClass("form-collapsed");

                $accordion.text("Hide form");
                $accordion.css({
                    "border-top-left-radius" : "0",
                    "border-top-right-radius" : "0"
                });
            };

            $formToCollapse.on("hidden.bs.collapse",function(){
                isCollapsed();
            });
            $formToCollapse.on("show.bs.collapse",function(){
                notCollapsed();
            });

        });
    }

    $(document).ready(function($){
        initStyling();
        setupRightSelects2();

        //setupFormToggle();

    });
}(window, document, $));
