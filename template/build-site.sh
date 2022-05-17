#!/bin/sh
export GIT_SSH_COMMAND="/usr/bin/ssh -i /root/.ssh/git_rsa"

echo ""
echo "new file at $1"
echo "############"

echo ""
echo "moving to content dir"
echo "############"
cd /mnt/chaos/content

echo ""
echo "configuring bot git user"
echo "############"
git config user.name "Micropub Bot"
git config user.email "micropub@bot.dev"
git config core.autoclrf "true"

echo ""
echo "switching to master branch"
echo "############"
/usr/bin/git checkout master

echo ""
echo "committing new file"
echo "############"
/usr/bin/git add $1
/usr/bin/git commit -m "AUTO: adds new file"

echo ""
echo "pushes new file to prod"
echo "############"
/usr/bin/git push

# if the chaos-webhook service is running, it will pick up
# this update and build the site. If it is not, then at least
# this may prevent merge conflicts
