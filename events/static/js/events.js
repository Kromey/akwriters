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
			if($(this).children(visible_events).length > 4) {
				$(this).children('.more-events').slideDown(duration);
			} else {
				$(this).children('.more-events').slideUp(duration);
			}
		});
		count_extra_events(visible_events);

		$(this).blur();
	});

	var count_extra_events = function(filter) {
		$('div.calendar-day').each(function(){
			var events = $(this).children(filter).length;
			events -= 3;

			var duration = 300;
			var span = $(this).children('.more-events').children('span');

			span.fadeOut(duration, function() {
				$(this).html('+'+events);
				$(this).fadeIn(duration);
			});
		});
	};
	count_extra_events('.event');

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
		$('#date-events').children('.date-events-container').each(function() {
			$(this).html(day.children('div.'+$(this).data('class')).clone());
			$(this).children().show();
			// Re-enable tooltips on the cloned events
			$(this).children().tooltip();
		});
	});

	//Not the standard method Bootstrap's docs recommend, but we'll need
	//the data-toggle attribute for the details modal.
	$('.event,.month-control').tooltip();
});
