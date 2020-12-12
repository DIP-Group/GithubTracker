from github import Github
from datetime import datetime
import matplotlib.pyplot as plt

    
    
github = Github()
#repo = github.get_repo("maidis/mythes-tr")

repo = github.get_repo("rocky-linux/rocky")
open_issues = repo.get_issues(state='open')
close_issues = repo.get_issues(state='closed')


total_opened_issues = open_issues.totalCount
total_closed_issues = close_issues.totalCount


fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['Opened Issues','Closed Issues']
metric = [total_opened_issues,total_closed_issues]
ax.bar(langs,metric)
ax.set_title('Issue Numbers')
plt.show()


print("Total opened issues: ",total_opened_issues)
print("Opened ones:")
counter=1
opened_time_taken_total = 0
assignee = 0
opened_assignee_no=0
comment_no=0
opened_total_comments = 0
for issue in open_issues:
    time_taken = datetime.today() - issue.created_at
    opened_time_taken_total += time_taken.days
    assignee = issue.assignee
    if assignee != None:
        opened_assignee_no += 1
    comment_no= issue.comments
    opened_total_comments += comment_no
    print(counter," - ",issue.title,":",assignee,",",time_taken,"Comment no: ",comment_no)
    counter +=1
    
print("\nIssue number that has assignee: ",opened_assignee_no)
print("Issue number that has NO assignee: ",total_opened_issues -opened_assignee_no)   
print("Total comment no for opened issues: ",opened_total_comments)
avg_opened_comments = opened_total_comments/total_opened_issues
print("Average comment no for opened issues: ",avg_opened_comments)

fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['HAS assignee','NO assignee']
metric = [opened_assignee_no,total_opened_issues -opened_assignee_no]
ax.bar(langs,metric)
ax.set_title('Opened Issued')

plt.show()

print("\n\n")

counter=1
closed_time_taken_total = 0
closed_assignee_no=0
closed_total_comments = 0
print("Closed ones:")
print("Total closed issues: ",total_closed_issues)
for issue in close_issues:
    time_taken = issue.closed_at - issue.created_at
    closed_time_taken_total += time_taken.days
    assignee = issue.assignee
    if assignee != None:
        closed_assignee_no += 1
    comment_no= issue.comments
    closed_total_comments += comment_no
    print(counter," - ",issue.title,":",assignee,",",time_taken,"Comment no: ",comment_no)
    counter +=1
    
fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['HAS assignee','NO assignee']
metric = [closed_assignee_no,total_closed_issues -closed_assignee_no]
ax.bar(langs,metric)
ax.set_title('Closed Issued')
plt.show()



print("\nIssue number that has assignee: ",closed_assignee_no)
print("Issue number that has NO assignee: ",total_closed_issues - closed_assignee_no)  
print("Total comment no for closed issues: ",closed_total_comments)
avg_closed_comments = closed_total_comments/total_closed_issues
print("Average comment no for closed issues: ",avg_closed_comments)

fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['Opened Issues','Closed Issues']
metric = [avg_opened_comments,avg_closed_comments]
ax.bar(langs,metric)
ax.set_title('Average comment number')
plt.show()


print("\n")    
print("Total time for opened issues: ",opened_time_taken_total)
print("Average time for opened issues: ",opened_time_taken_total/total_opened_issues) 
print("\n")  
print("Total time for closed issues: ",closed_time_taken_total)
print("Average time for closed issues: ",closed_time_taken_total /total_closed_issues)  
difference = total_opened_issues-total_closed_issues
if difference>0:
    print("Difference between closed and opened issues: ",difference)
else:
    print("Difference between closed and opened issues: ",difference*(-1))
    
open_milestones = repo.get_milestones(state='open')
print("\nOpen milestone number: ",open_milestones.totalCount)
total_due_time = 0
for milestone in open_milestones:
    due_time = milestone.due_on -milestone.created_at
    total_due_time += due_time.days
    print("Title: ",milestone.title,"Due Date: ", milestone.due_on," Total Time: ",due_time)
    
    
avg_due_time = total_due_time / open_milestones.totalCount
print("Average due time for open milestones: ",avg_due_time)    
close_milestones = repo.get_milestones(state='closed')

print("\nClosed milestone number: ",close_milestones.totalCount)

for milestone in close_milestones:
    print("Title: ",milestone.title,"Due Date: ", milestone.due_on)

fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['Opened Milestones','Closed Milestones']
metric = [open_milestones.totalCount,close_milestones.totalCount]
ax.bar(langs,metric)
ax.set_title('Milestone Numbers')
plt.show()
