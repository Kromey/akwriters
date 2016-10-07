$(function() {
	$('#new_password_name').keyup(function(event) {
		if($('#new_password_name').val())
		{
			$('#generate_new_password').removeAttr("disabled")
		} else {
			$('#generate_new_password').attr("disabled", "disabled")
		}
	});

	$('#revoke_modal').on('show.bs.modal', function (event) {
		var button = $(event.relatedTarget); // Button that triggered the modal
		var pass_id = button.data('password-id'); // Extract info from data-* attributes
		
		$('#password-id').val(pass_id);
	});

	$('#new_password_form').submit(function(event) {
		$('#generate_modal').modal({keyboard:false,backdrop:'static'});
		event.preventDefault();
	});
	$('#generate_modal').on('show.bs.modal', function(event) {
		$('#password_results').hide();
		$('#password_generating').show();
			$('#password_done_btn').addClass('disabled');
	});
	$('#generate_modal').on('shown.bs.modal', function(event) {
		var form = $('#new_password_form')

		$.post(form.attr('action'), form.serialize(), function(data) {
			$('#password_results').html(data);

			$('#password_results').show();
			$('#password_generating').hide();
			$('#password_done_btn').removeClass('disabled');

			$('#password').focus(function() { $(this).select(); } );
		});
	});

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
