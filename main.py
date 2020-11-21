from github import Github


g = Github()
repo = g.get_repo("maidis/mythes-tr")
open_issues = repo.get_issues(state='open')
print("Opened ones:")
for issue in open_issues:
    print(issue.created_at)
    
close_issues = repo.get_issues(state='closed')
print("Closed ones:")
for issue in close_issues:
    print(issue.created_at , " - ", issue.closed_at)