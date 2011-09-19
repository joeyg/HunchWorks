$(function()
{

  var init_token_input = function(class_name, theme)
  {
    $("input." + class_name).each(function()
    {
      var field = $(this);

      field.tokenInput(field.data("search-url"), {
        prePopulate: field.data("prepopulate"),
        preventDuplicates: true,
        animateDropdown: false,
        theme: theme
      });
    });
  };

  init_token_input("tags", "facebook");
  init_token_input("skills", "");
  init_token_input("languages", "");
  init_token_input("userProfiles", "hunchworks");
});


function popup(mylink, windowname)
{
	if (! window.focus)
	{
		return true;
	}
	var href;
	if (typeof(mylink) == 'string')
	{
		href=mylink;
		window.open(href, windowname, 'width=400,height=200,scrollbars=yes');
		return false;
	}
	else
	{
		href=mylink.href;
		window.open(href, windowname, 'width=400,height=200,scrollbars=yes');
		return false;
	}
}
