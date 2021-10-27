+++
category = "technology"
comments = true
date = "2021-03-19"
description = "In which Alex shares his analytical family's favorite online baby resources."
draft = true
tags = ["podman", "container", "networking", "ufw"]
title = "To Access A Podman Container from the Public Network"
[featuredImage]
  alt = ""
  large = ""
  small = ""
+++
From what I've gathered, these are the steps one must go through to allow a Podman container, such as a traefik proxy, to be accessible from the public network.

The challenge lies with the network interface. Podman creates its own cni virtual network interface, but it's the host's default network interface that's usually configured for intranet access. My ufw firewall blocks cross-interface traffic by default, with iptables in the backend to control access.

> to find out what network interfaces are on your host, run:

{{<highlight sh >}}
ip addr show
{{< / highlight >}}

I don't know much about network interfaces, but part of what they seem to allow is the capacity to have two different ip address ranges on the same machine. For example, my ip address is in the 102.122.\*.\* range on my physical network interface, but my podman containers run on the 10.88.\*.\* range on my virtual network interface.

So, what steps should I take to grant my container access to the public network?

Why don't we start with the obvious. If I want outside access to port 9999 from the public network, I need to allow traffic through my firewall.

{{<highlight sh >}}
ufw allow 9999/tcp
{{< / highlight >}}

Second, I must allow ufw to forward requests to other ip addresses. Funny, I actually want it to forward to other network interfaces, but I guess it's the same thing?

To achieve this, uncomment the applicable lines in /etc/ufw/sysctl.conf. For IPv4 forwarding, this line is:

```
net/ipv4/ip_forward=1
```

Finally, I'll need to allow requests to enter my physical network interface and exit my virtual interface.

{{<highlight sh >}}
sudo ufw route allow in on eth12 out on cni-podman9
{{< / highlight >}}

With these three steps I've granted public network access to all of my network interfaces through the open ports and allowed my virtual network interface to respond to forwarded requests. I could be yet more restrictive by only allowing traffic from port 3000 through to my virtual network interface. The manual is excellent reading - I'll let you find out how to do that ;)

{{<highlight sh >}}
man ufw
{{< / highlight >}}
