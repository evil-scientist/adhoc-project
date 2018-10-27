# HOWTO GIT v2.0

Me (Jur) and Sury have reorganised github repo a bit- to make it cleaner and more effective to work with.  
Before we only worked on one "master" branch, and we only had one commit history track. This was annoying  
bcs if I worked on experiment_1 and Sury pushed his experiment_4 to github, I had to pull his changes  
and only then I could push my work. The goal is to separate commit history and not to interfere in the  
workflow of others.

Anyway now there are 5 branches on the server (github):  
    master + simulation, exp1, exp2, exp3


So first, clone the repository or just pull the changes if you have it already.
Then if you want to work on experiment 1 for example, work on branch `exp1` and push to this branch as well.  

Which branch am I on currently?  
`git status` on the top OR `git branch`  

How to switch to different branches?
`git checkout <name of branch>`

How to merge commits from master branch into my current branch?
`git merge master`

How to merge commits from my current branch into master?
1. `git checkout master`
2. Merge from the branch you worked on `git merge --squash <name of branch>`
3. Commit and write into the message what have you merged into the master `git commit`

How to see commit history only for my branch?
`git log <name of your branch> --not master`


Let's have our master branch for "finished" tasks only - so when you finish one feature (that can be compiled/run) by anyone,
merge it to master. For work in progress and stuff - let's try to use branches.

**TL;DR** if you don't have time or energy to learn something about GIT-> you can just keep working as we did until now. But give
it a try -> it's useful to know git, it's not as hard as it seems, just read the basic tutorials to get the terminology and concepts right.

https://www.atlassian.com/git/tutorials 
https://git-scm.com/book/en/v1/Getting-Started 
