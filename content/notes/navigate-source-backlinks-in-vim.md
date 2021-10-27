+++
backlinks = [
    "/notes/craft-your-own-site"
]
author = "Alex Bilson"
comments = true
date = "2021-06-18T19:32:11"
epistemic = "plant"
tags = ["vim","backlink","markdown"]
title = "Navigate Source Backlinks in Vim"
+++
If you've begun to use backlinks on your static site and you also use Vim as your primary text editor then you'll appreciate how cool it is to configure Vim's `gf` command to navigate via backlinks.

My files aren't referenced relative to my current directory so I need to take more steps to configure `gf`, but if the files are sourced relative to one another then you won't even need these steps. My backlink references look like this: `/notes/what-is-the-gospel`

### Step 1. Add Root to Path

If Vim cannot find the file by relative path, it will prepend each path property and retry its search. Using my example above, add to path whatever completes the absolute path to your file reference. In Vim code:

```
set path+=~/my/source/path
```

### Step 2. Add File Suffix

If there is no file ending (suffix), Vim will iterate over the default suffixes to find your file. My references are engineered to match the URL path rather than the source file path, so I need to add the Markdown suffix. I decided to add this suffix only when working with Markdown files.

```
autocmd FileType markdown setlocal suffixesadd=.md
```

### Remove Leading Slash

If your backlinks are formatted as absolute paths (i.e. they have a prepended '/') Vim can't parse the path. I didn't dig further to understand why. So we're going to un-absolute them by removing the slash prefix. I've also applied this only to Markdown files.

```
autocmd FileType markdown setlocal includeexpr=substitute(v:fname,'^\/','','g')
```

> It's strange to apply this regex expression multiple times (the 'g' modifier), but for some reason I couldn't get it to work otherwise. Another one of those things I didn't dig further into.

Add these three lines to your .vimrc file and navigate your source content like you would from the browser!

Thanks to [Edwin](https://www.edwinwenink.xyz/posts/42-vim_notetaking/) for the idea.

