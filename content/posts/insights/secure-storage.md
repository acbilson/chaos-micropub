+++
aliases = ["/posts/secure-storage/"]
category = "technology"
comments = true
date = "2020-07-08"
description = "In which Alex explains how tar, gzip, and gpg can keep your data secure in the cloud."
tags = ["security", "cloud"]
title = "Secure Cloud Storage"
[featuredImage]
  alt   = "Rusted deadbolt lock"
  large = "https://images.unsplash.com/photo-1484043937869-a468066a4fbd?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
  small = "https://images.unsplash.com/photo-1484043937869-a468066a4fbd?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
+++
{{<photoref "James Sutton" "https://unsplash.com/@jamessutton_photography" >}}

I was updating my resume the other day when something creepy happened. Dropbox, where my resume sits, showed me an advertisement for resume assistance.

If it's not clear why this creeped me out, consider:

1. to know the file was a resume, Dropbox needs to scan the entire document. It wasn't called 'resume'.
2. the scan is sophisticated enough to accurately determine the contents of what I've written.
3. at least some of this data is shared with the owner of the advertisement. Worst-case scenario, the advertiser _created_ the file scanner.

I'm happy to share my resume with Dropbox (maybe they'll offer me a job? &#128521;), but what about all the other data? What about my private journal? I need a way to ensure select files can't be used by Dropbox or third-party advertisers. For this, I turned to the command line.

Two command-line programs married together in a single shell script secured my files, `tar` and `gpg`. Here's a run-down.

## tar

Put simply, this command rolls all specified files into one. The command has been around for ages, exists on every machine, and just works, so I use it instead of a newer algorithm. Run without options, the command will generate an output file with the exact number of kilobytes as the input files, but I use the compression option to save space. My journal files are stored in my current working directory for this example.

{{< highlight sh >}}
tar -czvf journals.tar.gz *
{{< / highlight >}}

## gpg

This command is short for [GNU Privacy Guard](https://gnupg.org). Unlike `tar` you may need to install this program, but it's free and widely available.

If you haven't generated a private key before, [follow the instructions](https://gnupg.org/gph/en/manual.html#AEN26). If you have an existing key on another machine, export/import your private key.

Once your private key is ready, let's run the following command to create an encrypted copy of our journals file.


{{< highlight sh >}}
gpg -o journals-safe.tar.gz.gpg -e -r acbilson@gmail.com journals.tar.gz
{{< / highlight >}}

## Last step

Programs like Dropbox keep every file that's uploaded, even if the user deletes it, so these steps won't make a difference unless the original files are never synced. To achieve this, we move the original's location outside the Dropbox sync folder. This way we can move only the secure version of our journals to Dropbox.

All of this is easily scripted. Here's an example:

{{< highlight sh >}}
#!/bin/sh

secure-journals () {

  ORIG=$(pwd)

  # navigates to journal directory
  cd ~/Journal

  # combines and compresses all journal files
  tar -czvf journals.tar.gz *

  # encrypts a copy of the journals file with my private key
  gpg -o journals-safe.tar.gz.gpg -e -r acbilson@gmail.com journals.tar.gz

  # moves the encrypted file to Dropbox and removes the intermediate tar.gz file
  mv -f journals-safe.tar.gz.gpg ~/Drobox//Journal/journals-safe.tar.gz.gpg
  rm journals.tar.gz

  # returns to wherever I was before
  cd "$ORIG"
}

 secure-journals
{{< / highlight >}}
