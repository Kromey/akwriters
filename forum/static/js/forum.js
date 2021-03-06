$(function(){
	$('.dropdown-submenu a.dropdown-toggle').click(function(e){
		$(this).next('ul').toggle();
		$(this).parent().toggleClass('submenu-open');
		e.stopPropagation();
		e.preventDefault();
	});

	$('#show-source, #hide-source').click(function(){
		$('.post, .post-source').slideToggle();
	});

	$('#toolbar-reply').click(function(e){
		$('#post-form').show();
		$('#reply').hide();

		e.stopPropagation();
		e.preventDefault();
	});
	$('#reply, #reply-cancel').click(function(){
		$('#post-form, #reply').toggle();
	});

	$('textarea[data-provide=markdown]').markdown({
		onPreview: function(e, previewContainer) {
			$.post("/forum/preview", $('#post-form').serialize())
			.done(function(result) {
				previewContainer.html(result);
			})
			.fail(function() {
				previewContainer.text('Oops! Something went wrong; preview is not available at the moment. Sorry. :-(');
			});

			return "Formatting...";
		}
	});
});
