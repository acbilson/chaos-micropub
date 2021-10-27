+++
backlinks = [
    "/notes/craft-your-own-site"
]
aliases = ["/comments/20201008-210602/"]
date = "2020-10-08T21:06:02"
epistemic = "plant"
tags = ["makefile","html","testing"]
title = "Self-Documenting Makefile"
+++
My favorite build tool is `make`. It's ironic that I've written little clang code given that the tool was created to manage building all those C libraries with header and source files. But whenever I see a `Makefile` I get excited.

The tool doesn't do much, at least for my use-case. It explicitly defines build dependencies and codifies the available commands in a Git repository. Do I need more from a build tool?

One feature `make` _is_ missing (maybe) is a straightforward way to list what options are available in the file. Kudos to Victoria Drake for the [self-documenting makefile](https://victoria.dev/blog/how-to-create-a-self-documenting-makefile/) snippet to add this feature to your own `Makefile`. I suggest adding these lines before any other commands so that running the base `make` command displays the help list.

{{< highlight sh >}}
.PHONY: help
help: ## Show this help
    @egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | \
    awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
{{< / highlight >}}
