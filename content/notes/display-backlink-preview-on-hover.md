+++
backlinks = [
    "/notes/craft-your-own-site",
    "/notes/read-webpage-as-api"
]
author = "Alex Bilson"
comments = false
date = "2021-06-11T20:43:55"
epistemic = "plant"
tags = ["snippet","javascript","software","backlink","microformat","indieweb"]
title = "Display Backlink Preview on Hover"
+++
The combination of microformat2 [h-entry](http://microformats.org/wiki/h-entry) and backlinks is potent. Each note page that's marked up with a `e-content` microformat2 property can be retrieved via `fetch()` and displayed as a preview elsewhere on the site. No database required; the website _is_ the API. With these two snippets you can implement dynamic backlink functionality on pretty much any webpage. With a little standardization (mostly complete by the microformat2 standard), one could support backlinks _across_ websites. Woah!

First, here's a snippet to retrieve a popup of an internal link's comment. For each link marked with `class="internal"`, the first three elements or less will be retrieved from its `e-content` div element.

{{< highlight js >}}

function parsePageContent(text) {
  var bodyDOM = new DOMParser().parseFromString(text, 'text/html');
  const contentElement = bodyDOM.querySelector('div.e-content');

  if (contentElement) {
    const elementCount = contentElement.childElementCount < 3 ? contentElement.childElementCount : 3;
    const contentSlice = Array.from(contentElement.children).slice(0, elementCount);

    if (elementCount < contentElement.childElementCount) {
      const ellipsisElement = document.createElement('p');
      ellipsisElement.innerText = '...';
      contentSlice.push(ellipsisElement);
    }
    return contentSlice;

  } else {
    const missing = document.createElement('p');
    missing.text = 'no content found';
    return [missing];
  }
}

function createPopup(offsetTop, offsetLeft, contentElements) {
  const popup = document.createElement('div');

  popup.classList.add('backlink-popup', 'hide');
  popup.style.top = `${offsetTop + 20}px`;
  popup.style.left = `${offsetLeft}px`;
  contentElements.forEach((el) => popup.appendChild(el));

  return popup;
}

function appendLinkPopup(link) {
  fetch(link.href)
    .then((resp) => {
      if (resp.status === 200) {
        return resp.text();
      } else {
        return null;
      }
    })
    .then((text) => {
      if (text === null) { return null; }
      const contentElements = parsePageContent(text);
      const popupElement = createPopup(link.offsetTop, link.offsetLeft, contentElements);
      link.appendChild(popupElement);
    });
}

// adds backlink popup as a hidden child element to all links marked internal
const internalLinks = document.querySelectorAll('a.internal');

internalLinks.forEach((link) => {
  appendLinkPopup(link);
});

{{< / highlight >}}

Second, here's a snippet to populate the context of a backlink. For each link marked with `class="backlink"`, the parent context of the link on the backlinked page will be appended to the link's parent element.

{{< highlight js >}}

function parsePageContext(text) {
  var bodyDOM = new DOMParser().parseFromString(text, 'text/html');
  var urlParts = document.URL.split('/');
  var backlinkName = urlParts[urlParts.length - 2];
  var backlinkElement = bodyDOM.getElementsByName(backlinkName)[0];
  return backlinkElement.parentElement;
}

function appendSourceContent(link) {
  fetch(link.href)
    .then((resp) => {
      if (resp.status === 200) {
        return resp.text();
      } else {
        return null;
      }
    })
    .then((text) => {
      if (text === null) { return null; }
      const contextElement = parsePageContext(text);
      const wrapper = document.createElement('p');
      wrapper.appendChild(contextElement);
      link.parentElement.appendChild(wrapper);
    });
}

// retrieves content from all backlinks that reference this page
const sourceLinks = document.querySelectorAll('a.backlink');

sourceLinks.forEach((link) => {
  appendSourceContent(link);
});
{{< / highlight >}}
