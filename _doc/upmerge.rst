*************
Upstrem Merge
*************

The process to merge ``ruamel.yaml``'s Mercurial repository to ours is
non-trivial due to non-unique Mergurial-to-git imports and squash merges.

Preparation
===========

We create a git import of the Upstream repository. Then we add a
pseudo-merge node to it which represents our version of the code
at the point where the last merge happened. The commit we want is most
likely named "Upstream 0.xx.yy".

So, first we get a git copy of an HG clone of the ``ruamel.yaml``
repository::

    # install Mercurial (depends on your distribution)

    cd /your/src
    mkdir -p ruyaml/git
    cd ruyaml/git; git init
    cd ../
    hg clone http://hg.code.sf.net/p/ruamel-yaml/code hg

Next we prepare our repository for merging. We need a ``hg-fast-export``
script::

    cd ..
    git clone git@github.com:frej/fast-export.git

We use that script to setup our git copy::

    cd ../git
    ../fast-export/hg-fast-export.sh -r ../hg --ignore-unnamed-heads

Now let's create a third repository for the actual work::

    cd ../
    git clone git@github.com:pycontribs/ruyaml.git repo
    cd repo
    git remote add ../git ruamel
    git fetch ruamel

Create a branch for merging::

    git checkout -b merge main

This concludes setting things up.

Incremental merge
=================

First, let's pull the remote changes (if any)::

    cd /your/src/ruyaml/hg
    hg pull
    cd ../git
    ../fast-export/hg-fast-export.sh -r ../hg --ignore-unnamed-heads
    cd ../repo
    git fetch --all
    git checkout merge

Next, we need a pseudo-merge that declares "we have merged all of Upstream
up to *THAT* into *THIS*", where *THIS* is the latest Merge commit in our
repository (typically named "Upstream 0.xx.yy") and *THAT* is the
corresponding commit in the Ruamel tree (it should be tagged 0.xx.yy)::

    git log --date-order --all --oneline
    git reset --hard THIS
    git merge -s ours THAT

Now we'll "merge" the current Upstream sources::

    git merge --squash ruamel/main

This will create a heap of conflicts, but no commit yet.

.. note::

    The reason we do a squash-merge here is that otherwise git will
    un-helpfully upload the complete history of ``ruamel.yaml`` to GitHub.
    It's already there, of course, but due to the diverging git hashes that
    doesn't help.

The next step, obviously, is to fix the conflicts. (There will be a bunch.)
If git complains about a deleted ``__init__.py``, the solution is to ``git
rm -f __init__.py``.

Then, commit your changes::

    git commit -a -m "Merge Upstream 0.xx.yz"
    git push -f origin merge

Now check github. If everything is OK, congratulations, otherwise fix and
push (no need to repeat the ``-f``).
