+++
backlinks = [
    "/notes/craft-your-own-site"
]
author = "Alex Bilson"
comments = false
date = "2021-07-23T12:49:13"
epistemic = "seedling"
tags = ["terminal","sed","grep"]
title = "Replace Text Across All Content"
+++
As my content grows, so does my need to make adjustments across dozens of files. I'm familiar with `grep` and it's successor, `ripgrep`, and I'm familiar with `sed`, but I can never quite remember how to make replacements in-place. Here's how:

{{< highlight sh >}}
rg -il '< backref' | xargs sed -i "" -e 's/backref "\(.*\)"/backref src="\1"/g'
{{< /highlight >}}

First, you retrieve the relative file path of the files you want to change. Technically, you could run the command against every file and it would only operate on content that matches, but there's no reason to be so inefficient. A nifty feature of `rg` is that it automatically skips `.git` folders, so if you use it's predecessor, `grep`, be sure to skip that folder.

Second, you run the stream editor, `sed`, on the content of each file. The `xargs` command pipes the output from `rg` line-by-line to `sed`.

If you're just fixing a misspelling, you could simplify the `sed` replacement to `'s/oldtext/newtext/g`. The `g` applies the change to every occurrence on every line. However, many replacements are more complex than changing a single text value, so using `\(` and `\)` to form a group selection that can be referred to by index `\1` is invaluable.

The above is Mac-specific because sed's `-i` flag works differently than others. You can simplify this on Windows/Linux to:

{{< highlight sh >}}
rg -il '< backref' | xargs sed -i 's/backref "\(.*\)"/backref src="\1"/g'
{{< /highlight >}}
