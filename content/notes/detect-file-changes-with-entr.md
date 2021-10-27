+++
backlinks = [
  "/notes/craft-your-own-site"
]
aliases = ["/comments/2020-07-01_19:30:13"]
date = "2020-07-01T19:30:13+01:00"
epistemic = "seedling"
title = "Detect File Changes With entr"
tags = ["cli","devops"]
+++
 How have I never heard of entr? This amazing CLI makes it possible to run my custom build scripts on file change, just like many of my favorite tools. Thanks for [sharing](https://jvns.ca/blog/2020/06/28/entr/) Julia!

I organize various commands with a Makefile that executes Bash scripts. Some tasks, like running a test suite, should be run every time I make a change. If you have a similar configuration as I do, you can simply run the following in your terminal and it'll execute your test suite on every change! It's important to note that new files will not be captured without restarting this command since it pipes a full list of existing files from the moment you started it.

{{< highlight sh >}}
find ./src | entr make test
{{< /highlight >}}
