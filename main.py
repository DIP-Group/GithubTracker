from github import Github
from datetime import datetime
import matplotlib.pyplot as plt

#DENEME

#creating a GitHub object
github = Github()
#repo = github.get_repo("maidis/mythes-tr")

#taking repository data from Github, need to enter 
#repository owner/repository name
#repo = github.get_repo("aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE")

repo = github.get_repo("iperov/DeepFaceLab")
#repo = github.get_repo("commaai/openpilot") 


open_issues = repo.get_issues(state='open')
close_issues = repo.get_issues(state='closed')

#total open issues and closed issues
total_opened_issues = open_issues.totalCount
total_closed_issues = close_issues.totalCount



#creating Open Issues-Closed Issues Graph.
fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['Opened Issues','Closed Issues']
metric = [total_opened_issues,total_closed_issues]
ax.bar(langs,metric)
ax.set_title('Issue Numbers')
plt.show() 



print("Opened ones:")
counter=1
opened_time_taken_total = 0
assignee = 0
opened_assignee_no=0
comment_no=0
opened_total_comments = 0
try:
    #taking open issues' data.
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
except:
    print("Exception occured while taking open issues")

    
#creating has assignee-No assignee graph for open issues.
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
try:
    #taking closed issues' data.
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
except:
    print("Exception occured while taking closed issues")
        
    
print("\n\n\nTotal opened issues: ",total_opened_issues)
print("Total closed issues: ",total_closed_issues)

difference = total_opened_issues-total_closed_issues
if difference>0:
    print("Difference between closed and opened issues: ",difference)
else:
    print("Difference between closed and opened issues: ",difference*(-1))

print("\nIssue number that has assignee: ",opened_assignee_no)
print("Issue number that has NO assignee: ",total_opened_issues -opened_assignee_no)   
print("Total comment no for opened issues: ",opened_total_comments)
try:
    avg_opened_comments = opened_total_comments/total_opened_issues
    print("Average comment no for opened issues: ",avg_opened_comments)
except:
    print("Division by zero because of 0 issues!")
    
    
print("\n")    
print("Total time for opened issues(from creating time to today): ",opened_time_taken_total)
print("Average time for opened issues: ",opened_time_taken_total/total_opened_issues) 
print("\n")  
print("Total time for closed issues(from creating time to closing time): ",closed_time_taken_total)
print("Average time for closed issues: ",closed_time_taken_total /total_closed_issues)  
#creating has assignee-No assignee graph for closed issues.
fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['HAS assignee','NO assignee']
metric = [closed_assignee_no,total_closed_issues -closed_assignee_no]
ax.bar(langs,metric)
ax.set_title('Closed Issued')
plt.show()



print("\nIssue number that has assignee for closed issues: ",closed_assignee_no)
print("Issue number that has NO assignee for closed issues: ",total_closed_issues - closed_assignee_no)  
print("Total comment no for closed issues: ",closed_total_comments)
avg_closed_comments = closed_total_comments/total_closed_issues
print("Average comment no for closed issues: ",avg_closed_comments)


#creating average comment number graph
fig = plt.figure()
ax = fig.add_axes([1,1,1,1])
langs = ['Opened Issues','Closed Issues']
metric = [avg_opened_comments,avg_closed_comments]
ax.bar(langs,metric)
ax.set_title('Average comment number')
plt.show()

open_milestones = repo.get_milestones(state='open')
close_milestones = repo.get_milestones(state='closed')
try:
    total_time_open_milestones = open_milestones.totalCount
    total_time_closed_milestones = close_milestones.totalCount
    print("\nOpen milestone number: ",open_milestones.totalCount)



    total_due_time = 0
    for milestone in open_milestones:
        try:
            due_time = milestone.due_on - milestone.created_at
            total_due_time += due_time.days
            print("Title: ",milestone.title,"Due Date: ", milestone.due_on," Total Time(total time given for milestone): ",due_time)
        except:
            print("Due time does not exist")
        
        
    try:    
        avg_due_time = total_due_time / open_milestones.totalCount
        print("Average due time for open milestones: ",avg_due_time)    
        
        
        print("\nClosed milestone number: ",close_milestones.totalCount)
        
        for milestone in close_milestones:
            time_taken_close_milestone = milestone.due_on() - milestone.created_at 
            print("Title: ",milestone.title,"Due Date: ","Due time(Total time given NOT CLOSING TIME):", time_taken_close_milestone.due_on)
        
        fig = plt.figure()
        ax = fig.add_axes([1,1,1,1])
        langs = ['Opened Milestones','Closed Milestones']
        metric = [total_time_open_milestones,total_time_closed_milestones]
        ax.bar(langs,metric)
        ax.set_title('Milestone Numbers')
        plt.show()
    
    except:
        print("Zero division because of 0 milestone!")
except:
    print("Exception occured while taking milestones")
    
