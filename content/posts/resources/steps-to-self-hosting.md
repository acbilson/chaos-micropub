+++
aliases = ["/posts/steps-to-self-hosting/"]
backlinks = [
  "/notes/craft-your-own-site",
  "/posts/insights/hosted-webhooks"
]
category = "technology"
comments = true
date = "2020-05-13"
description = "In which Alex aggregates instructions to entirely host one's own website."
dropCap = false
tags = ["hosting", "server"]
title = "Steps to Self Hosting"
toc = true
[featuredImage]
  alt = "Graham on a Block Cycle"
  large = "https://uwroja.by.files.1drv.com/y4mOfiFdz2sYcWeBbnlwv5Edazg8EUrV36VtacrZTHNo3wIwG0m3oaYnbK0-ySkYaMaGaP5EP9vgFT0eBRXhCF5w8fQcMEr3l39vBknGXazWEVYr1TD-HFdCz67uivJjh68Os3WIS9iz0YK3Vl4tHiJYvatWT3wM9EE0CTLkkUXvXMcKhemyXZCwirQgLnuRP6J_iPRxjQMeWvz9b4KEqZhDg?width=768&height=1024&cropmode=none"
  small = "https://uwroja.by.files.1drv.com/y4mOfiFdz2sYcWeBbnlwv5Edazg8EUrV36VtacrZTHNo3wIwG0m3oaYnbK0-ySkYaMaGaP5EP9vgFT0eBRXhCF5w8fQcMEr3l39vBknGXazWEVYr1TD-HFdCz67uivJjh68Os3WIS9iz0YK3Vl4tHiJYvatWT3wM9EE0CTLkkUXvXMcKhemyXZCwirQgLnuRP6J_iPRxjQMeWvz9b4KEqZhDg?width=192&height=256&cropmode=none"
+++

# Introduction

At a time where digital resource management is being aggregated into a few global storehouses, what does it take to run your website from scratch? Turns out, it's simpler than I thought. Here's what it took to serve this website from my home office.

# Purchase and Configure a Physical Server

My first website in 2014 was hosted by a third-party provider. I managed the site through a web interface and left the server management to the provider. After the ease of a hosted service, the thought of running my server was daunting. Then I heard about the Raspberry Pi.

A {{< acronym DIY "Do It Yourself" >}} Raspberry Pi 4 package cost me ~$100 on Amazon.com. Armed only with the instructions in the package and the invaluable tutorials on the [official website](https://projects.raspberrypi.org/en/), I had the machine running in an evening. How cool is that!

![Raspberry Pi](https://he0fgq.by.files.1drv.com/y4mWwRLP3c_WnEqlokOOJS2VF2ubhAmXJawy2m3ivvQ73O7ztDlTGsPDm8ljA-Saf-4cAbLbviEpoSxUkFYqdUu8tnP9sYMFuPfo1a0e_nYqPxff9wKkfOdi_RQ8_GmpT86iSJILffTWNdDsoWP-2WM8YZ2pVRqtV1qEPu5VnUbgASh1pOMZ3Zi5P2I5VNTvsYytRwOMUbKsqAdVaDz5UbOGg?width=1024&height=768&cropmode=none)

## Server OS

A physical server isn't worth much without an operating system. Fortunately, the Raspberry Pi has several suitable OSes to choose from. The Rasberry Pi package I purchased on Amazon.com came with an OS installer called NOOBS on the SD card.

While I did use NOOBS to get started, I suggest you skip the extra cruft the NOOBS installer adds and image the SD card directly. I used [Etcher](https://www.balena.io/etcher/#download) to image the Raspbian OS onto my SD card.

Note: my Amazon.com package also came with a handy SD Card adapter so I could plug my SD card directly into a USB port. If you can't access your SD card from your computer, follow the official [setup instructions](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up) before you continue.

> before you pull the SD card from your computer, be sure to add an empty file titled 'ssh' to the card. You don't need to put it in any folder. This will enable SSH from square one, which allows you to interact with your new server without plugging in a mouse or keyboard.

## Server Accessibility

A server is hardly worth the name unless it's part of a network. Before we make our website available to the world wide web ({{< acronym WAN "Wide Area Network" >}}), let's get it running on our local network ({{< acronym LAN "Local Area Network" >}}).

I added the server to my LAN by plugging the Raspberry Pi directly into an available ethernet port on my wireless router. The router assigns an IP address to the Raspberry Pi. To retrieve the IP address, log into your router and look for the attached Raspberry Pi under its attached devices. Every router provider is different, but you can figure it out.

> Save yourself some trouble and permanently assign this IP address to your Raspberry Pi. This is called address reservation and was under LAN setup on my router. If you don't, your router may assign the IP address to another device the next time it's allocating addresses.

Now let's make our first connection to our server! Make sure it's turned on &#x1F609;.

Open up a terminal instance on your computer. We'll use [OpenSSH](https://www.openssh.com/) to access the Raspberry Pi. Most computers have this software pre-installed, or you may install it now. Type the following command; changing the IP address to the address your router assigned.


{{< highlight sh >}}
ssh pi@192.168.1.3
{{< / highlight >}}

You're in!

## Server Access Security

It would be a shame to run your website only to have it hacked. Or worse. Follow the official [security guidelines](https://www.raspberrypi.org/documentation/configuration/security) to harden {{< acronym SSH "Secure SHell" >}} access.

I recommend you do not proceed until you have configured SSH access to accept only key-based authentication and set a lengthy private key passphrase. Your server, the one on your home network, will be accessible from anywhere in the world; think about it. If you're not familiar with SSH keys, check out the manual [here](https://www.ssh.com/ssh/keygen).

> If you're following my steps, you may not require a firewall installation. A firewall isn't necessary for closed ports and we'll open only what we need.

# Install Server Software

Now we've got a working distribution of Debian Linux on our own Raspberry Pi physical server. What geeks we are!

The possible options at this stage are endless, so I will focus on a single, opinionated path for the software that will 'serve' our website. I chose Nginx because it's simple to configure, but you could use Apache or any other Debian-compatible server software.

First, let's install the server software. Log back into your Raspberry Pi (remember your passphrase?) and run the following commands.

{{< highlight sh >}}
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install nginx -y
{{< / highlight >}}

> The first line updates your package registry and upgrades all the installed software packages. You should run this command periodically to keep your server up-to-date with security patches. The second line installs our software, [Nginx](https://www.nginx.com/).

We don't have a website yet, but Nginx comes with a default landing page. Start the server with:

{{< highlight sh >}}
sudo /etc/init.d/nginx start
{{< / highlight >}}

> This command launches the Nginx background process on your Raspberry Pi. You can also run similar commands to restart and stop the service.

Finally, navigate to the host address from your computer's browser (e.g. `http://192.168.1.2` - change to your Raspberry Pi's IP address). You should see a default landing page. This is where your site will display, but first, we have to create it!

## Build Your Website

There are thousands of tutorials for building a website, and I won't replicate them. I wanted a website with almost no moving parts to preserve security and enable me to focus on content instead of configuration. A static web generator was a perfect match for my needs. Why not try [Hugo](https://gohugo.io/getting-started/quick-start/)?

From this point, I'll assume we'll run a static website, but many of these steps apply to more complex configurations.

## Server Software Configuration

Nginx comes with sensible defaults, but you'll want to make some modifications to host your static site. The smart people at Nginx have already published a helpful article about [hosting static content](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/) and supply useful [configuration examples](https://www.nginx.com/resources/wiki/start/topics/examples/full/).

> Unless you're already familiar with Debian Linux, Hugo web development and Nginx, at this point you're probably drowning in information. Remember, you haven't exposed anything to the world yet! Rather than get bogged down in detail here, keep moving with defaults and get it working.

# Go Public!

You've got a working website served on your LAN, now it's time to go public!

> Don't proceed unless you're comfortable with your current security posture. If you're not certain, stop now and review the security documentation for your selected server software, for website dependencies (if any), for Debian Linux, and the Raspberry Pi.

![Olympic Globe, Colorado Springs, CO](https://0urnmg.by.files.1drv.com/y4mYEu2FL8HQ-ifSSpD_d6XiCqTvYmdHD4GNbRG5Gz9Z1ArzZlxemU1X-bqBnnHzc-uZuZvfuR-orEYfAN2iRu9zHac0NAMlMcWcQ3BAqjwW-kn_5IwR-mWCC8O8a05TCUlaiohSQlx84tGFywgCC_wJ-UV9sN-jUlHBob0oedjypvNaaISoHtiMePGFDIEYjnXccxgfo-ZmDx8xzZfvYvDWg?width=768&height=1024&cropmode=none)

## Forward Requests

Your router is the doorway to public access with machines on your LAN. By default it offers no external access, so we'll need to configure it to forward requests to our home server. To achieve this, add a port forwarding rule to send requests to your router to your Raspberry Pi's IP address. It may be under an advanced configuration section. Until we configure HTTPS, we'll use port 80.

To confirm that requests are being forwarded, you'll need your router's public IP address. It may be listed in on your router's config page, or you can use https://www.whatismyip.com/. Navigate to your router's address and you should see your website! (e.g. `http://200.124.45.23` - change to your public IP address)

## Purchase A Domain Name

At this point, you _could_ send your router's public IP address to a friend on the opposite side of the world and she could view your website. But who is going to remember a numeric address? And what happens if your {{< acronym ISP "Internet Service Provider">}} changes your public address? Let's buy a domain name.

Choose a domain name to fit the content of your website. There are several domain name registrars, and all of them have suggestions for selecting a website domain name and a search bar to check that name's availability. At the time of writing, a dotcom address costs about $10/year.

Follow the registrar's instructions to configure an A Record that points to your router's public IP address. You may have to wait for a bit, but in time you can enter your new domain name (e.g. http://thisismycoolsite.com/) and get back the website hosted from your home office!

> If you're familiar with DNS records, you'll notice that for the rest of this post I'll presume you have configured a bare domain name (i.e. no prepended www dot). This is for simplicity; tweak my examples to suit your site's DNS configuration.

Technically, if your ISP assigns a new IP address to your router, your hostname won't resolve until you've updated the A Record to the new IP address. The AAAA Record allows server software, such as ddclient, to dynamically update the record address. Dynamic configuration not required to continue, and some ISPs recycle addresses so infrequently that manual updates aren't arduous.

## Configure HTTPS

You've probably noticed that security is a theme. Your site may not require in-transit encryption today, but why wait until it does? Let's configure your site for {{< acronym HTTPS "Hyper-Text Transfer Protocol, Secure" >}}.

> These notes include more manual steps than you may require. Between ISP restrictions and a lack of registrar support, I had to perform the certificate configuration manually. We'll be using [Let's Encrypt](https://letsencrypt.org/) as our certificate authority.

First, we need to install certbot on our Raspberry Pi. Log in and run the following command:

{{< highlight sh >}}
sudo apt-get install certbot python-certbot-nginx -y
{{< / highlight >}}

> This installs the certbot software that we'll use to register a certificate and helper software to update our Nginx configuration.

The helper software didn't update my Nginx configuration properly. If this happens to you, see the Nginx docs for [configuring HTTPS servers](https://nginx.org/en/docs/http/configuring_https_servers.html).

Then we'll run the following command:

{{< highlight sh >}}
sudo certbot certonly --manual --preferred-challenges dns -d thisismycoolsite.com
{{< / highlight >}}

Follow the prompts. When you get to a question about adding a DNS TXT record, add a TXT record in your registrar's interface with the key certbot displays in your terminal. It might look like this:

{{< raw >}}
&emsp;Type: TXT Record<br />
&emsp;Host: acme-challenge<br />
&emsp;Value: { enter key here }<br />
&emsp;<acronym title="Time To Live">TTL</acronym>: Automatic
{{< / raw >}}

> Some registrars require that you append your domain name to the host value. Follow your registrar's instructions for TXT records.

Finally, you'll need to add a new port forwarding record to your router. HTTPS is port 443.

> To limit your site's attack surface, when you can successfully navigate to your website with HTTPS (e.g. https://thisismycoolsite.com/), remove the port forwarding rule for port 80. All traffic can and should travel over HTTPS port 443.

# Finalé

If you made it this far, congratulations! When I said it was simple, I meant that you won't need in-depth knowledge of every technology, not that you won't need to know something about _many_ technologies.

With the instructions I've laid out, you should have:

1. A static website served by a decently secure web server running on a Raspberry Pi.
2. A router configured to forward HTTPS requests to your web server.
3. A domain name that resolves to your router's public IP address.

> I didn't supply instructions to enable remote SSH. It would only take another port forwarding rule, but do you need to access the server outside of your LAN?

Thanks for reading!
