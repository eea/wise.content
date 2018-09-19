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

            $(selectorFormCont + " #s2id_form-widgets-marine_unit_id").hide();

            var removePaginationButtons = function(){
                $wise_search_form.find("[name='form.buttons.prev']").remove();
                $wise_search_form.find("[name='form.buttons.next']").remove();
                $wise_search_form.find("[name='form.widgets.page']").remove();
            };

            $(selectElement).on("select2-selecting", function(ev) {
                // remove results following form-widgets-article select element
                // as we want to reset each facet to it's initial value if we change form
                if( $(this).attr("id") === "form-widgets-article" ) {
                    $(ev.target).closest(".form-right-side").next().remove();
                }

                removePaginationButtons()

                var self = this;
                window.setTimeout( function (){
                    $(selectorFormCont + " .formControls #form-buttons-continue").trigger("click", {'select': self});
                }, 300);

            });
        });
    }

    function initStyling(){
        //$("#form-buttons-continue").hide("fast");
        $(".button-field").addClass("btn");

    }

    $(document).ready(function($){
        initStyling();
        setupRightSelects2();
    });
}(window, document, $));
