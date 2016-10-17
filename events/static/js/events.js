$(function() {
	$('.gcal-control input[type=checkbox]').change(function() {
		target = $(this).val();
		if($(this).is(':checked')) {
			$(this).parent().removeClass('gcal-control-disabled');
			$('.event.'+target).slideDown();
		} else {
			$(this).parent().addClass('gcal-control-disabled');
			$('.event.'+target).slideUp();
		}
		$(this).blur();
	});

	// Fix FF being stupid
	$('.gcal-control input').prop('checked', true);
});
