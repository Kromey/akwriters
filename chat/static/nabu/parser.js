const SIMPLE_RULES = [
	{token: '*', pattern: '\\*', tag: 'strong'},
	{token: '_', tag: 'em'},
	{token: '~', tag: 's'},
];

const MATCH = (() => {
	let patterns = [];
	SIMPLE_RULES.forEach(rule => patterns.push(rule.pattern || rule.token));

	patterns = patterns.join('|');

	return new RegExp('(' + patterns + ')');
})();

function Parser(text) {
	this.text = text;
}

Parser.prototype.parse = function() {
	sanitized = this.sanitize();
	return this.format(sanitized);
}

Parser.prototype.sanitize = function() {
	// Create a DOM node, then append the text to be sanitized as a
	// Text node. In order for the browser to render it as a Text node,
	// it has to have all HTML entities escaped; we can then access the
	// escaped string as the innerHTML attribute of the node.
	return document
		.createElement('div')
		.appendChild(document.createTextNode(this.text))
		.parentNode // appendChild returns the appended node, so go back "up"
		.innerHTML;
}

Parser.prototype.format = function(text) {
	if(!text.trim()) {
		return text;
	}

	console.log('Formatting', text);
	const m = text.match(MATCH);

	if(m === null) {
		return text;
	}

	let pre = text.slice(0, m.index);
	let post = text.slice(m.index + 1);

	if(pre.match(/[\\a-zA-Z0-9]$/)) {
		console.log('Preceded by "word" or escape character:', pre.slice(-1));
		if(pre.match(/\\$/)) {
			pre = pre.slice(0, -1);
		}
		return pre + m[0] + this.format(post);
	}

	const idx2 = this.find_matching_token(post, m[0]);

	if(idx2 == -1) {
		console.log('Unmatched, now parsing', post);
		return pre + m[0] + this.format(post);
	}

	let content = post.slice(0, idx2);
	post = post.slice(idx2 + 1);

	const tag = (SIMPLE_RULES.find(rule => rule.token == m[0])).tag;

	console.log('Matched', m[0]);
	console.log(idx2, content, post);
	return pre + '<' + tag + '>' + this.format(content) + '</' + tag + '>' + this.format(post);
}

Parser.prototype.find_matching_token = function(text, token, offset) {
	if(!offset) {
		offset = 0;
	}

	let i = text.indexOf(token, offset);
	console.log('Potential match of', token, 'in', text, 'at', i);

	if(i == -1) {
		return -1;
	}

	if(text[i-1] == '\\' || (text[i+1] && text[i+1].match(/\w/))) {
		return find_matching_token(text, token, i+1);
	}

	return i;
}
