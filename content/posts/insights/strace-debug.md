+++
aliases = ["/posts/strace-debug/"]
category = "technology"
comments = true
date = "2020-10-03"
description = "In which Alex describes a debugging moment."
tags = ["debug", "strace", "cli"]
title = "Debugging keychain with strace"
[featuredImage]
  alt = "strace output"
  large = "https://vzbzfg.by.files.1drv.com/y4mNACbUB9fk3tBZ-XNN1yayYhr7fqP9rWjgSmByo4z7ZjBeckIx4uoRiZ56cm1EZgPC8IZVnUOID9bOrO29Owr1eMschMOPhFQyuCXsqz1Yx_DFJIrepY-IO6THq5_9oAL6UZK0ynOE88_KI8Z5JbyN5gY32HnsNjoutEVC4PGjAf5oDeCLYDIq3PWaQXz_ngbHhPG9LMxFdVx6_leR3Mb6A?width=1024&height=711&cropmode=none"
  small = "https://vzbzfg.by.files.1drv.com/y4mNACbUB9fk3tBZ-XNN1yayYhr7fqP9rWjgSmByo4z7ZjBeckIx4uoRiZ56cm1EZgPC8IZVnUOID9bOrO29Owr1eMschMOPhFQyuCXsqz1Yx_DFJIrepY-IO6THq5_9oAL6UZK0ynOE88_KI8Z5JbyN5gY32HnsNjoutEVC4PGjAf5oDeCLYDIq3PWaQXz_ngbHhPG9LMxFdVx6_leR3Mb6A?width=256&height=178&cropmode=none"
+++
Here's a fun little debugging story.

I'd begun to use [keychain](https://www.funtoo.org/Keychain) to manage ssh keys across processes. Before keychain, ssh-agent processes would multiply because each script that needed access to an ssh key would spawn its own ssh-agent process.

But then I found this error. When I ran <code>eval \`/usr/bin/keychain --agents ssh --eval my_rsa\`</code>  while logged into my shell, the keychain process correctly applied the ssh key to my user's ssh-agent process. However, when the same command was run by the same user on a webhook process, the command failed with the following message:

> mkdir: cannot create directory "/.keychain": Permission denied

I figured out that my user has a ~/.keychain directory, which meant that keychain seems to be creating the same directory for root. I checked the webhook process to confirm it wasn't running as root. It wasn't. But that still didn't explain why keychain was creating a root copy of the .keychain directory.

I couldn't figure out why the command succeeded in my shell but failed when executed by my webhook process. I remembered that Julia Evans has a [series on strace](https://jvns.ca/categories/strace/). With Julia's help I put a trace on the webhook process and dumped it to a local file with this command: `strace -yf -p 27404 -o temp.txt`. With a little grepping I discovered some lines like this:

{{< highlight sh >}}
27727 stat64("/.keychain", 0xbea5f6f8) = -1 ENOENT (No such file or directory)
{{< / highlight >}}

(My original logs were overwritten while debugging or I'd show you a better example, like the trace of the failing mkdir command and its context.)

This example line says, "thread 27727 checked for statistics on a file or directory ([stat64](https://linux.die.net/man/2/stat64)) at '/.keychain' and returned -1, which means this file or directory does not exist"

What I discovered from digging through the stack trace is that the thread in question was looking in the correct place, my user's home directory, but then moving on to the root directory to find relevant keychain files.

So now I knew that the problem was further upstream than the mkdir error, which meant that I needed to recreate the error in my shell.

I killed all the running ssh-agents with `keychain -k all` and attempted to re-add my ssh key. That's when I discovered this error:

> Warning: Cannot find separate public key for id_rsa.

Well, that's interesting! I never added the public key to my server because it didn't seem necessary. But keychain was expecting to find both private and public keys. Somehow it was getting by in my shell; probably because the private key had already been loaded before I began to use keychain. When it didn't find the public key in my user's .ssh folder, however, it began to look elsewhere. Hence the error (far as I can tell).

To solve this issue, I generated a new ssh key, copied both private and public keys to my server, and updated the endpoint with my new public key. Viola, success!

To summarize, I was seeing an unexpected error from a process that I didn't see when executing the same line in my shell. With Julia's strace help I was able to piece together enough of keychain's logic to determine that the error happened when the process searched a backup path after an error occurred in the user's directory. I killed my shell's ssh-agent processes and discovered a keychain warning about a missing public key. When new private/public keys were added, my error disappeared.

UPDATE: it turns out that's not all to fix my issue. I discovered afterward that keychain pulls its context from the HOME variable, which is different based on the process. Fortunately, poking through the help page revealed that I could override this value with `--dir /my/root/path`. It's good to know, however, that I also needed to read the full path to the ssh key because it apparently still depends on HOME. Here's the final result:

{{< highlight sh >}}
eval `/usr/bin/keychain --dir /home/user --agents ssh --eval /home/user/.ssh/id_rsa`
{{< / highlight >}}
