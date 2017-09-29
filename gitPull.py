import os
import git

import config

branch = "master"
if config.gitDev:
    branch = "development"

o = git.Repo.clone_from("https://github.com/Ravenholdt/Discord-Imitator.git" , os.path.dirname(os.path.abspath(__file__)), branch=branch)
