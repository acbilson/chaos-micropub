+++
aliases = ["/posts/ethical-hacker-resources/reconnaissance/"]
backlinks = [
  "/posts/resources/ethical-hacker-resources"
]
category = "technology"
comments = true
date = "2020-06-03"
description = "In which Alex notates what he's learned about reconnaissance as an ethical hacker."
displayInList = false
dropcap = false
toc = true
tags = ["security", "reconnaissance"]
title = "Ethical Hacker / Reconnaissance"
+++
{{< muted >}}
These are notes under the umbrella post titled: {{< backref src="/posts/resources/ethical-hacker-resources" >}}. Check there for a master list of notes taken for the Ethical Hacker certification.
{{< /muted >}}

# Definition

Reconnaissance (Recon), also referred to as footprinting, is the first step a hacker takes in their path to hacking your system. A hacker may spent up to 90% of their time on this step, passively gathering intelligence that will aid them in a future hack.

# Reasons to Recon

The parts of hacking made glamorous in movies centers on the "attack." But hackers spend the preponderance of their time
on recon. Why?

- Hackers seek the simplest access points. If a hacker can find the weakest link a network, he'll save hours of work trying to breach more secure areas.
- Hackers reduce their attack surface. A hacker's purpose often doesn't require access to every machine in a network. If he can narrow down the targets to a short list, he'll save time and protect his anonymity by focusing his efforts on
  the right machines.
- Hackers sell network information. Similar to other forms of commercialized data, hackers can generate an income from the network information they've gathered on dark websites.

# Types of Recon

There are essentially two types of recon: active and passive.

Passive recon accesses publicly-available content and is indisinguishable from a normal user's activity. It's where hackers begin because it raises no alarms. Though it's silent, it doesn't mean that it is always anonymous. For example, accessing employee's LinkedIn information does leave a trace. But it's not suspicious.

Active recon moves towards activity which might raise an alarm. It may use the same avenue as passive recon, but the activity could look suspicious. For example, if a single user enumerated over a company's entire organization in LinkedIn within five minutes, this might raise suspicion.

# What Hackers Look For

Anything has potential value for a hacker. Machine information gives them data to map the network. Employee information gives them fodder for social engineering.

# Tools

## Search Engines
Google has sophisticated search options a hacker can use to pull up exposed files. Some are particularly helful:

- **site:** limits query to the target site.
- **cache:** returns cached versions of the site.
- **links:** sites that contain hyperlinks to the target site.
- **intitle:** cached files with this title.
- **inurl:** cached files that have this string in the url.

`[google] intitle:"index of"`

Pulls up sites that have exposed directories.

`[google] site:hackthissite.org inurl:.xlsx`

Finds all public Excel files on hackthissite.org.

## Job Sites
HR managers post detailed information about job requirements on public job sites every day. A hacker gleans OS, software, versions, and more from these posts and can perform sophisticated queries to find vulnerable software, such as server versions which no longer receive support.

## Archival Websites
The Wayback Machine stores snapshots of websites. Sometimes sensitive data was present on a site before the administrator learned better security practices. A hacker can retrieve this sensitive information after the site has been fixed by retrieving its snapshot.

## Network Diagram Software
Network software builds a comprehensive map, complete with detailed notes, of a target network that a hacker can easily return to at any step in his hack.

## Site Download Software
Download software enumerates over every possible path at a specified domain. This process can reveal pages and files which have been unwittingly exposed by the administrator. Some can specify particular file types, such as Excel files. WinHTTrack is an example of such software.

## SaaS Tools
[Whois](https://whois.domaintools.com/) gives domain ownership information and much more.

[Netcraft](https://www.netcraft.com/) identified the server tech I'm using, scary.

[Exploit Db](https://www.exploit-db.com/) lists software vulnerabilities and is super comprehensive.

## Command Line Tools
### Ping
Ping has numerous flags which a hacker can use to determine accepted packet size. For example, a hacker can attempt different packet sizes with this snippet, where -f turns off packet fragmentation (it'll be sent as one packet, not many) and -l specifies the packet size in bytes.

{{< highlight sh >}}
ping hackthissite.org -f -l 1500
{{< / highlight >}}

### NSLookup
Nslookup can retrieve sets of related servers at a domain, including the DNS servers. A domain may have mail servers, backup servers, even print servers available on the public web. To list all mail servers at a public domain:


{{< highlight sh >}}
nslookup
set type=mx
hackthissite.org
{{< / highlight >}}

Or to identify the authoritative name server:

{{< highlight sh >}}
> nslookup
> set type=cname
> hackthissite.org
{{< / highlight >}}

When the authoritative name server has been identified, a hacker may glean more information by querying that server directly.

{{< highlight sh >}}
> nslookup
> set server=198.148.81.188
> set type=any
> hackthissite.org
{{< / highlight >}}

Change the final line to `ls -d hackthissite` to attempt a zone transfer.
