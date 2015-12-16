$('[data-popup-uri]').click(function()
{
	newWin = window.open($(this).data('popup-uri'), 'Candy', 'width=800,height=500');
	if(!newWin || newWin.closed || typeof newWin.closed=='undefined')
	{
		alert("Your browser has blocked the pop-up. Please allow pop-ups for this site.");
	}
	return false;
});

