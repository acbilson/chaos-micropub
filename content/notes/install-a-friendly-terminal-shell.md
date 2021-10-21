+++
backlinks = [
  "/notes/craft-your-own-site"
]
author = "Alex Bilson"
date = "2021-07-29T16:52:25"
lastmod = "2021-08-02 14:59:07"
epistemic = "plant"
tags = ["shell","fish","terminal"]
title = "Install a Friendly Terminal Shell"
+++
If you're unfamiliar with a terminal command line or tired of using bash, you'll benefit from installing another shell. There are a number of options, but the fish shell is the simplest to install and use. Simple doesn't mean basic - it's elegant and wonderful.

# Install Fish

First, install fish. On MacOs the command is:

{{< highlight sh >}}
brew install fish
{{< /highlight >}}

> If you need an exhaustive install manual, see {{< outref src="https://github.com/jorgebucaran/cookbook.fish" name="Jorge's cookbook" >}}.

You're done! Just type `fish` into your terminal and it'll switch over. If you want your terminal to start with fish by default, run this:

{{< highlight sh >}}
chsh -s /usr/local/bin/fish
{{< /highlight >}}

# Customization

Unlike any other shell, fish has a web interface to customize. Run `fish_config` and view the awesomeness!

I have a couple recommended plugins, so lets install a package manager to make this simple.

{{< highlight sh >}}
curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher
{{< /highlight >}}

The prompt isn't terrible, but I prefer minimalism. For that, you'll want the hydro prompt:

{{< highlight sh >}}
fisher install jorgebucaran/hydro
{{< /highlight >}}

My most common error when typing a command is to miss a closing parenthesis or quote. Never again with:

{{< highlight sh >}}
fisher install jorgebucaran/autopair.fish
{{< /highlight >}}

