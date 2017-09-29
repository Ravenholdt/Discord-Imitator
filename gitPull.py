import os
import git

import config

branch = "master"
if config.gitDev:
    branch = "development"

#o = git.Repo.pull_from("https://github.com/Ravenholdt/Discord-Imitator.git" , os.path.dirname(os.path.abspath(__file__)), branch=branch)

repo = git.Repo("https://github.com/Ravenholdt/Discord-Imitator.git")
o = repo.remotes.origin.development
o.fetch()
