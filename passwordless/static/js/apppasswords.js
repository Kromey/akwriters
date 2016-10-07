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
	})
});
