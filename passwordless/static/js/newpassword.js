$(function() {
	var clipboard = new Clipboard('#password');

	clipboard.on('success', function(e) {
		console.info('Action:', e.action);
		console.info('Text:', e.text);
		console.info('Trigger:', e.trigger);

		e.clearSelection();
	});
});
