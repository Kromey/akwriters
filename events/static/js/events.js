$(function() {
	$('.gcal-control input[type=checkbox]').change(function() {
		target = $(this).val()
		if($(this).is(':checked')) {
			$(this).parent().removeClass('gcal-control-disabled')
			$('.'+target).show()
		} else {
			$(this).parent().addClass('gcal-control-disabled')
			$('.'+target).hide()
			$(this).parent().show()
		}
	});
});
