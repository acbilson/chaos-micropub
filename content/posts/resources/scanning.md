+++
aliases = ["/posts/ethical-hacker-resources/scanning/"]
backlinks = [
  "/posts/resources/ethical-hacker-resources"
]
category = "technology"
comments = true
date = "2020-06-03"
description = "In which Alex notates what he's learned about scanning as an ethical hacker."
displayInList = false
dropcap = false
tags = ["security", "scanning"]
title = "Ethical Hacker / Scanning"
toc = true
+++
{{< muted >}}
These are notes under the umbrella post titled: {{< backref src="/posts/resources/ethical-hacker-resources" >}}. Check there for a master list of notes taken for the Ethical Hacker certification.
{{< /muted >}}

# Definition

Scanning is the second step a hacker takes to hacking a system. To read about the first, check out {{< backref src="/posts/resources/reconnaissance" >}}.

Hackers scan to build out a more complete picture than recon, and especially to add information about the current status of the network and not only its infrastructure. This may be open ports, the running services, and which machines are online. The line between recon and scanning can be blurred, but I think recon tends towards passive data retrieval while scanning is active.

# Types of Scanning

**Network scan:** sends requests to each machine on the network and investigates the responses. This can give a wealth of information about firewalls, OSes, ports, and more. This scan is noisy because, while it is possible for a hacker to individually poll a network, software automation will rapidly bombard the network.

**Port scan:** sends requests to every port on a machine. With 65,535 ports per machine, most scans will focus on a subrange such as the first 1023 because these are standard ports. For example, port 22 is used for SSH, port 53 for DNS, port 443 for SSL. This can also be noisy unless the hacker picks a small range and spaces out their scans.

# Manipulating the 3-way Handshake

Computers communicate over a network via two primary protocols, {{< acronym TCP "Transmission Control Protocol" >}} and{{< acronym UDP. "User Datagram Protocol" >}} TCP performs a three-step verification process called the 3-way handshake to ensure a connection has been made and that data was received. A hacker can manipulate TCP flags to trick a computer into divulging information.

The TCP handshake operates like this:

{{< raw >}}
<svg width="100%" height="90px">
  <text x="15"  y="50" fill="blue"> Bob's Machine</text>
  <text x="410" y="50" fill="green">Jill's Machine</text>
  <text x="140" y="20" fill="red">  SYN (#403)</text>
  <text x="140" y="50" fill="red">  SYN/ACK (#404/#356)</text>
  <text x="140" y="80" fill="red">  ACK (#357)</text>
  <!-- first red arrow -->
  <line x1="350" y1="15" x2="400" y2="15" style="stroke:red;stroke-width:2"></line>
  <line x1="390" y1="8" x2="399" y2="15" style="stroke:red;stroke-width:2"></line>
  <line x1="390" y1="23" x2="399" y2="15" style="stroke:red;stroke-width:2"></line>
  <!-- second red arrow -->
  <line x1="350" y1="45" x2="400" y2="45" style="stroke:red;stroke-width:2"></line>
  <line x1="360" y1="37" x2="351" y2="45" style="stroke:red;stroke-width:2"></line>
  <line x1="360" y1="53" x2="351" y2="45" style="stroke:red;stroke-width:2"></line>
  <!-- third red arrow -->
  <line x1="350" y1="75" x2="400" y2="75" style="stroke:red;stroke-width:2"></line>
  <line x1="390" y1="67" x2="399" y2="75" style="stroke:red;stroke-width:2"></line>
  <line x1="390" y1="83" x2="399" y2="75" style="stroke:red;stroke-width:2"></line>
</svg>
{{< / raw >}}

1. Bob's computer sends a TCP packet with a {{< acronym SYN "Sync, pronounced 'sin'" >}} flag with a sequence number (#403).
2. Jill's computer receives Bob's TCP packet and responds with two flags: a SYN and an {{< acronym ACK. "Acknowlege" >}} The SYN flag passes Bob's sequence number, incremented by one (#404) and the ACK flag sends Bob's sequence number (#356).
3. Bob's computer receives Jill's TCP response and responds with an ACK flag with Bob's incremented sequence number (#357).

Hackers can manipulate this process by sending a flag that's not expected. For example, Bob's computer could begin with a SYN/ACK.

# Banner Grabbing

# Scanning Software

The top scanning software every ethical hacker should be familiar with are: nmap, Angry IP Scanner, and Nessus.  I've also included a plug for hping3 because it's demoed on the PluralSight course, and for [Fing's](https://www.fing.com/products/fing-app) iOS app which was suggested on PluralSight and I've begun to use at home.

## nmap

The nmap command line utility enumerates over a target IP range to gather comprehensive information about status, ports, and more. It also has a GUI called zenmap.

`> nmap --top-ports 10 192.168.1.1-50`

Scans the IP address range for active machines and checks the status of the top ten most common ports on each machine. Here's a table-formatted example of the output for one machine:

{{< raw >}}
<table>
<tr><th>PORT</th><th>STATE</th><th>SERVICE</th></tr>
<tr><td>21/tcp </td><td>closed</td><td>ftp</td></tr>
<tr><td>22/tcp </td><td>closed</td><td>ssh</td></tr>
<tr><td>23/tcp </td><td>closed</td><td>telnet</td></tr>
<tr><td>80/tcp </td><td>open  </td><td>http</td></tr>
<tr><td>110/tcp</td><td>closed</td><td>pop3</td></tr>
<tr><td>139/tcp</td><td>closed</td><td>netbios-ssn</td></tr>
<tr><td>443/tcp</td><td>closed</td><td>https</td></tr>
<tr><td>445/tcp</td><td>closed</td><td>microsoft-ds</td></tr>
<tr><td>3389/tcp</td><td>closed</td><td>ms-wbt-server</td></tr>
</table>
{{< / raw >}}

## hping3

The hping3 command line utility expands typical ping functionality.

`> hping3 -l 192.168.1.x --rand-dest -I eth0`

Sends an ICMP requests to hosts in the specified IP address range from the eth0 {{< acronym NIC. "Network Interface Card" >}}

## Fing

[Fing](https://www.fing.com/products/fing-app) is a company that, among other things, supplies a nifty iOS/Android app to run various network diagnostics. For the ethical hacker, it's a pocket tool to troubleshoot your local network or detect intruders.
