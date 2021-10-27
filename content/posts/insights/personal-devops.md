+++
aliases = ["/posts/personal-devops/"]
category = "technology"
comments = true
date = "2021-03-10"
description = "In which Alex catalogs his thought progression from bare-metal to Kubernetes."
tags = ["consulting", "bare-metal", "raspberrypi", "ci/cd", "k3s"]
title = "Personal DevOps"
[featuredImage]
  alt   = "Graham and Royal in a Wicker Container"
  large = "https://bn02pap001files.storage.live.com/y4mzPw7Fpg9BxjkAp7GJ85UMQwRvbYOJg2WsJNfj07VP-D_r02oepgkx3DEqcgRSUi0eCc8Mv6PER6Te-Zfl8N62H-mQPVyHXBvNy7zXwrM2z12vEswjTuPbXf_6IwZyoI_lKcNfTF5MYwekOBu_rVu6PDsS-1lfA0cwcmFH_lWdWZdV_0ZLkJfqj6HjNzXayPy?width=768&height=1024&cropmode=none"
  small = "https://bn02pap001files.storage.live.com/y4mzPw7Fpg9BxjkAp7GJ85UMQwRvbYOJg2WsJNfj07VP-D_r02oepgkx3DEqcgRSUi0eCc8Mv6PER6Te-Zfl8N62H-mQPVyHXBvNy7zXwrM2z12vEswjTuPbXf_6IwZyoI_lKcNfTF5MYwekOBu_rVu6PDsS-1lfA0cwcmFH_lWdWZdV_0ZLkJfqj6HjNzXayPy?width=192&height=256&cropmode=none"
+++
# The Journey Begins

When my raspberry pi arrived two years ago, I opened it with excited trepidation. Will I overcome the hurdles to self-hosting on an unfamiliar architecture and operating system? How performant will it be? What tools will I learn, or give up, to achieve my goals?

Once I had figured out the [steps to self-hosting](/posts/steps-to-self-hosting), I felt confident hosting my own static blog. But it wasn't long before I began to dream of more. What if I could publish content to my static site from anywhere, and not only when I have network access? What if I want to integrate other services into my website, like a daily memorial of covid-related deaths in Cook County?

My first project after a working static site was to create a way to continuously publish. The coolest writing tools already have this functionality, so why can't I? My site's content is stored on Github, so it was fairly simple to use Github hooks, a webhook server, and a little client-side JavaScript to accomplish the same workflow. To improve security I ended up writing my own publishing server, but that's another story.

Still amazed that my publishing server works, I discovered this amazing data publishing tool called [datasette](https://github.com/simonw/datasette). Simon's examples got me dreaming of what I might do with a plug-n-play sqlite web interface, and I landed on [displaying the daily covid-related deaths in Cook county](/posts/data-journalism).

Somewhere between running my static site and creating a publishing server, I became nervous that all my tinkering would be demolished if my raspberry pi's SD card were corrupted. Time to [learn Ansible](/posts/learning-ansible)!

Ansible turned out to be a time-saver. Not only did it give me disaster recovery, it also simplified standardization. For example, when I began to secure my services by running each as a distinct non-root user, the boilerplate user/group setup was simple and replicable via Ansible. It would have been more error prone and annoying if I'd done each service by hand, one at a time.

> If you're going to use Ansible to manage server configurations (which you totally should), don't mix-and-match with direct updates. As soon as you start making configurations directly on the server you become nervous about using automated configuration lest you accidentally overwrite your work! #lessonslearned

Now I have a few services running on my raspberry pi, but {{< acronym FOMO "Fear Of Missing Out" >}} is rising - is it time to go full container, kubernetes style? There's even [k3s](https://k3s.io/), a light-weight version of kubernetes that's designed for my raspberry pi!

# Container CI/CD Diversion

I manage my services with supervisord and enjoy the freedom to configure each aspect. I can limit system access, configure logs, and manage ingress without much trouble. Linux services enjoy inherent stability and add little overhead. I've used Ansible to deploy my growing configurations so the fear that I'll lose it all is reduced. But it's still a lot to review and configure. Wouldn't it be cool if I were running k3s with a cluster of containerized services instead of a "normal" machine with boring old systemd services?

When I began to chart this course, I uncovered an assumption in my existing workflow. I conceptualized my existing setup as a single production deployment with several services, but when I tried to map each service to a container it became obvious that there are two distinct service types - {{< acronym "CI/CD" "Continuous Integration / Continuous Deployment" >}} and production. For example, I imagined running my webhook service in a single container but soon realized that every time the service created a new page on my static site it would need to generate a new static site container and replace it in the same cluster. A container that replaces other containers in the same cluster? This smells fishy to me.

So I pondered alternatives and came to the conclusion that larger kubernetes instances likely run separate clusters for CI/CD and production. So it seems I'd have to run two clusters to make my workflow happen - not awesome. All this to replace a small set of tiny Linux services that haven't given me a hiccup in over a year?

Of course, if this were a twenty person development team working on a dozen microservices, the ability to generate and test new container images by pushing a Git branch is stellar. The chances for error would increase if each developer independently updated their microservice configurations live on the servers like I do with my raspberry pi. No mystery why a company can justify running multiple CI/CD kubernetes clusters. However, I'm not a twenty person team so, as cool as running a CI/CD kubernetes cluster on my raspberry pi would be, I can't justify the cost. But I still want to understand how production kubernetes works, so I shelved this diversion for a bit.

> I did look into creating a lightweight CI/CD cluster with [podman](https://podman.io/), [buildah](https://buildah.io/) and [skopeo](https://github.com/containers/skopeo). While this path has merit, I found that ARM support isn't complete enough for me to try these tools out without low-level troubleshooting. I'm just not committed enough to my pet projects to spend hours digging through errors.

# Another Day, Another Perspective

When I came back to the problem, I decided to create a network diagram to describe my existing infrastructure and a second diagram to describe my proposed kubernetes infrastructure. By starting with what I had, I soon realized that I didn't need to think about deploying new containers on a regular basis if I treated the static content like a database. When Markdown files are added, if they're shared via persistent storage instead of inside containers, all my container deployment issues went away!

A diagram is worth ten thousand words, so here's what I've modeled. First, my existing architecture.

{{< image "/posts/data/arch/bare-metal_deployment.svg" "diagram" >}}

Notice how simple it is. When I push an update to my site, my webhook service pulls the update and compiles the site for nginx to serve. If I send an update with my publishing service, it stores the new file in my content repo, pushes a change, and the same webhook process fires. To load data onto my static site I run a datasette instance. Simple and effective.

Then, my proposed kubernetes cluster architecture.

{{< image "/posts/data/arch/k3s_deployment.svg" "diagram" >}}

I've split the deployment into two because my site does not depend upon the data server to operate, but it does depend upon my build and publish server to manage my own CD process. I've also moved from a model where every time I publish it stores a new file, pushes it to my repo, and rebuilds to a scheduled build. I've kept the publish and build processes separate so that I can still support either or both options, but I've found that I don't care that much about seeing what I publish immediately render on my site.

My hope is to add little complexity by switching to kubernetes while enabling me to deploy updates to any part of the system by swapping in a new container image, but I'm still learning kubernetes and haven't actually tried this (yet). Feedback is welcome 😁.

# Conclusion

Here's where I've landed, at least for today.

The state of container CI/CD at this time requires a dedicated node, and I'm not ready to buy another raspberry pi to make that happen. But I don't need container CI/CD anyways, just a means to back up my Markdown content, so who cares? I can run the whole shebang on my raspberry pi with no need for regular container deployments AND get practice running k3s. Win/win, don't-cha think?
