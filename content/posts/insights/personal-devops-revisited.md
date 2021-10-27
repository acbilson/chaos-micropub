+++
category = "technology"
comments = true
date = "2021-10-19"
description = "In which Alex progresses further from baremetal towards Kubernetes."
tags = ["consulting", "bare-metal", "raspberrypi", "ci/cd", "k3s"]
title = "Personal DevOps Revisited"
[featuredImage]
  alt   = "Raspberry Pi With Glowing Lights"
  large = "https://bn02pap001files.storage.live.com/y4mC1ndbsdT9IhItBz1pa5mJtifO0kY0G50fGA1ycll7q-NTXheJW95wr2Y3oXIUBPaH30dGcOzLtY2-HTN9c2gjI_veEqLqXhZoeyFGGLkCiK_ruu_GlDhEXzODmkv7GFke_63LO5NwR_0lNZ9YHqcsk2Rr54lP-LmunA6R1kFjud8YzYNXcLY8so9F0piogBe?width=768&height=1024&cropmode=none"
  small = "https://bn02pap001files.storage.live.com/y4mC1ndbsdT9IhItBz1pa5mJtifO0kY0G50fGA1ycll7q-NTXheJW95wr2Y3oXIUBPaH30dGcOzLtY2-HTN9c2gjI_veEqLqXhZoeyFGGLkCiK_ruu_GlDhEXzODmkv7GFke_63LO5NwR_0lNZ9YHqcsk2Rr54lP-LmunA6R1kFjud8YzYNXcLY8so9F0piogBe?width=192&height=256&cropmode=none"
+++
My self-hosting journey has taken many turns since it began in 2019.

My first foray was little more than an Nginx proxy serving up Hugo-generated HTML files. As needs arose I began to add web services. Automated deployments with a webhook server and mobile publishing with a custom publishing service were two of the first. At the time I wrote {{< backref src="/posts/insights/personal-devops" >}}, I was also running a data-publishing service called {{< outref name="datasette" src="https://github.com/simonw/datasette" >}}, deploying server updates with Ansible, and managing all processes with supervisord.

I thought the natural progression was towards Kubernetes, so I attempted to make the transition to {{< outref name=k3s src="https://k3s.io/" >}}. When I drafted a network diagram, however, I discovered that the CI/CD process I wanted to implement to deploy my Kube nodes would require a second machine, and I didn't want to spend the money or manage the extra configuration. I had attempted an intermediary Podman installation but had run into difficulties configuring Debian Buster since it's not officially supported. But I didn't get very far until I also experienced trouble with k3s and, unwilling to let my site languish for weeks while I tried to implement a deployment process I didn't need, I abandoned the project. Fortunately, after bit of tinkering I _did_ get Podman working. And it's been a dream come true.

# The Podman Era

{{< image "/posts/data/podman-services.png" "services" >}}

One of the intermediary transitions I needed to move my services to Kubernetes was to containerize them. I had a few in Docker containers for local development, so it wouldn't take much, but running my production services as containers was a new experience. And it's been such a great experience.

Podman has been a pleasure to operate for three reasons.

- Instead of relying on a mysterious Docker daemon to operate my containers, Podman let me convert each container unit into a systemd service so I can leverage the stability and support of Debian's process management. Systemd services can be enabled to launch on startup and log output to the system journal. It just feels more, integrated.

- Docker didn't have native pod support. I couldn't launch a web service plus database as a single unit without a bit of finagling, or by using Docker Compose. Podman has pods that work identically to pods in Kubernetes and can be operated as a unit with, you guessed it, the systemd service architecture.

- Debian Bullseye is now a stable release, which means that Podman is now officially supported! I don't know if Docker was ever _officially_ supported, though I did see installation tutorials.

# Updated Architecture

{{< image "/posts/data/arch/podman_arch.svg" "podman architecture" >}}

# Conclusion

Thanks to {{< outref name="Jeff Geerling's" src="https://www.jeffgeerling.com/" >}} invaluable YouTube {{< outref name="Cluster Series - Part 1" src="https://youtu.be/kgVz4-SEhbE" >}}, it's evident that I need at least three nodes are necessary before Kubernetes is a worthwhile option. One node is dedicated to operating the cluster and offers little but resource consumption if it's the only node. Two nodes allow for only a single node for the master node to manage - again offering little and supplying no opportunity for Kubernete's container distribution logic. Two nodes for the master node to manage does give Kubernetes the chance to select the best node for a given pod, to have a backup for failed pods, and starts to become tedious to operate independently (barely).

{{< notice >}}
...at least three nodes are necessary before Kubernetes is a worthwhile option.
{{< /notice >}}

Is it time to move to Kubernetes? There's never been a better opportunity to make the attempt but, for my purposes, Podman may be the sweet spot. There's nothing k3s offers that my little Podman cluster can't already do with fewer resources. But with Debian Bullseye moving me closer to a fully supported OS, I might have to try anyways, if only to learn.
