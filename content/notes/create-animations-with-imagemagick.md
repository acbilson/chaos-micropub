+++
backlinks = [
  "/notes/craft-your-own-site"
]
author = "Alex Bilson"
date = "2021-09-03"
lastmod = "2021-09-03 14:09:28"
epistemic = "sprout"
tags = ["gif","command-line","imagemagick"]
title = "Create Animations With Imagemagick"
+++
I've considered the tool `imagemagick` on multiple occasions (it does practically anything you could imagine with images), but finally downloaded and tested it out. Here's how I created a useless gif animation.

First, generate two gifs.

{{< highlight sh >}}
convert -pointsize 20 -page 50x20 label:Open -append open.gif; \
convert -pointsize 20 -page 50x20 label:Close -append close.gif
{{< /highlight >}}

Next, combine them together into an animation.

{{< highlight sh >}}
convert -delay 100 -page 50x20 open.gif -page 50x20 close.gif -loop 0 animation.gif
{{< /highlight >}}

Open up `animation.gif` in your web browser and, viola, that's it!

{{< raw >}}
<img style="width: 50px" src="/notes/data/animation_example.gif"/>
{{< /raw >}}

