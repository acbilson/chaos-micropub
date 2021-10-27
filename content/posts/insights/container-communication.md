+++
aliases = ["/posts/container-communication/"]
category = "technology"
comments = true
date = "2020-07-22"
description = "In which Alex demonstrates a third way to manage multi-docker workflows."
dropCap = false
tags = ["docker","ssh","jenkins","architecture"]
title = "Controller/Client Docker Connection"
toc = true
[featuredImage]
  alt = "Graham with flamingoes"
  large = "https://iskkpa.by.files.1drv.com/y4mkdmObmsu_UM2mLGV3_ae4616KwLRPGCHkC6EN98CEkroqnjsHTsEB3pZ3vpp9D5dOv_v8Pqd4HTqu30VrzAvMQpPpPNU2DlIQo1GLRIVY8HlIeOO2auVSpS1ruFuEs8A9lq7qqHRUruKofTTA3ecodGj_ojgAemYaZUEcuxanfeadp9hObsWJv9N2J5Jd2Pls1UAdanCKXKHDg70Ienggg?width=768&height=1024&cropmode=none"
  small = "https://iskkpa.by.files.1drv.com/y4mkdmObmsu_UM2mLGV3_ae4616KwLRPGCHkC6EN98CEkroqnjsHTsEB3pZ3vpp9D5dOv_v8Pqd4HTqu30VrzAvMQpPpPNU2DlIQo1GLRIVY8HlIeOO2auVSpS1ruFuEs8A9lq7qqHRUruKofTTA3ecodGj_ojgAemYaZUEcuxanfeadp9hObsWJv9N2J5Jd2Pls1UAdanCKXKHDg70Ienggg?width=192&height=256&cropmode=none"
+++
{{< muted >}}
For the complete, working example, check out the code: {{< outref src="https://github.com/acbilson/connected-containers" name="connected-containers" >}}.
{{< /muted >}}

# Introduction

Have you ever had that sinking feeling when you remember that you've solved this problem before but you don't remember where you stashed the solution? And the sense of frustration searching for it, especially when it doesn't turn up in your usual places? Yea, that's why I'm writing this down where I can find it.

I love the concept of sandboxed environments that can be provisioned and destroyed at whim, which is why I love Docker. I've built dozens of applications using Docker, and I feel a sense of joyful satisfaction whenever I return to an old project, run `docker-compose up -d`, and it _just works_.

When I want to utilize software inside one Docker container to interact with my other Docker containers; however, I haven't been happy with the options. For example, if I want to run a Jenkins server that executes integration tests in another container my Google searches list two options. I'm here to propose a third.

# Three Options

First, a couple of definitions.

What I refer to as the controller is the container where your orchestration software resides. It's where you'd install Jenkins, which then would run jobs on the other containers. I'll use the &#127918; emoji to indicate steps for this container.

The client is the container where your code's dependencies sit. It's where you'd install the build dependencies (if it's a build container) or where your testing executables are copied. I'll use the &#128119; emoji to indicate steps for these containers.

## Option #1. DIND

The most commonly suggested path is to use a Docker-in-a-docker (DIND) container as the controller, install your software (for example, Jenkins), and launch new containers from within this container.

Although I did get a prototype working with this system, it felt wrong to have my containers two levels deep. I wanted to have direct access from my terminal into any one of my running containers, not to connect to the controller, then jump from there into a client container.

## Option #2. Local Machine

The other option was to abandon the sandbox approach and use my local machine as the controller.

This defeated my purpose for containers, which is to resist installing complex software on my local machine. When I install software locally I end up configuring it. Later, when I want to reinstall the software or put it onto another computer, I spend days running into configuration problems because I didn't remember everything I'd done over the weeks I'd operated the software on the original machine. Jenkins is a great example because it's so heavy on configuration.

With all that said, let's consider a third option.

## Option #3. Connected Containers

What if, instead of running DIND or installing to my local machine, I launched both a controller and a client container, install my orchestration software on the controller, then laterally wire up my controller to the client? This is what I've opted to do, and I'd like to walk you through it.

# Connected Container Steps

> Caveat: I wrote these instructions weeks after I pulled this off... for the second time. Even though this post may sound like it was straightforward, this option took hours of tinkering to finally get it to work.

These steps are listed by execution, not by location. It's a commentary on the steps in my [run.sh](https://github.com/acbilson/connected-containers/blob/master/run.sh) example, with each example pulled verbatim from the scripts.

## Give User Shared Volume Ownership &#127918;

I didn't run into this issue right away, but at some point I discovered that copying my SSH public key to a shared volume location will fail unless the container user has ownership of the folder. Docker grants shared volume ownership to root by default, so I needed to change this first.

{{< highlight docker >}}
docker exec --user root "$CONTROLLER_NAME" \
  /bin/bash -c "chown controller $KEY_DRIVE"
{{< / highlight >}}

## Generate SSH Key &#127918;

Now that the `controller` user has ownership of the shared volume (set to variable: `KEY_DRIVE`), it's time to generate the key. I discovered in the process that using the `-P` option with an empty string skips the passphrase user input.

{{< highlight sh >}}
mkdir -p ~/.ssh && \
ssh-keygen -t rsa -f ~/.ssh/controller_rsa -P "" && \
cp -f ~/.ssh/controller_rsa.pub "$KEY_DRIVE"
{{< / highlight >}}

## Add Public Key &#128119;

With the SSH key generated and shared, now my clients must authorize it. My example only runs one client, but it shouldn't (🤞) take much more to loop through all the clients you may run.

{{< highlight sh >}}
mkdir -p ~/.ssh && \
  cat "$KEY_DRIVE"/controller_rsa.pub >> ~/.ssh/authorized_keys
{{< / highlight >}}

## Start SSH Service &#128119;

For full automation, I need the ssh service running on every client. So I spin it up inside the container.

> Note: Service interaction varies widely between Linux distros. I'm using Debian for all my containers.

{{< highlight sh >}}
/etc/init.d/ssh start
{{< / highlight >}}

### Remove Password Access &#128119;

I try to use Docker as responsibly as I would if I were administering these containers in a public cloud. Now that I have SSH key authentication, there's no reason to remote access containers by password auth. So I disable it.

> This step also proves my success since my controller can no longer access other containers by password.

{{< highlight sh >}}
sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
{{< / highlight >}}

### Add Client IP to Host &#127918;

The first time the controller connects to a client requires user input to verify that the connection is appropriate. I bypass this request by adding the client to the controller's list of known hosts.


{{< highlight sh >}}
ssh-keyscan -t rsa "$CLIENT_NAME" >> ~/.ssh/known_hosts
{{< / highlight >}}

### Verify Connection &#127918;

We're finished! But just to be certain, let's verify that the controller does have automatic access to the client by running a simple `whoami` on the client from the controller.

{{< highlight sh >}}
ssh -i ~/.ssh/controller_rsa client@"$CLIENT_NAME" whoami
{{< / highlight >}}

## Design Choices

You'll notice that my shell scripts are added to the containers with shared volumes and executed by `docker exec` commands. You might think it'd be a better practice to copy the scripts in the Dockerfile and run them while building the image. Then you'd have images pre-built for connection. That was my first attempt.

What I discovered, however, was that the steps were inviolably interconnected between containers and, try as I might, there was no way to enforce order except to pull the steps entirely out of image creation and into the container startup.

---

Now the steps are listed here so, when I need them again, I'll have them!
