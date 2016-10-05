$(document).ready(function() {
	//Fetch our data elements
	var username = $('#candy').data('username');
	var domain = $('#candy').data('domain');
	var otp = $('#candy').data('otp');
	var assets = $('#candy').data('candy-assets');

	var jid = username.toLowerCase() + '@' + domain.toLowerCase();

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
	Candy.Core.connect(jid, otp, username);
});
