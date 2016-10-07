function enableGenerate()
{
	if($('#new_password_name').val())
	{
		$('#generate_new_password').removeAttr("disabled")
	} else {
		$('#generate_new_password').attr("disabled", "disabled")
	}
}

$(function() {
	$('#revoke_modal').on('show.bs.modal', function (event) {
		var button = $(event.relatedTarget); // Button that triggered the modal
		var pass_id = button.data('password-id'); // Extract info from data-* attributes
		
		$('#password-id').val(pass_id);
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
		});
	});
});
