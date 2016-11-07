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
	//NotifyMe plugin
	CandyShop.NotifyMe.init({nameIdentifier: ''});
	//Notifications plugin
	CandyShop.Notifications.init({notifyNormalMessage: true});
	//Add /me formatting (note: should be after most plugins)
	CandyShop.MeDoes.init();

	//Connect
	Candy.Core.connect(jid, otp, nick);
});
