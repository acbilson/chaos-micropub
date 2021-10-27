+++
backlinks = [
    "/notes/craft-your-own-site"
]
date = "2020-10-02T14:45:33"
epistemic = "plant"
tags = ["writing","javascript"]
title = "Read Webpage As API"
+++
One of the Indieweb mindsets is to treat HTML content as its own API.

This oneline snippet uses the Mozilla's Fetch API to read the content from one of my notes and display it in the developer console. Copy it into your developer console and see the content of the note appear in the console.

{{< highlight js >}}
fetch('/notes/aversions-to-the-word-evangelism').then((response) => response.text()).then((text) => { var mydom = new DOMParser().parseFromString(text, 'text/html'); var el = mydom.querySelector('div.e-content'); console.log(el.innerHTML.trim()); });
{{< / highlight >}}

I've used the same philosophy to {{< backref src="/notes/display-backlink-preview-on-hover" >}}
