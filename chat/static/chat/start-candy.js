$(document).ready(function() {
	//Fetch our data elements
	var jid = $('#candy').data('jid');
	var nick = $('#candy').data('nick');
	var domain = $('#candy').data('domain');
	var otp = $('#candy').data('otp');
	var assets = $('#candy').data('candy-assets');


	//Initialize Candy
	Candy.init('/http-bind/', {
		core: {
			debug: false,
			autojoin: ['nano@conf.'+domain]
			},
		view: {
			assets: assets,
			enableXHTML: true,
			updateWindowOnAllMessages: true
			}
	});

	//Emphasis plugin
	CandyShop.Emphasis.init();

	//Connect
	Candy.Core.connect(jid, otp, nick);
});
