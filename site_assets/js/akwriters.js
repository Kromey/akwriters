$(function() {
	$('[data-popup-uri]').click(function()
	{
		newWin = window.open($(this).data('popup-uri'), 'Candy', 'width=800,height=500');
		if(!newWin || newWin.closed || typeof newWin.closed=='undefined')
		{
			alert("Your browser has blocked the pop-up. Please allow pop-ups for this site.");
		}
		return false;
	});

	$('div.alert button.close').click(function(event) {
		$(this).blur();
		$(this).parent().slideUp();
	});

	//Calculate the % width of all progress bars
	$('div[role=progressbar]').width(function() {
		var vmin = parseFloat($(this).attr('aria-valuemin'));
		var vmax = parseFloat($(this).attr('aria-valuemax'));
		var vnow = parseFloat($(this).attr('aria-valuenow'));

		var width = (vnow - vmin)/(vmax - vmin);
		width = width * 100;
		return width+"%";
	});

	//Make textareas auto-grow to fit their content
	$('textarea').each(function()
	{
		$(this).focus(function() {
			var minHeight = $(this).css('min-height');
			if(parseInt(minHeight) <= 0)
			{
				minHeight = $(this).height();
				$(this).css('min-height', minHeight);
			}

			$(this).on('input', function (e) {
				$(this).css('height', minHeight);
				var newHeight = $(this)[0].scrollHeight+5;
				$(this).css('height', newHeight);
			});
		});
	});
});

