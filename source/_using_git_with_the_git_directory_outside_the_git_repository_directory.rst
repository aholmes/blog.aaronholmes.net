Using Git with the .git directory outside the Git repository directory
======================================================================

19 August 2016

I have a particular use case where I want to use Git on top of another version control system. The only problem I ran into is that the other VCS wanted to track the .git directory that Git creates for its own tracking purposes.

Rather than mess about with making the existing VCS ignore this directory, I set out to make Git store the .git directory somewhere else. Turns out it's pretty easy, but Git is fickle, and you have to set a couple environment variables rather than simply using ``--git-dir`` or ``--work-tree``.

The bash script below creates a function named ``git`` in your environment that shells out to the real Git binary. It will also attempt to create a new directory in your home directory (``~/gitdirs``) to hold these new ``.git`` directories. This script also works in Git Bash!

.. code-block:: bash

    # Store a reference to the Git binary
    GIT_BIN=`which git`

    # The function that runs when you type `git`
    function git  
    {
        # The location .git directories are stored in
        gitdirroot=~/gitdirs
        # Create that directory if it does not exist
        if [ ! -d $gitdirroot ]; then
            mkdir -p $gitdirroot
        fi

        # Use the current working directory as the .git directory name
        gitdirname="$gitdirroot/`pwd | tr "/" '_'`"

        # Set the two environment variables Git needs to use the new .git directory
        export GIT_DIR=$gitdirname
        export GIT_WORK_TREE=.
    }


.. tags:: git, git-bash, bash