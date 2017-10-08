$(function(){
	$('.dropdown-submenu a.dropdown-toggle').click(function(e){
		$(this).next('ul').toggle();
		$(this).parent().toggleClass('submenu-open');
		e.stopPropagation();
		e.preventDefault();
	});

	$('textarea[data-provide=markdown]').markdown({
		onPreview: function (e, previewContainer) {
			$.ajax({ method: "POST", url: "/forum/preview", data: $('#post-form').serialize() })
			.then(function (result) {
				previewContainer.html(result);
			});

			return "Formatting...";
		}
	});
});
