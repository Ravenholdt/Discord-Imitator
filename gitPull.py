import os

import config

branch = ""
if config.gitDev:
    branch = "development"

os.system("git pull origin " + branch)