import main_page
import result_page
from github import Github
from datetime import datetime
import matplotlib.pyplot as plt
import csv 
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from result_page import second_page_dialog
# Önemli toplantı notları

# Export olayı önemli alınacak inputları düzenle
# Export ta export edilecek bilgileri class altında toplayıp csv fonksiyonuna objeyi atıp yapabiliriz.
# Her bir class altında issue bilgileri milestone bilgileri Repo adı gibi bilgileri tut 
# Her bir repo için bir table olacak 
# Table da seçilen metriclerin gösterilmesi gerekiyor
# İleride diğer Repolar da eklenecek bunu planlayıp düzenlenecek...

# Show butonu ile max 5 tane itemin graphını göster 
# Export butonu ekle bu export butonunda sınır olmayacak ve basılırsa direkt veriyi export edecek
# Show butonuna listenin zunluğunu sınırlayacak if statement koy if(len(list)>5) ise mesela göseterme (pop up eror gelicek )
# Eğer karşılaştırma yoksa tek değerse graph gösterme (not applicable)

# Metricleri Difference şeklinde almaya odaklanmalıyız:
# Difference between issues Has assignee and no assigneee
# Difference between the number of ıssues with assignee and without assignee
# Difference between issues with comment and without comment

# Issue metrics:
    #0: Total Opened Isues
    #1: Total Closed Issues
    #2: Dıfference between opened and closed issues
    #3: Distrubution of issues on contributors
    #4: Number of label types
    #5: Label usage frequency
    #6: Total amount of contributors
    #7: Total number of assignees on spesific issue
    #8: Total number of comments
    #9: Avg. Comment Lenght
    #10: Label colors for default Spesic titles
    #11: Mean time to response the issues.
    
# Milesotne metrics:
    #Total amount of Milestones
    #Total Opened Milestones
    #Total Closed Milestones

""""    
for item in list :
  if(item=="Total Opened Isues"):
    list2.append(0)
  elif(item=="Total Closed Issues"):
    list2.append(1)

"""


#issues={'Issue_type':[],'issue_number':[],'İssue_Title':[],'time_taken':[],'assignee':[],'comment_no':[]}  


# class Issue_list():
#     def __init__(self,open_issue_list,close_issue_list,total_issue_list):
#         self.open_issue_list=open_issue_list
#         self.close_issue_list=close_issue_list
#         self.total_issue_list=total_issue_list
#     def append_open_issue(self,open_issue):
#         self.open_issue_list.append(open_issue)
#     def append_close_issue(self,close_issue):
#         self.close_issue_list.append(close_issue)
#     def calculate_total_list(self,open_issue_list,close_issue_list):
#         temp=[] 
#         temp.append(open_issue_list)
#         temp.append(close_issue_list)
#         self.total_issue_list= temp
        
# Issue_list= Issue_list([],[],[])     

# Repo Export bilgileri:
class Repository():
  def __init__(self):
    self.total_opened_issues=0
    self.total_closed_issues=0
    self.total_issue_number=0




open_issues = []
close_issues = []
total_issues = []        
#Gets a dictionary list and export a csv file
def export_csv(list):
    #In order to write in csv format we are establishing connection 
    with open('Output.csv', mode='w',newline='') as file:
        Output_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Empty list for header and colum values
        header_list=[]
        values_list=[]
        
        # Gets the header for the table
        for header in list[0].keys():
            header_list.append(header)
        
        writer = csv.DictWriter(file, fieldnames=header_list)
        writer.writeheader()
        
        # Writes the column values
        for element in list:
            value=element.values()
            for i in value:
                values_list.append(i)
            Output_writer.writerow(values_list)
            values_list=[]
        
def get_repo(repo_url):
    #creating a GitHub object
    github = Github()
    #repo = github.get_repo("maidis/mythes-tr")
    
    #taking repository data from Github, need to enter 
    #repository owner/repository name
    #repo = github.get_repo("aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE")
    
    #repo = github.get_repo("iperov/DeepFaceLab")
    #repo = github.get_repo("commaai/openpilot")
    repo = github.get_repo(repo_url)
    return repo



# Plotları ayır(draw_plot)
# Output dictionary formatlarını ayarla ve nasıl return edicekler onu belirle
# Csv formatını tekrar ayarla 

def get_issue_metrics(repo,s_date,e_date):
    global open_issues
    global close_issues
    global total_issues
    open_issues = repo.get_issues(state='open')
    close_issues = repo.get_issues(state='closed')
    #total open issues and closed issues
    temp =[]
    temp.append(open_issues)
    temp.append(close_issues)
    total_issues = temp
    # Issue_list.append_open_issue(open_issues)
    # Issue_list.append_close_issue(close_issues)
    temp2=[]
    
    for issues in open_issues:
        if(s_date <= issues.created_at):
            temp2.append(issues)
    open_issues = temp2
    
    temp2 = []
    for issues in close_issues:
        if((e_date >= issues.closed_at) and (s_date <= issues.created_at)):
            temp2.append(issues)
    close_issues = temp2
    
    total_opened_issues=0
    for i in open_issues:
        total_opened_issues+=1
    
    total_closed_issues=0
    for i in close_issues:
        total_closed_issues+=1
    
    Repo.total_closed_issues=total_closed_issues
    Repo.total_opened_issues=total_opened_issues
    Repo.total_issue_number=total_closed_issues+total_opened_issues

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
    #issues={'issue_number':[],'İssue_Title':[],'time_taken':[],'assignee':[],'comment_no':[]}
    issue_list=[]
    issue_number=1
    #taking open issues' data.
    try:
        for issue in open_issues:
            time_taken = datetime.today() - issue.created_at
            opened_time_taken_total += time_taken.days
            assignee = issue.assignee
            if assignee != None:
                opened_assignee_no += 1
            comment_no= issue.comments
            opened_total_comments += comment_no
            #issues['issue_number':issue_number,'time_taken':time_taken,'assignee':assignee,'comment_no':comment_no]
            #issue_list.append(issues)
            #export_csv(issue_list) 
            print(counter," - ",issue.title,":",assignee,",",time_taken,"Comment no: ",comment_no)
            counter +=1
            issue_number+=1
    except:
        print("Exception occured while taking open issues' metrics")
    
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
        print("\n")    
        print("Total time for opened issues(from creating time to today): ",opened_time_taken_total)
        print("Average time for opened issues: ",opened_time_taken_total/total_opened_issues) 
        print("\n")  
        print("Total time for closed issues(from creating time to closing time): ",closed_time_taken_total)
        print("Average time for closed issues: ",closed_time_taken_total /total_closed_issues) 
        print("\nIssue number that has assignee for closed issues: ",closed_assignee_no)
        print("Issue number that has NO assignee for closed issues: ",total_closed_issues - closed_assignee_no)  
        print("Total comment no for closed issues: ",closed_total_comments)
        avg_closed_comments = closed_total_comments/total_closed_issues
        print("Average comment no for closed issues: ",avg_closed_comments)
    except:
        print("Division by zero because of 0 milestones!")
        
         
    #creating has assignee-No assignee graph for closed milestones.
    fig = plt.figure()
    ax = fig.add_axes([1,1,1,1])
    langs = ['HAS assignee','NO assignee']
    metric = [closed_assignee_no,total_closed_issues -closed_assignee_no]
    ax.bar(langs,metric)
    ax.set_title('Closed Issued')
    plt.show()
    
    
def get_milestone_metrics(repo):
    
    open_milestones = repo.get_milestones(state='open')
    close_milestones = repo.get_milestones(state='closed')
    open_milestones_list=[]
    closed_milestones_list = []
    total_open_milestones = 0
    total_closed_milestones = 0
    total_due_time = 0
    try:
        for milestone in open_milestones:
            open_milestones_list.append(milestone)
            total_open_milestones += 1
            due_time = milestone.due_on - milestone.created_at
            total_due_time += due_time.days
            print("Title: ",milestone.title,"Due Date: ", milestone.due_on," Total Time(total time given for milestone): ",due_time)
  
        avg_due_time = total_due_time / total_open_milestones
        print("Average due time for open milestones: ",avg_due_time)    
    except:
        print("Exception occured while taking open milestones!")
        
    try:
        for milestone in close_milestones:
            closed_milestones_list.append(milestone)
            total_closed_milestones += 1
            time_taken_close_milestone = milestone.due_on() - milestone.created_at 
            print("Title: ",milestone.title,"Due Date: ","Due time(Total time given NOT CLOSING TIME):", time_taken_close_milestone.due_on)
    except:
        print("Exception occured while taking closed milestones")
        
    fig = plt.figure()
    ax = fig.add_axes([1,1,1,1])
    langs = ['Opened Milestones','Closed Milestones']
    metric = [total_open_milestones ,total_closed_milestones]
    ax.bar(langs,metric)
    ax.set_title('Milestone Numbers')
    plt.show()

        
#It checks repo labels generally, and then determines which labels are used opened and closed issues seperately. 
def get_label(repo):
  labelName = []
  labelColor = []
  labelValuesOpened = []
  labelValuesClosed = []


  for label in repo.get_labels():
      labelName.append(label.name)
      labelColor.append(label.color)
      labelValuesOpened.append(0)
      labelValuesClosed.append(0)

  for issue in open_issues:
      #print("{} - labels {} ".format(count, issue.get_labels()))
      open_labels = issue.get_labels()
      for label in open_labels:
          count = 0
          count = labelColor.index(label.color)
          labelValuesOpened[count] += 1

  count = 0
  for member in labelValuesOpened:
      if member != 0:
          print("Between opened issues, {} ({}) label is used {} times.".format(labelName[count],labelColor[count],labelValuesOpened[count]))
      count += 1


  for issue in close_issues:
      open_labels = issue.get_labels()
      for label in open_labels:
          count = 0
          count = labelColor.index(label.color)
          labelValuesClosed[count] += 1
  count = 0
  for member in labelValuesClosed:
      if member != 0:
          print("Between closed issues, {} ({}) label is used {} times.".format(labelName[count],labelColor[count],labelValuesClosed[count]))
      count += 1


def get_issue_creators(repo):
  #It gives who opened and closed issues and comprasion with contributers.
  contrArray = []
  openedIssueUserArray = [] 

  repo_contributors = repo.get_contributors()
  for repo_contributor in repo_contributors:
      if repo_contributor.id not in contrArray:
          contrArray.append(repo_contributor.id)

  contr_num = len(contrArray)
  if contr_num > 1:
      print("\nThere are {} contributors for this repo.".format(contr_num))
  #elif contr_num == 1:
      #print("\nThere is one contributors for this repo as named ",contr_array[0])
  else:
      print("\nThere is NO contributors for this repo yet.")

  contr_issue = 0
  contr_not_issue = 0
  not_contr_but_issue = 0
  openedIssueUser = 0

  for issue in open_issues:
      opened_issue_user = issue.user
      if opened_issue_user.id not in openedIssueUserArray:
          openedIssueUserArray.append(opened_issue_user.id)
          contr_temp = opened_issue_user.id
          
          if (opened_issue_user.id in openedIssueUserArray) and (contr_temp in contrArray):
              contr_issue += 1
          if(opened_issue_user.id in openedIssueUserArray) and (contr_temp not in contrArray):
              not_contr_but_issue += 1
      
          openedIssueUser = len(openedIssueUserArray)
      contr_not_issue = len(set(contrArray) - set(openedIssueUserArray))

  print("{} of these contributors have opened issues before".format(contr_issue))
  print("{} of these contributors have NOT opened issues before".format(contr_not_issue))  
  print("Although {} people are not contributors, they have opened issue.".format(not_contr_but_issue))
  print("Issues opened by {} different people".format(openedIssueUser))      


  contr_issue = 0
  contr_not_issue = 0
  not_contr_but_issue = 0
  closedIssueUser = 0
  closedIssueUserArray = [] 

  for issue in close_issues:
      closed_issue_user = issue.user
      if closed_issue_user.id not in closedIssueUserArray:
          closedIssueUserArray.append(closed_issue_user.id)
          contr_temp = closed_issue_user.id
          
          if (closed_issue_user.id in closedIssueUserArray) and (contr_temp in contrArray):
              contr_issue += 1
          if(closed_issue_user.id in closedIssueUserArray) and (contr_temp not in contrArray):
              not_contr_but_issue += 1
      
          closedIssueUser = len(closedIssueUserArray)
      contr_not_issue = len(set(contrArray) - set(closedIssueUserArray))

  print("\n{} of these contributors have closed issues before".format(contr_issue))
  print("{} of these contributors have NOT closed issues before".format(contr_not_issue))  
  print("Although {} people are not contributors, they have closed issue.".format(not_contr_but_issue))
  print("Issues closed by {} different people".format(closedIssueUser))  


def parse_url(ui):
    url = ui.url
    repo_url =url.split('/')
    print(repo_url)
    if(len(repo_url)<5 or len(repo_url)>5):
        raise (Exception("Sorry, İnvalid Url PLease enter the url of the main github page..."))
    repo_url = repo_url[3]+'/'+ repo_url[4]
    return  repo_url

def main():
    """ repo_url= input("Please enter the Repository name:")
    repo_url =repo_url.split('/')
    print(repo_url)
    if(len(repo_url)<5 or len(repo_url)>5):
        raise (Exception("Sorry, İnvalid Url PLease enter the url of the main github page..."))
    repo_url = repo_url[3]+'/'+ repo_url[4]
    #Start and finish time 
    start_date = input('Enter a date in DD/MM/YYYY format')
    s_date = datetime.strptime(start_date, '%d/%m/%Y')
    print(type(s_date))
    
    end_date = input('Enter a date in DD/MM/YYYY format')
    e_date = datetime.strptime(end_date, '%d/%m/%Y') """
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui =main_page.Ui_Dialog()
   
    ui.setupUi(Dialog)
    ui.Get_Ui(Dialog)
    Dialog.show()

    repo_url = parse_url(ui)
    print(repo_url)



    repo = get_repo(repo_url)
    get_issue_metrics(repo,s_date,e_date)      
    get_milestone_metrics(repo)

    sys.exit(app.exec_())
    
    



Repo=Repository()
 
if __name__=="__main__":
    main()