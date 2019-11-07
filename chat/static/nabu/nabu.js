const MAX_MESSAGES = 100;

Vue.component('slide-toggle', {
	model: {
		prop: 'value',
		event: 'toggle',
	},
	props: {
		value: Boolean,
	},
	template: '<div class="slide-toggle"><slot></slot><div :class="[\'switch\', value?\'on\':\'\']" @click="$emit(\'toggle\', !value)"></div></div>',
})

var Nabu = new Vue({
	el: '#nabu',
	data: {
		status_msg: 'Connecting...',
		username: null,
		socket: null,

		rooms: {},
		current_room: null,

		roster_colors: {},

		chatbox: '',
		chatimg: null,
		img_maxsize: 1048576, //1MB

		retry_time: 0,
		retry_count: 0,

		dragging: false,

		show_notifications: false,
	},
	mounted: function() {
		let data = this.$el.dataset;

		this.connect(data.server, data.jwt);

		window.addEventListener('blur', this.onblur);
	},
	computed: {
		chat_json: function() {
			let data = {
				type: 'chat',
				from: this.username,
				room: this.current_room,
				timestamp: new Date(),
				id: this.newId(),
				body: this.chatbox.trim(),
			};

			if(this.chatimg) {
				data.img = this.chatimg;
			}

			return JSON.stringify(data);
		},
		chatimg_data: function() {
			return this.imageFromData(this.chatimg);
		},
		messages: function() {
			this.autoscroll();

			try {
				return this.rooms[this.current_room].messages;
			} catch(error) {
				return [];
			}
		},
		occupants: function() {
			try {
				const occupants = this.rooms[this.current_room].occupants.sort();

				occupants.forEach(o => {
					if(!(o in this.roster_colors)) {
						// Set a placeholder object to avoid doing this work more than once
						// Use this.$set() to ensure it's properly "reactive" in Vue
						this.$set(this.roster_colors, o, {});

						// What we're doing next isn't supported on older browsers...
						// ...in which case the "default" colors from the stylesheet will be used
						try {
							// Need to encode the string into a buffer
							const data = (new TextEncoder()).encode(o);

							// Hashing in the browser is done async as a Promise
							window.crypto.subtle.digest('SHA-256', data).then(digest => {
								// Convert the digest buffer into a byte array
								const bytes = new Uint8Array(digest);
								// Slice out 3 bytes for our R, G, and B channels
								let [r, g, b] = bytes.slice(0, 3);

								// Average each channel with 200% white to get a light pastel
								// We're also bit-shifting the result back to their final positions
								r = Math.floor((r + 512) / 3) << 16;
								g = Math.floor((g + 512) / 3) << 8;
								b = Math.floor((b + 512) / 3);

								// Put the channels back together and convert to a CSS hex color string
								const color = '#' + (r + g + b).toString(16);

								// And finally update roster_colors object
								// We're already "reactive" so no need to use this.$set here
								this.roster_colors[o] = {backgroundColor: color};
							}).catch(e => console.log('Error hashing', o, '[', e.name, e.message, ']'));
						} catch(error) {
							console.log('Could not hash', o, '[', error, ']');
						}
					}
				});

				return occupants;
			} catch(error) {
				return [];
			}
		}
	},
	watch : {
		chatbox: 'autoscroll',
	},
	methods: {
		connect: function(server, jwt) {
			console.log('Connecting to', server, 'with token', jwt);

			if(server && jwt) {
				let authn = {
					type: 'authn',
					timestamp: new Date(),
					from: null,
					token: jwt,
				}

				this.socket = new WebSocket(server);

				this.socket.onerror = error => {
					//TODO: What can we do here?
					console.log(error);
				};

				this.socket.onopen = evt => {
					this.status_msg = 'Authenticating...';
					this.retry_count = 0;

					// Send authn message
					this.socket.send(JSON.stringify(authn));
				};

				this.socket.onmessage = msg => {
					console.log(msg.data);
					this.handleMessage(JSON.parse(msg.data));
				};

				this.socket.onclose = evt => {
					if(this.status_msg) {
						this.status_msg = 'Failed!';
					}

					if(!evt.wasClean) {
						this.handleMessage({
							type: 'error',
							body: 'Connection Error Code '+evt.code,
						});
					}
					this.handleMessage({
						type: 'system',
						body: 'Disconnected from server!',
					});
				};
			}
		},
		handleMessage: function(msg) {
			console.log(msg);

			if(!msg.room) {
				msg.room = this.current_room;
			}

			switch(msg.type) {
				case 'authn':
					this.username = msg.from;
					this.status_msg = null;
					break;
				case 'roster':
					if(!this.rooms[msg.room]) {
						//this.rooms[msg.room] = {name: msg.room, occupants: msg.occupants, messages: []};
						this.$set(this.rooms, msg.room, {name: msg.room, occupants: msg.occupants, messages: []});
					} else {
						this.rooms[msg.room].occupants = msg.occupants;
					}

					if(!this.current_room) {
						this.current_room = msg.room;

						this.handleMessage({
							type: 'system',
							body: 'Connected to server!',
						});
					}
					break;
				case 'join':
					this.rooms[msg.room].occupants.push(msg.from);
					this.pushMessage(msg.room, msg);
					break;
				case 'leave':
					this.rooms[msg.room].occupants = this.rooms[msg.room].occupants.filter(o => o != msg.from);
					this.pushMessage(msg.room, msg);
					break;
				case 'chat':
					if(msg.img) {
						msg.img_src = this.imageFromData(msg.img);
					}
				case 'error':
				case 'system':
					msg.body = (new Parser(msg.body)).parse();
					this.pushMessage(msg.room, msg);
					break;
			}
		},
		pushMessage: function(room, msg) {
			if(this.rooms[room]) {
				this.rooms[room].messages.push(msg);

				while(this.rooms[room].messages.length > MAX_MESSAGES) {
					this.rooms[room].messages.shift();
				}
			}
		},
		autoscroll: function() {
			try {
				let mbx = document.getElementById('message-box');
				if(mbx.scrollHeight - mbx.scrollTop - mbx.offsetHeight <= 50) {
					this.$nextTick(() => {
						document.querySelector('#message-box > div:last-child').scrollIntoView();
					});
				}
			} catch(error) {
			}
		},
		reconnect: function() {
			this.retry_count += 1;
			this.retry_time = 15 * this.retry_count;

			let timer = setInterval(() => {
				this.retry_time -= 1;

				if(this.retry_time <= 0) {
					clearInterval(timer);
					this.connect();
				}
			}, 1000);
		},
		sendChat: function() {
			const json = this.chat_json;
			this.chatbox = '';
			this.chatimg = null;

			console.log('Sending:', json);
			this.socket.send(json);
		},
		newId: () => Date.now().toString(36) + '+' + Math.random().toString(36).split('.').pop(),
		imageFromData: function(data) {
			if(data) {
				return "data:image/"+data.type+";base64,"+data.data;
			}

			return null;
		},
		dragImage: function(evt) {
			const types = ['image/png', 'image/jpeg', 'image/gif'];
			const item = evt.dataTransfer.items[0];

			types.forEach(type => {
				if(item.type == type) {
					this.dragging = true;
					evt.preventDefault();
				};
			});
		},
		dropImage: function(evt) {
			if(this.dragging) {
				evt.preventDefault();
				this.dragging = false;
				this.chatimg = null;

				const file = evt.dataTransfer.items[0].getAsFile();

				if(file.size > this.img_maxsize) {
					//TODO: Alert the user to the file being too big
					return;
				}

				console.log(evt.dataTransfer.items[0]);

				let reader = new FileReader();
				reader.addEventListener('load', () => {
					const [meta, data] = reader.result.split(',');
					const type = meta.match('^data:image/([a-z]+);')[1];

					this.chatimg = {type:type, data:data};
				});
				reader.readAsDataURL(evt.dataTransfer.items[0].getAsFile());
			}
		},
		onblur: function(evt) {
			//FIXME: This room is hard-coded for the Lobby room only
			console.log('blurring');
			let messages = this.rooms['Lobby'].messages.filter(msg => msg.type != 'unread');
			this.rooms['Lobby'].messages = messages;
			this.pushMessage('Lobby', {'type':'unread'});
		},
	},
});
