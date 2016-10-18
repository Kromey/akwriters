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

	//Not the standard method Bootstrap's docs recommend, but we'll need
	//the data-toggle attribute for the details modal.
	$('.event').tooltip();
});
