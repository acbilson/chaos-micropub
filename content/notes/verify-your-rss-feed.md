+++
backlinks = [
    "/notes/craft-your-own-site"
]
author = "Alex Bilson"
comments = false
date = "2021-07-27T17:04:15"
lastmod = "2021-07-27 14:18:12"
epistemic = "sprout"
tags = ["rss","javascript","snippet"]
title = "Verify Your RSS Feed"
+++
If you have an RSS feed, you can use this snippet as a starting place to review the output. I'm printing the titles of each RSS item to the console, but go as deep as necessary to ensure the right information ends up in your feed.

{{< highlight js >}}
fetch('https://my-url-here.com')
.then(res => res.text())
.then(text => {
	const domParser = new DOMParser();
	const doc = domParser.parseFromString(text, 'text/html');
	var feedURL = doc.querySelector('link[type="application/rss+xml"]');
	return fetch(feedURL.href);
})
.then(resp => resp.text())
.then(text => {
	const domParser = new DOMParser();
	const doc = domParser.parseFromString(text, 'text/xml');
	const items = doc.querySelectorAll('item');
	return Array.from(items).map(item => item.querySelector('title').textContent);
}).then(titles => console.log(titles));
{{< /highlight >}}

