function gotoStep(ref, step, old_step) 
{
    $("#"+ref+"\\:"+step).trigger("pre_on_step");

    if (!(old_step === undefined))
    {
        $("#"+ref+"\\:"+old_step).css("display", "none");
    }
    else
    {
        $("#"+ref).children("div").css("display", "none");
    }

    $("#"+ref+"\\:"+step).css("display", "block").trigger("on_step");
}

function toggle_option(ref, option)
{
    if (!(option === undefined))
    {
        $("#"+ref).children().removeClass("ui-selected");
    }
    $("#"+ref).children("#"+option).addClass("ui-selected");
}

/**
 *  * Transform text into a URL slug: spaces turned into dashes, remove non alnum
 *   * @param string text
 *    */
function slugify(text) {
    text = text.toLowerCase();
    text = text.replace(/[^-a-zA-Z0-9,&\s]+/ig, '');
    text = text.replace(/-/gi, "_");
    text = text.replace(/\s/gi, "-");
    return text;
}

function validate_key() {
    $.getJSON('/node/json/check_name/'+$("#new_node\\:req\\:key").val(), function(data) {
    var key_error = $("#new_node\\:req\\:key\\:error");
        if (data.exists)
        {
           $("#new_node\\:req\\:key").addClass("ui-state-error");
            key_error.children(".form_error_text").text(
                "This key is not available. Please fix it!")
            key_error.children(".form_error_icon").removeClass(
                "ui-icon-check").addClass("ui-icon-alert");
        }
        else
        {
            $("#new_node\\:req\\:key").removeClass("ui-state-error");
            key_error.removeClass("ui-state-error");
            key_error.children(".form_error_text").text(
                "This key is available.")
            key_error.children(".form_error_icon").removeClass(
                "ui-icon-alert").addClass("ui-icon-check");
        }
    });
}
