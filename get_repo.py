from github import Github
import sys
import pickle


#creating a GitHub object
url = input("Enter url: ")
github = Github()

repo = github.get_repo(url)

with open('repo.pkl', 'wb') as output:
    pickle.dump(repo, output, pickle.HIGHEST_PROTOCOL)