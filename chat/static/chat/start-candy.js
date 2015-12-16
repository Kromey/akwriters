$(document).ready(function() {
	//Fetch our data elements
	var username = $('#candy').data('username').toLowerCase();
	var domain = $('#candy').data('domain').toLowerCase();
	var assets = $('#candy').data('candy-assets');

	//Initialize Candy
	Candy.init('/http-bind/', {
		core: {
			debug: false,
	autojoin: ['nano@conf.'+domain]
		},
	view: {
		assets: assets,
	enableXHTML: true
	}
	});

	//Connect
	Candy.Core.connect();

	//Add a customized header to the Candy login window
	var header = document.createElement('div');
	header.appendChild(document.createTextNode('Alaska Writers Chat'));
	var modal = $('#chat-modal').get(0);
	modal.insertBefore(header, modal.firstChild);

	//Give the user a bit of a hint for their username
	$('#username').val(username+'@'+domain);
});
