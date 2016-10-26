$(function() {
	$('.gcal-control').click(function() {
		var target = $(this).data('target');
		var showing = $(this).hasClass('gcal-control-disabled');

		var duration = 500;

		if(showing) {
			$(this).removeClass('gcal-control-disabled');
			$('.event.'+target).slideDown(duration);
			var visible_events = '.event:visible';
		} else {
			$(this).addClass('gcal-control-disabled');
			$('.event.'+target).slideUp(duration);
			var visible_events = '.event:not(.'+target+'):visible';
		}

		$('div.calendar-day').each(function(){
			if($(this).children(visible_events).length > 3) {
				$(this).children('.more-events').show();
				$(this).children('.more-events').children('span').fadeIn(duration);
			} else {
				$(this).children('.more-events').children('span').fadeOut(duration, function(){
					$(this).parent().hide();
				});
			}
		});

		$(this).blur();
	});

	$('#event-modal').on('show.bs.modal', function(event) {
		var trigger = $(event.relatedTarget);

		$('#event-title').html(trigger.data('summary'));
		$('#event-date').html(trigger.data('date'));
		$('#event-when').html(trigger.data('time'));
		$('#event-where').html(trigger.data('where'));
		$('#event-desc').html(trigger.data('details'));
		$('#event-link').attr('href', trigger.data('href'));

		trigger.tooltip('hide');
	});
	$('#date-modal').on('show.bs.modal', function(event) {
		var trigger = $(event.relatedTarget);
		var day = trigger.parent();

		$('#date-date').html(day.data('date'));
		$('#date-events').html(day.children('div.event').clone());
		// Re-enable tooltips on the cloned events
		$('#date-events').children('.event').tooltip();

		$('#date-events .event').show();
	});

	//Not the standard method Bootstrap's docs recommend, but we'll need
	//the data-toggle attribute for the details modal.
	$('.event,.month-control').tooltip();
});
