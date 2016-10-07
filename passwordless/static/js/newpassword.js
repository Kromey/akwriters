$(function() {
	var clipboard = new Clipboard('#copy_password');

	clipboard.on('success', function(e) {
		$('#password_copied').slideDown();

		e.clearSelection();
	});
	clipboard.on('error', function(e) {
		$('#password_error').slideDown();
	});

	$('#password').focus(function() { $(this).select(); } );
});
