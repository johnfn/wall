function toggle_comment(id){
	var item = $("#" + id);

	if (item.css("display") == "none") {
		$("#" + id).css("display", "block");
	} else {
		$("#" + id).css("display", "none");
	}
}
/* ensure that CSRF token is sent with AJAX requests */
$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
$.fn.setDefaultValue = function(value) {
	var DEFAULT_CLASS = "wispy";
    return this.each(function() {
        var jQueryObj = $(this);
        jQueryObj.blur(function() {
    	    if (!jQueryObj.val() || jQueryObj.val() == value) {
    	        jQueryObj.val(value);
    	        jQueryObj.addClass(DEFAULT_CLASS);
            }
    	}).focus(function() {
    	    if (jQueryObj.val() == value) {
    	        jQueryObj.removeClass(DEFAULT_CLASS);
    	        jQueryObj.val("");
            }
        }).val(value);
    }).addClass(DEFAULT_CLASS);
}
$(function() {
    var question = $("#challent textarea");
    var postButton = $("#challent input.button");
    question.setDefaultValue("I'd like to comment...");
    $("#candidatedropdown").hide()
    $("#choices a.tab").live('click', function() {
        $("#candidatedropdown").toggle()

        if ($("#candidatedropdown").css("display") == "none")
            {
                $("#posttype").attr("name", "comment");
            }
        else
            {
                $("#posttype").attr("name", "challenge");
            }

        $("#choices div.tab").replaceWith(function() {
            return '<a href="javascript:void(0);" class="tab">' + $(this).html() + '</a>';
        });
        var self = $(this);
        self.replaceWith(function() {
            return '<div class="tab">' + $(this).html() + '</div>';
        });
        question.setDefaultValue("I'd like to" + self.text().toLowerCase() + "...");
        postButton.val(self.text().replace(" ", "") + "!");
    });
    $("#posts .comment .foldout textarea").setDefaultValue("Post a reply to the thread above.");
});