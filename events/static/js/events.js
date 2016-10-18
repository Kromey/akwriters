$(function() {
	$('.gcal-control').click(function() {
		target = $(this).data('target');
		if($(this).hasClass('gcal-control-disabled')) {
			$(this).removeClass('gcal-control-disabled');
			$('.event.'+target).slideDown(500);
		} else {
			$(this).addClass('gcal-control-disabled');
			$('.event.'+target).slideUp(500);
		}
		$(this).blur();
	});
});
