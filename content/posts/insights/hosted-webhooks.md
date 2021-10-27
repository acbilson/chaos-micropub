+++
backlinks = [
  "/notes/craft-your-own-site"
]
category = "technology"
comments = true
date = "2020-09-23"
description = "In which Alex describes how to configure a personal webhook server for git-flow-esque automation."
tags = ["webhook", "hosting", "git-flow", "hugo"]
title = "Hosting a Webhook Server"
[featuredImage]
  alt = "Graham Builds a Train Set"
  large = "https://bn02pap001files.storage.live.com/y4mA_H-d0LrDzW4Xzahz6PI89jsuIztpY7-FO4tk77xfhteqAOdS1Z7VX44uJPGWJx6RQO0A1_laz9F48Bis85QW3ew_Z7RZ7riB5iHQx0z2rLAw8JejVqgW60V3O-N8K8YXTWrJrlGiCWdQMLNpioIOJdbZzp65Qf2EHZ7bTnkQ4eToOK38dInjx9VLQQUrmvL?width=768&height=1024&cropmode=none"
  small = "https://bn02pap001files.storage.live.com/y4mA_H-d0LrDzW4Xzahz6PI89jsuIztpY7-FO4tk77xfhteqAOdS1Z7VX44uJPGWJx6RQO0A1_laz9F48Bis85QW3ew_Z7RZ7riB5iHQx0z2rLAw8JejVqgW60V3O-N8K8YXTWrJrlGiCWdQMLNpioIOJdbZzp65Qf2EHZ7bTnkQ4eToOK38dInjx9VLQQUrmvL?width=192&height=256&cropmode=none"
+++
If you've followed the {{< backref src="/posts/resources/steps-to-self-hosting" >}}, you've got a static site you can build and deploy to your local server. The process is simple and entirely within your control, but it does limit how you add posts to your website. If you just want to put a quick note up on your site, you've got to access the laptop from which you've built the website, write a new post, publish the update, and pull the update on our local server. That's a lot of steps, limited to your laptop. Can you add a note more easily?

Yes, you can! Enter the magic of webhooks.

A webhook is a simple server that accepts a payload and runs a command on the server when certain criteria are met. Many services use webhooks to allow developers to automate workflows. For example, Github offers webhooks to allow developers to kick off processes when command actions occur on their repository, such as sending an email when a pull request is submitted. But these services host their own webhook servers, which means we'll need to run the same technology on our local server to get the effect. For this exercise, I'll be using Adnan's brilliant tool, aptly called [webhook](https://github.com/adnanh/webhook).

If you're familiar with software, you know there are infinite other ways you could achieve this. You might build your own custom server that receives HTTP requests and executes functions on your server. There are probably already libraries to plug into your code that will manage common tasks like working with Git repos. The webhook approach separates the server from the execution (which is in a script) and thus puts more burden on the admin to configure the file system instead of the developer to write the server code.

# Installation

First, let's discuss the bare minimum to get this setup working. It's nice to have the bare minimum so you can test it for yourself. Then we'll review security practices you'll want to implement before you start using this webhook.

To install webhook, I recommend you to the [source](https://github.com/adnanh/webhook/blob/master/README.md) since it's likely to be less out-of-date. All I had to do was install webhook from the package repository.

With webhook installed, we can choose to run it as a stand-alone server or to place it behind a reverse proxy. I'll show you my command for a stand-alone instance, then give you a simple template to configure an Nginx reverse proxy.

{{< highlight sh >}}
sudo /usr/bin/webhook -hooks /etc/webhook/hooks.json -port 9000 -secure -cert /etc/letsencrypt/live/mycoolsite/fullchain.pem -key /etc/letsencrypt/live/mycoolsite/privkey.pem -verbose
{{< / highlight >}}

Let's break this down.

The `-hooks` variable sets the path to your hooks.json file. This file configures your enabled hooks. You may have a webhook configuration that listens for a request from Github, verifies a header secret, then runs a git-pull script. Adnan supplies multiple examples.

The `-port` variable does what you expect, it runs the server on your specified port. You can also specify the host, or it defaults to localhost. Don't forget to open that port on your firewall if you're running stand-alone.

The `-secure` flag goes along with the `-cert` and `-key` variables enable SSL for your server. If you use a reverse proxy, you can configure SSL at that level and allow the webhook to run over HTTP since traffic won't leave your network unencrypted. However, if you do run webhook as a stand-alone server, DO ADD THIS! You don't want your Github header secret in plaintext.

To confirm it's running, you can run a simple curl command like so:

```
curl localhost:9000
```

If everything is good, you'll get an OK response.

# Configuration

I host two systems, production and user-acceptance-testing (UAT), because I attempt service integrations that are painful to replicate without a close-to-production environment. I use a simplified [git-flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) approach where feature branches are merged into a release candidate, then the release candidate will be merged into the main branch.

To automate my workflow, I want the following to happen:

1. When commits are pushed to main, my production site should rebuild with the latest in main.
2. When commits are pushed to a release branch, my uat site should rebuild with the latest in that branch.

Let's look at my hooks.json configuration and I'll explain.

{{< highlight json >}}
[
	{
		"id": "content-pull-webhook",
		"execute-command": "/usr/local/bin/build-site.sh",
    "pass-arguments-to-command": [
    {
      "source": "payload",
      "name": "ref"
    },
    {
      "source": "payload",
      "name": "repository.name"
    }
    ],
		"trigger-rule": {
      "match": {
        "type": "payload-hmac-sha1",
        "secret": "mysillysecret",
        "parameter": {
          "source": "header",
          "name": "X-Hub-Signature"
        }
      }
    }
  }
]
{{< / highlight >}}

This configuration listens for a Github event (in my case, a pull event), compares a hashed secret in the request header with a plaintext secret, then parses the HEAD reference and the repository name out of the request body and passes it as an argument to my shell script.

For completeness, here's a screenshot of my Github webhook configuration:

![github webhook configuration](/posts/data/github_webhook.png)

> If you're curious what's available in the request body, Github will display the complete JSON payload on the webhook page. You can also resend an event, which is perfect for testing!

But wait, there's more! This post intends to be a complete example, so here's the build-site.sh script.

{{< highlight sh >}}
#!/bin/sh

# Sets the arguments to variables
REF=$1
REPO=$2

BRANCH=unset
PATH=unset
DIST_PATH=unset
CONFIG_PATH=unset

# Verifies that the repository is valid and sets its path
####
case $REPO in

  chaos-content)
    PATH=/mnt/chaos/content
  ;;

  *)
    echo "$REPO was not a valid git repo"
    echo "################"
    return 1
  ;;
esac

# Verifies that the branch reference matches and sets the correct distribution location
####
case $REF in

  refs/heads/main)
    BRANCH=main
    DIST_PATH=/var/www/site
    CONFIG_PATH=/etc/hugo/config-prod.toml
  ;;

  # use basename to strip the release number off the HEAD reference
  refs/heads/release/*)
    BRANCH="release/$(/usr/bin/basename $REF)"
    DIST_PATH=/var/www/uat
    CONFIG_PATH=/etc/hugo/config-uat.toml
  ;;

  *)
    echo "$REF was not a valid git reference"
    echo "################"
    return 1
esac

echo "checking out $BRANCH for content"
echo "################"
cd /mnt/chaos/content
/usr/bin/git fetch

# Retrieves content based on which repo is requested
#
# This approach allows me to have a release candidate for one
# repo and use master for the other, or the same release candidate
# for both.
####
case $REPO in

chaos-content)

  echo "\nfetching content"
  echo "################"
  cd /mnt/chaos/content && /usr/bin/git fetch

  echo "\nchecking out content on $BRANCH"
  echo "################"
  /usr/bin/git checkout $BRANCH

  echo "\npulling latest from $BRANCH"
  echo "################"
  /usr/bin/git pull
;;

esac

echo "\nbuilding site from $BRANCH to $DIST_PATH"
echo "################"
/usr/bin/hugo \
  -d $DIST_PATH \
  --config $CONFIG_PATH \
  --contentDir /mnt/chaos/content \
  --themesDir /mnt/chaos/themes \
  --cleanDestinationDir

{{< / highlight >}}
