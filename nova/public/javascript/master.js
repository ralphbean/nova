function toggle_option(ref, option)
{
    if (!(option === undefined))
    {
        $("#"+ref).children().removeClass("ui-selected");
    }
    $("#"+ref).children("#"+option).addClass("ui-selected");
    $("#sel_type").val(option);
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

var _key_avail;
function validate_key() {
    var val = $("#new_node_key").val();
    var key_error = $("#new_node_key_error");

    if (val.length >= 3)
    {
        var ret_code = $.getJSON('/node/json/check_name/'+val, function(data) {
            if (data.exists)
            {
               $("#new_node_key").addClass("ui-state-error");
                key_error.children(".form_error_text").text(
                    "This key is not available. Please fix it!");
                key_error.children(".form_error_icon").removeClass(
                    "ui-icon-check").addClass("ui-icon-alert");
                _key_avail = false;
            }
            else
            {
                $("#new_node_key").removeClass("ui-state-error");
                key_error.removeClass("ui-state-error");
                key_error.children(".form_error_text").text(
                    "This key is available.");
                key_error.children(".form_error_icon").removeClass(
                    "ui-icon-alert").addClass("ui-icon-check");
                _key_avail = true;
            }
        });
        return _key_avail;
    }
    else
    {
        $("#new_node_key").addClass("ui-state-error");
        key_error.children(".form_error_text").text(
            "The key must be atleast 3 characters long. Please fix it!");
        key_error.children(".form_error_icon").removeClass(
            "ui-icon-check").addClass("ui-icon-alert");

        return false;
    }
}

function onNewNodeTypeClick() 
{
    toggle_option("new_node_sel_type", $(this).attr('id'));
    $.getJSON('/node/json/get_type/'+$(this).attr('id'), function (data) {
        var w_loc = $("#additional-widgets");
        w_loc.empty();
        $.each(data.type['req_attrs'], function(i, value) {
            var w = $("<div></div>").load("/widgets/"+value['key'], {'name':value["key"]});
            w_loc.append(w);
        });
    });
}
