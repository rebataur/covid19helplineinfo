git add --all
@echo off
read -p "If applied, this commit will: " msg
echo $msg
git commit -m "$msg"
git push -u origin master

