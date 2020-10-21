import base64
from github import Github
from pprint import pprint

username = "socodes" #please type the user you want to take repositories'
g = Github()
user = g.get_user(username)
for repo in user.get_repos():
    print(repo)
#-------------------------------------------

repo = g.get_repo("PyGithub/PyGithub")
print(repo.get_issue(number=874))
