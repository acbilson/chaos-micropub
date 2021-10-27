+++
aliases = ["/posts/ethical-hacker-resources/session-hijacking/"]
backlinks = [
    "/posts/resources/ethical-hacker-resources"
]
category = "technology"
comments = true
date = "2020-06-03"
description = "In which Alex notates what he's learned about session hijacking as an ethical hacker."
displayInList = false
dropcap = false
tags = ["security", "session-hijacking"]
title = "Ethical Hacker / Session Hijacking"
toc = true
+++
{{< muted >}}
These are notes under the umbrella post titled: {{< backref src="/posts/resources/ethical-hacker-resources" >}}. Check there for a master list of notes taken for the Ethical Hacker certification.
{{< /muted >}}

# Definition

Session hijacking occurs when a hacker acquires session information from a network user the hacker can use to impersonate the user, halt the user's activity, or steal the user's information.

# Types of Session Hijacking

Session hijacking can happen at the application, such as a web application.

- Session ID sniffing
- Session fixation
- Session donation
- Session ID brute force

Or at the network, such as a TCP hijack.

- Blind hijacking
- Session sniffing
- IP spoofing
- UDP hijacking

# HTTP and State Management

HTTP is by definition stateless. This means that standard requests do not send any identifying information about the user. This has led to several means to identify a user and their current session.

**Token management:** grants a unique value called a token to a user's request. The user then sends that token with following requests to associate each request with that user. An example I've used is [Identity Server]("https://identityserver.io/").

**Cookies:** are stored by the browser and shared with each request. Cookies can be valuable to manage user's identity because they 1) persist in the browser, so they'll work across tabs, 2) don't require every request to manage tokens.

**URL persistence:** sends user identity via the URL request itself. This allows each tab in a browser to possess a unique identity.

## Session Fixation

If a hacker can supply a user an identity, such as passing them a link with the session ID set in the URL, and the user logs in, the specified session ID may be allocated to that user by the system. Because the hacker has the session ID, the hacker will also be identified as that user by following the same link.
