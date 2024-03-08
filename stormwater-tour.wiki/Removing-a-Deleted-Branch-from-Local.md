Notice that info_feedback was deleted. That feature is complete the branch is not needed. If you have `git pull`ed on your machine you will need to remove the branch.

So `git pull` will retrieve the new changes. As it does.

Using `git branch -a` or `git branch --all` will show all branches include the remote ones.

To remove a remote branch (namely the info_feedback here) you can do this `git remote prune origin --dry-run`. The dry run shows you what this command will do before you ACTUALLY do it. Dry runs are nice for this in case you are accidentally removing a non-deleted remote branch.

Mine showed this for this example

      Pruning origin
      URL: git@github.com:xRazoo/stormwater-tour.git
      * [would prune] origin/info_feedback

So I continued with the command and ran the non-dry-run `git remote prune origin` since it looked good.

However `git branch -a` still shows a non-remote, local branch named info_feedback

ex:

      bmp-site
      info_feedback
      map_page
    * master
      remotes/origin/HEAD -> origin/master
      remotes/origin/bmp-site
      remotes/origin/map_page
      remotes/origin/master
 
For that non-remote branch you can just do `git branch -d info_feedback` easy as pie.

Outputted this for me:
`Deleted branch info_feedback (was 513fece).`

Another `git branch -a` shows a better list of branches after the delete.

      bmp-site
      map_page
    * master
      remotes/origin/HEAD -> origin/master
      remotes/origin/bmp-site
      remotes/origin/map_page
      remotes/origin/master
