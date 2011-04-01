function toggle_comment(id){
	var item = $("#" + id);

	if (item.css("display") == "none")
	{
		$("#" + id).css("display", "block");
	}
	else
	{
		$("#" + id).css("display", "none");
	}
}
