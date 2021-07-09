from tkinter import *
from tkinter import filedialog
from tkinter.font import BOLD
from github import Github
import sys
import pickle
from tkinter import ttk
import os
import re
import statistics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv 
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

color = '#cee4f0'
#color = '#0E6655'

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class EnteringScreen(Frame):
    def __init__(self):
        root = Tk()
        root.minsize(width=350, height=350)
        root.maxsize(width=650, height=500)
        root.configure(bg=color)
        

        Frame.__init__(self)
        self.pack()
        self.master.title("DIP Reasearch Tool")

        self.frame1 = Frame()
        self.frame1.pack()

        URL = "https://i.ibb.co/Nm39ZjD/orginal.png"
        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        im = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(im)

        label = Label(image=photo)
        label.image = photo
        label.config(background = color)
        label.pack()
        
        self.sizeLabel = Label(self.frame1, text="Welcome to DIP Research Tool", font='Helvetica 14 bold')
        self.sizeLabel.config(background = color)
        self.sizeLabel.pack(side=LEFT)

        self.frame2 = Frame()
        self.frame2.pack()

        self.New_Repo_Button = Button(self.frame2, text="Get New Repo",command=Get_New_Repo)
        self.New_Repo_Button.pack(side=LEFT)
        CreateToolTip(self.New_Repo_Button, text = 'The button use for\n'
                 'new repositories from GitHub\n'
                 'and saves as Pickle file automatically')

        self.Load_Repo_Button = Button(self.frame2, text="Load New Repo And Continue",command=lambda :New_load_repo_page(root))
        self.Load_Repo_Button.pack(side=LEFT)
        CreateToolTip(self.Load_Repo_Button, text = 'The button use for\n'
                 'loading repositories from\n'
                 'Pickle file which are saved before')

        self.frame1.place(anchor="c", relx=.5, rely=.37)
        self.frame2.place(anchor="c", relx=.5, rely=.5)


def browseFiles(label_file_explorer):
    global file
    rootdir = os.path.dirname(os.path.abspath(__file__))
    filename = filedialog.askopenfilename(initialdir=rootdir, title="Select a File",
                                          filetypes=(("Pickle files", "*.pkl*"), ("all files", "*.*")))
    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    file=filename

def retrieve_input(textBox):
    global url
    inputValue=textBox.get("1.0","end-1c")
    url = inputValue
    get_repo(url)

def Get_New_Repo():
    window = Tk()
    # Set window title
    window.title('Get Repo')

    # Set window size
    window.geometry("600x300")

    # Set window background color
    window.config(background=color)

    url_field = Text(window, height=2, width=60)
    url_field.pack(pady=40)
    CreateToolTip(url_field, text = 'Write the full URL \n'
                 'of a repository')


    buttonCommit = Button(window, height=1, width=10, text="Get Repo",
                          command=lambda: retrieve_input(url_field))
    # command=lambda: retrieve_input() >>> just means do this when i press the button
    buttonCommit.pack()

    mainloop()

def parse_url(url):
    new_url = url
    repo_url = new_url.split('/')
    print(repo_url)
    if (len(repo_url) < 5 or len(repo_url) > 5):
        raise (Exception("Sorry, İnvalid Url PLease enter the url of the main github page..."))
    repo_url = repo_url[3] + '/' + repo_url[4]
    print(repo_url)
    return repo_url

def get_repo(url):
    new_url=parse_url(url)
    github = Github()

    repo = github.get_repo(new_url)

    name=repo.name
    name = str(name)

    with open(name+'.pkl', 'wb') as output:
        pickle.dump(repo, output, pickle.HIGHEST_PROTOCOL)

def load_repo_from_file(file):
    with open(file, 'rb') as config_dictionary_file:
        # Step 3
        repo = pickle.load(config_dictionary_file)

    return repo

def draw_scatter_chart(tab, labels, sizes):
    figure = plt.figure(facecolor=color, tight_layout=True)
    ax = figure.add_subplot(111).scatter(labels,sizes)
    chart = FigureCanvasTkAgg(figure, tab)
    chart.get_tk_widget().pack(side="right", fill="both", expand=True)
    plt.grid()
    
def box_plot(tab,labels,sizes):
    figure = plt.figure(facecolor=color, tight_layout=True)
    ax = figure.add_subplot(111).boxplot(sizes)
    chart = FigureCanvasTkAgg(figure, tab)
    chart.get_tk_widget().pack(side="right", fill="both", expand=True)
    plt.grid()


def draw_line_chart(tab, labels, sizes):
    figure = plt.figure(facecolor=color, tight_layout=True)
    ax = figure.add_subplot(111).plot(labels,sizes)
    
    chart = FigureCanvasTkAgg(figure, tab)
    chart.get_tk_widget().pack(side="right", fill="both", expand=True)
    
    plt.grid()


def draw_pie_chart(tab, labels, sizes):

    figure = plt.figure(facecolor=color, tight_layout=True)
    ax = figure.add_subplot(111)

    ax.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    canvas = FigureCanvasTkAgg(figure, tab)
    canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    plt.grid()
    

def draw_bar_chart(tab, labels, sizes):
    figure = plt.figure(facecolor=color, tight_layout=True)
    #ax = figure.add_axes([1,1,1,1])
    ax = figure.add_subplot(111)
    arr = []
    ax.bar(labels,sizes)
    canvas = FigureCanvasTkAgg(figure, tab)
    canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    plt.grid()

def write_result(tab, label, size):
    Label(tab, text=str(label) + "\n" + str(size), fg="black", font=("Helvetica",40, BOLD), bg=color).pack(side="left",fill="both",expand=True)

    #figure = plt.figure(figsize = (5,4), dpi = 100, facecolor=color, tight_layout=True)
    #figure.add_subplot(111).plot(data)
    #chart = FigureCanvasTkAgg(figure, tab)
    #chart.get_tk_widget().grid(row = 5, column = 0)
    
    #plt.grid()
    """
    axes = plt.axes()
    axes.set_xlim([0, 6.3])
    axes.set_ylim([-3, 3])
    """
    """
    plt.bar(0, data)
    plt.title(title)

    plt(tab,width='50', height='23', selectmode='extended')
    """



def write_answers(root):
    global answers_list

    root.title('Question Answers')
    root.geometry('600x300')
    root['bg']=color

    tv = ttk.Treeview(root)
    tv['columns']=('Questions', 'Answers')
    tv.column('#0', width=0, stretch=NO)
    tv.column('Questions', anchor=CENTER, width=250)
    tv.column('Answers', anchor=CENTER, width=15)

    tv.heading('#0', text='', anchor=CENTER)
    tv.heading('Questions', text='Questions', anchor=CENTER)
    tv.heading('Answers', text='Answers', anchor=CENTER)

    counter = 0
    for answer in answers_list:
        tv.insert(parent='', index=counter, iid=counter, text='', values=(answer[0],answer[1]))
        counter += 1
    tv.pack(side="right", fill="both", expand=True)
    root.mainloop()




def calculate_metrics(Repo):
    global selectionArray
    #print(Repo.name)
    window = Tk()

    # Set window title
    window.title('Calculation Results')

    # Set window size
    window.geometry("800x600")

    # Set window background color
    window.config(background=color)


    tabControl = ttk.Notebook(window)

    style = ttk.Style() 
    style.configure('tabb.TFrame', background=color, foreground=color)
    """    
    style = ttk.Style() 
    style.configure('.',background=color)
    """
    global answers_list
    answers_list = []
    open_issues = Repo.get_issues(state='open')
    closed_issues = Repo.get_issues(state='closed')


    for item in selectionArray:
        # Rate limiti azaltmak için Repo.open_issues_count() kullanılabilir (direkt open issue sayısını dönüyor / Closed issue için de kullanılabilir)
        
        if (item == "Total Opened Issues"):
            Total_open_issues=[]
            for issue in open_issues:
                Total_open_issues.append(issue.title)
            
            tab1 = ttk.Frame(tabControl, style='tabb.TFrame')
            tabControl.add(tab1, text='Opened issues')
            #labels = ["Total Opened Issues"]
            #sizes = [len(Total_open_issues)]
            write_result(tab1, item, len(Total_open_issues))
            #draw_bar_chart(tab1, labels, sizes)
            print("Opened issues : {}".format(len(Total_open_issues)))
            answers_list.append([item, len(Total_open_issues)])
        
        elif (item == "Total Closed Issues"):
            Total_closed_issues=[]
            for issue in closed_issues:
                Total_closed_issues.append(issue.title)
            tab2 = ttk.Frame(tabControl)
            tabControl.add(tab2, text='Closed issues')
            #labels = ["Total Closed Issues"]
            #sizes = [len(Total_closed_issues)]
            write_result(tab2, item, len(Total_closed_issues))
            #draw_bar_chart(tab2, labels, sizes)
            print("Closed issues : {}".format(len(Total_closed_issues)))
            answers_list.append([item, len(Total_closed_issues)])
        
        elif (item == "Difference between opened and closed issues"):
            temp = []
            Total_open_issues=[]
            Total_closed_issues=[]
            for issue in open_issues:
                Total_open_issues.append(issue)
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            temp = abs(len(Total_open_issues)-len(Total_closed_issues))

            tab3 = ttk.Frame(tabControl)
            tabControl.add(tab3, text='Difference O/C')
            labels = ["Total open issues: "+str(len(Total_open_issues)), "Total close issues: "+str(len(Total_closed_issues))]
            sizes = [len(Total_open_issues), len(Total_closed_issues)]
            draw_pie_chart(tab3, labels, sizes)
            print("Difference between opened and closed issues : {}".format(temp))
            answers_list.append([item, temp])

        elif (item == "Distribution score of issues on contributors"):
            contrArray = []
            openedIssueUserArray = [] 
            repo_contributors = Repo.get_contributors()
            for repo_contributor in repo_contributors:
                if (repo_contributor,0) not in contrArray:
                    contrArray.append([repo_contributor,0])
            Total_issues=[]
            for issue in open_issues:
                Total_issues.append(issue)
            for issue in closed_issues:
                Total_issues.append(issue)

            for issue in Total_issues:
                for cont in contrArray:
                    if(cont[0] in issue.assignees):
                        cont[1] += 1
            sample = []
            for cont in contrArray:
                sample.append(cont[1])

            stdeviation = statistics.stdev(sample)
            meann = statistics.mean(sample)
            
            result = stdeviation/meann


            tab4 = ttk.Frame(tabControl)
            tabControl.add(tab4, text='Dist issues on contributors')
            labels = []
            sizes = []
            for cont in contrArray:
                """
                strr = str(cont[0])
                labels.append(str(strr.split("'")))
                """
                labels.append(str(re.findall('"([^"]*)"', str(cont[0]))))
                sizes.append(int(cont[1]))
            draw_bar_chart(tab4, labels, sizes)
            print("Distribution score of issues on contributors: {0:.3f}".format(result))
            """
            for cont in contrArray:
                print("Name: {} Contributed issue number: {}".format(cont[0],cont[1]))
            """
            answers_list.append([item, result])

        elif (item == "Number of label types"):
            control1 = 0
            control2 = 0
            defaultLableSet = ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix"]
            labelName = []
            for label in Repo.get_labels():
                labelName.append(label.name)
            for tempLabel in labelName:
                if tempLabel not in defaultLableSet:
                    control1 = control1 + 1
                else:
                    control2 = control2 + 1
            
            tab5 = ttk.Frame(tabControl)
            tabControl.add(tab5, text='Number of label types')

            labels = ["In Default Set: "+str(control2), "NOT In Default Set: "+str(control1)]
            sizes = [control2, control1]
            draw_pie_chart(tab5, labels, sizes)

            labels = ["Number of label types: "+str(control2+control1)]
            sizes = [control2+control1]
            #draw_bar_chart(tab5, labels, sizes)
            print("Number of label types: {}\n{} of them are in default set, {} of them are NOT in default set.".format(control1+control2, control2, control1))
            answers_list.append([item, control1+control2])


        elif (item == "Label usage frequency"):
            labelName = []
            labelCount = 0
            Total_issues=[]
            for issue in open_issues:
                Total_issues.append(issue)
            for issue in closed_issues:
                Total_issues.append(issue)

            for issue in Total_issues:
                total_labels = issue.get_labels()
                for label in total_labels:
                    if(label != None):
                        labelCount += 1
            totalIssues = len(Total_issues)

            tab6 = ttk.Frame(tabControl)
            tabControl.add(tab6, text='Label usage frequency')
            
            labels = ["Used Labels for All Issues: "+str(labelCount), "NOT Used Labels for All Issues: "+str(totalIssues - labelCount)]
            sizes = [labelCount, totalIssues - labelCount]
            draw_pie_chart(tab6, labels, sizes)

            print("Label usage frequency: %{}\nTotal issues {}, labels are used {} times.".format(int((labelCount/totalIssues)*100),totalIssues,labelCount))
            control = totalIssues/2
            answers_list.append([item, int((labelCount/totalIssues)*100)])
            
        
        elif (item == "Total amount of contributors"):
            contrArray = []
            openedIssueUserArray = [] 
            repo_contributors = Repo.get_contributors()
            for repo_contributor in repo_contributors:
                if repo_contributor.id not in contrArray:
                    contrArray.append(repo_contributor.id)
            contr_num = len(contrArray)
            if contr_num > 1:
                print("Total amount of contributors: {}".format(contr_num))
            else:
                print("\nThere is NO contributors for this repo yet.")
            
            tab7 = ttk.Frame(tabControl)
            tabControl.add(tab7, text='Total amount of contributors')

            #labels = ["Total amount of contributors"]
            #sizes = [contr_num]
            write_result(tab7, item, contr_num)
            #draw_bar_chart(tab7, labels, sizes)
            answers_list.append([item, contr_num])


        elif (item == "Total number of assignees on specific Repo"):
            issues=Repo.get_issues()
            assignee = []
            for item in issues:
                x = item.assignees
                for member in x:
                    assignee.append(member)
            assignee = len(list(dict.fromkeys(assignee)))
            print("Total number of assignee is: {}".format(assignee))

            tab8 = ttk.Frame(tabControl)
            tabControl.add(tab8, text='Total number of assignees')

            #labels = ["Total number of assignees"]
            #sizes = [assignee]
            write_result(tab8, item, assignee)
            #draw_bar_chart(tab8, labels, sizes)
            answers_list.append([item, assignee])


        elif (item == "Total number of comments"):
            open_total_comments = 0
            closed_total_comments = 0
            for issue in open_issues:
                comment_no = issue.comments
                open_total_comments += comment_no
            comment_no = 0
            for issue in closed_issues:
                comment_no= issue.comments
                closed_total_comments += comment_no
            print("Total number of comments: {}".format(open_total_comments + closed_total_comments))

            tab9 = ttk.Frame(tabControl)
            tabControl.add(tab9, text='Total number of comments')

            #labels = ["Total number of comments"]
            #sizes = [open_total_comments + closed_total_comments]
            write_result(tab9, item, open_total_comments + closed_total_comments)
            #draw_bar_chart(tab9, labels, sizes)
            answers_list.append([item, open_total_comments + closed_total_comments])


        elif (item == "Avg. Comment Length"):
            total = 0
            temp_comment = 0
            count = 0
            labels = []
            sizes = []
            for issue in Repo.get_issues():
                comments = issue.get_comments()
                temp = 0
                counter = 0
                for comment in comments:
                    for character in comment.body:
                        temp = temp + 1
                    
                    counter = counter + 1
                    labels.append(counter)
                    print(counter)
                    sizes.append(temp)
                    print(temp)
                    
                if temp != 0:
                    temp_comment = temp_comment + temp/counter
                else:
                    temp_comment = 0
                count = count + 1
            total = temp_comment/count
            print("Avg. Comment Lenght: {}".format(total))

            tab10 = ttk.Frame(tabControl)
            tabControl.add(tab10, text='Avg. Comment Length')

            box_plot(tab10,labels,sizes)
            answers_list.append([item, total])


        elif (item == "Total number of used labels"):
            Total_issues = []
            labelTwins = []
            for issue in open_issues:
                Total_issues.append(issue)
            for issue in closed_issues:
                Total_issues.append(issue)
            for issue in Total_issues:
                labels = issue.get_labels()
                for label in labels:
                    labelTwins.append((label.name))
            print("Total number of used labels: {}".format(len(labelTwins)))

            tab11 = ttk.Frame(tabControl)
            tabControl.add(tab11, text='Total number of used labels')

            #labels = ["Total number of used labels"]
            #sizes = [len(labelTwins)]
            write_result(tab11, item, len(labelTwins))
            #draw_bar_chart(tab11, labels, sizes)
            answers_list.append([item, len(labelTwins)])

        # Mean time i Gün bazında hesaplıyor (Mean Response u Issue nün oluşturulduğu tarihten en son update edildiği zamana kadar alıyorum (Acaba kapatıldığı güne kadar mı alınmalı))
        elif (item == "Mean time to response the issues."):
            Total_closed_issues=[]
            response_time = []
            labels = []
            sizes = []
            Mean_response = 0
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            counter = 1
            for issue in Total_closed_issues:
                created=issue.created_at
                updated = issue.updated_at
                closed = issue.closed_at
                response = updated-created
                duration = closed - created
                response_time.append(response)
                labels.append(counter)
                counter += 1
            for x in response_time:
                Mean_response = Mean_response + x.days
                sizes.append(x.days)
            Mean_response = Mean_response/len(response_time)
            print("Mean time to response the issues: {}".format(Mean_response))

            tab12 = ttk.Frame(tabControl)
            tabControl.add(tab12, text='Mean time to response the issues')

            #labels = ["Mean time to response the issues"]
            #sizes = [Mean_response]
            #draw_bar_chart(tab12, labels, sizes)
            box_plot(tab12, labels, sizes)
            answers_list.append([item, Mean_response])


        elif (item == "Total amount of Milestones"):
            open_milestones = Repo.get_milestones(state='open')
            close_milestones = Repo.get_milestones(state='closed')
            open_milestones_list=[]
            closed_milestones_list = []
            for milestone in open_milestones:
                open_milestones_list.append(milestone)           
            for milestone in close_milestones:
                closed_milestones_list.append(milestone)
            print("Total amount of Milestones: {}".format(len(open_milestones_list) + len(closed_milestones_list)))

            tab13 = ttk.Frame(tabControl)
            tabControl.add(tab13, text='Total amount of Milestones')

            labels = ["Total amount of Milestones"]
            sizes = [len(open_milestones_list) + len(closed_milestones_list)]
            #draw_bar_chart(tab13, labels, sizes)

            labels = ["Total Opened Milestones: "+str(len(open_milestones_list)),"Total Closed Milestones: "+str(len(closed_milestones_list))]
            sizes = [len(open_milestones_list), len(closed_milestones_list)]
            draw_pie_chart(tab13, labels, sizes)
            answers_list.append([item, len(open_milestones_list) + len(closed_milestones_list)])

        elif (item == "Total Opened Milestones"):
            open_milestones = Repo.get_milestones(state='open')
            open_milestones_list=[]
            for milestone in open_milestones:
                open_milestones_list.append(milestone)
            print("Total Opened Milestones: {}".format(len(open_milestones_list)))

            tab14 = ttk.Frame(tabControl)
            tabControl.add(tab14, text='Total Opened Milestones')

            #labels = ["Total Opened Milestones"]
            #sizes = [len(open_milestones_list)]
            write_result(tab14, item, len(open_milestones_list))
            #draw_bar_chart(tab14, labels, sizes)
            answers_list.append([item, len(open_milestones_list)])

        elif (item == "Total Closed Milestones"):
            close_milestones = Repo.get_milestones(state='closed')
            closed_milestones_list = []
            for milestone in close_milestones:
                closed_milestones_list.append(milestone)
            print("Total Closed Milestones: {}".format(len(closed_milestones_list)))

            tab15 = ttk.Frame(tabControl)
            tabControl.add(tab15, text='Total Closed Milestones')

            #labels = ["Total Closed Milestones"]
            #sizes = [len(closed_milestones_list)]
            write_result(tab15, item, len(closed_milestones_list))
            #draw_bar_chart(tab15, labels, sizes)
            answers_list.append([item, len(closed_milestones_list)])

        else:
            print("Error...")
        
        tabControl.pack(expand=1, fill="both")



def calculate_questions(Repo):
    global selectionArray
    #print(Repo.name)
    window = Tk()

    # Set window title
    window.title('Question Answers')

    # Set window size
    window.geometry("800x600")

    # Set window background color
    window.config(background=color)


    tabControl = ttk.Notebook(window)

    style = ttk.Style() 
    style.configure('tabb.TFrame', background=color, foreground=color)
    """    
    style = ttk.Style() 
    style.configure('.',background=color)
    """
    global answers_list
    answers_list = []

    print(Repo.name)
    open_issues = Repo.get_issues(state='open')
    closed_issues = Repo.get_issues(state='closed')

    for item in selectionArray:
        if (item == "Are labels used for issue management?"):
            labelName = []
            labelCount = 0
            Total_open_issues=[]
            Total_closed_issues=[]
            for issue in open_issues:
                Total_open_issues.append(issue)
            
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            
            total_issues = Total_open_issues + Total_closed_issues
            for issue in total_issues:
                total_labels = issue.get_labels()
                for label in total_labels:
                    if(label != None):
                        labelCount += 1
            totalIssues = len(total_issues)
            print("Total issues {}, labels are used {} times / Labels not used {} times.".format(totalIssues,labelCount,totalIssues-labelCount))
            control = totalIssues/2
            
            """
            tab1 = ttk.Frame(tabControl)
            tabControl.add(tab1, text=item)
            """

            if labelCount >= control:
                answer = "Yes, labels are important for this repository."
                print(answer)
                #write_result(tab1, item, answer)
                answers_list.append([item, "Yes"])
            else:
                answer = "No, labels are NOT important for this repository."
                print(answer)
                #write_result(tab1, item, answer)
                answers_list.append([item, "No"])

        elif (item == "Is the default set of labels sufficient for issue management?"):
            control = 0
            defaultLableSet = ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix"]
            labelName = []
            for label in Repo.get_labels():
                labelName.append(label.name)
            for tempLabel in labelName:
                if tempLabel not in defaultLableSet:
                    control = control + 1
            """
            tab2 = ttk.Frame(tabControl)
            tabControl.add(tab2, text=item)
            """    
            if control > 0:
                answer = "No, default set of labels is NOT sufficient for issue management"
                print(answer)
                #write_result(tab2, item, answer)
                answers_list.append([item, "No"])
            else:
                answer = "Yes, default set of labels is sufficient for issue management"
                print(answer)
                #write_result(tab2, item, answer)
                answers_list.append([item, "Yes"])

        
        elif (item == "Is every contributor active in issue management?"):
            """
            tab3 = ttk.Frame(tabControl)
            tabControl.add(tab3, text=item)
            """
            open_issue_comment_writer = []
            open_issue_contributors = []
            closed_issue_comment_writer = []
            closed_issue_contributors = []
            all_issue_comment_writer = []
            all_issue_contributors = []
            
            
            for issue in open_issues:
                for comment in issue.get_comments():
                    open_issue_comment_writer.append(comment.user.login)
            
            for issue in open_issues:
                open_issue_contributors.append(issue.user.login)
                
            for issue in closed_issues:
                for comment in issue.get_comments():
                    closed_issue_comment_writer.append(comment.user.login)
            
            for issue in closed_issues:
                open_issue_contributors.append(issue.user.login)
                
            all_issue_comment_writer.extend(open_issue_comment_writer)    
            all_issue_comment_writer.extend(closed_issue_comment_writer)
            all_issue_contributors.extend(open_issue_contributors)
            all_issue_contributors.extend(closed_issue_contributors)
            print(all_issue_comment_writer)
            print(all_issue_contributors)
            answer = ""
            for i in all_issue_contributors:
                flag = 0
                for j in all_issue_comment_writer:
                    if(i==j):
                        flag=1
                if(flag==0):
                    answer = "No, not every contributor active in issue management"
                    #write_result(tab3, item, answer)
                    answers_list.append([item, "No"])
                    break
                    
            if(answer==""):
                answer = "Yes, every contributor active in issue management"
                #write_result(tab3, item, answer)
                answers_list.append([item, "Yes"])

        elif (item == "Is the responsibility of opening and closing issues equally distributed among contributors?"):
            tab4 = ttk.Frame(tabControl)
            tabControl.add(tab4, text=item)
            open_issue_openers = []
            closed_issue_openers = []
            all_issue_openers = []
            open_issue_closers = []
            closed_issue_closers = []
            all_issue_closers = []
            all_issue_openers_and_closers = []
            #issue openers
            for issue in open_issues:
                open_issue_openers.append(issue.user.login)

            
            for issue in closed_issues:
                closed_issue_openers.append(issue.user.login)
               
            all_issue_openers.extend(open_issue_openers)
            all_issue_openers.extend(closed_issue_openers)
            total_opening_an_issue = len(all_issue_openers)
            print("opened ones:")
            print(open_issue_openers)
            print("closed ones:")
            print(closed_issue_openers)
            print("alls:")
            print(all_issue_openers)
            unique_list = []
            for x in all_issue_openers:
                if x not in unique_list:
                    unique_list.append(x)
                    
            #issue closers    
            for issue in open_issues:
                if(issue.closed_by!=None):
                    open_issue_closers.append(issue.closed_by.login)

            for issue in closed_issues:
                if(issue.closed_by!=None):
                    closed_issue_closers.append(issue.closed_by.login)
               
            all_issue_closers.extend(open_issue_closers)
            all_issue_closers.extend(closed_issue_closers)
            total_closing_an_issue = len(all_issue_closers)
            print("total closing an issue:",total_closing_an_issue)
            print("opened ones:")
            print(open_issue_closers)
            print("closed ones:")
            print(closed_issue_closers)
            print("alls:")
            print(all_issue_closers)
            for x in all_issue_closers:
                if x not in unique_list:
                    unique_list.append(x)        
                    
            
            number_of_contributors = len(unique_list)
            
            all_issue_openers_and_closers.extend(all_issue_openers)
            all_issue_openers_and_closers.extend(all_issue_closers)
            
            distribution_of_opening_and_closing_issue = (total_opening_an_issue+total_closing_an_issue) / number_of_contributors
            print("distribution_of_opening_and_closing_issue",distribution_of_opening_and_closing_issue)
            
            for contributor in unique_list:
                contribution_count = all_issue_openers_and_closers.count(contributor)
                if(((contribution_count-distribution_of_opening_and_closing_issue)<2) and ((distribution_of_opening_and_closing_issue-contribution_count)<2)):
                    answer = "Yes,the responsibility of opening and closing issues is equally distributed among contributors"
                else:
                    answer = "No,the responsibility of opening and closing issues is NOT equally distributed among contributors" 
                    break
            if(answer=="Yes,the responsibility of opening and closing issues is equally distributed among contributors"):
                write_result(tab4, item, answer)
                answers_list.append([item, "Yes"])
            elif(answer=="No,the responsibility of opening and closing issues is NOT equally distributed among contributors" ):
                write_result(tab4, item, answer)
                answers_list.append([item, "No"])      
            

        elif (item == "Are the life times of the issues consistent?"):
            issues=[]
            duration_list=[]
            for issue in closed_issues:
                created = issue.created_at
                closed = issue.closed_at
                duration = closed - created
                duration_list.append(duration)
            Mean_duration=0
            for x in duration_list:
                Mean_duration = Mean_duration + x.days
            Mean_duration = Mean_duration/len(duration_list)

            # print("=================>")
            # print(f"Mean duration is:{Mean_duration}")
            # print("=================>")

            # We will say that 1 week is our tolerance
            lower_bound = Mean_duration-7
            if(lower_bound<0):
                lower_bound=0
            upper_bound = Mean_duration +7

            # print("=================>")
            # print(f"Lower Bound:{lower_bound}  Upper Bound: {upper_bound}")
            # print("=================>")

            #if %80 of the issues are in this range we will say it is consistent

            count=0
            for i in duration_list:
                #print(f"Days:{float(i.days)}")
                if (float(i.days)>=lower_bound and float(i.days)<=upper_bound):
                    count = count +1
            lenght = len(duration_list)
            # print("=================>")
            # print(f"Ratio:{count/lenght}")
            # print("=================>")
            
            """
            tab5 = ttk.Frame(tabControl)
            tabControl.add(tab5, text=item)
            """
            
            if ((count/lenght)>=0.8):
                answer = "Yes, life times of the issues are consistent for this Repo"
                print(answer)
                #write_result(tab5, item, answer)
                answers_list.append([item, "Yes"])
            else:
                answer = "No, life times of the issues are not consistent for this Repo"
                print(answer)
                #write_result(tab5, item, answer)
                answers_list.append([item, "No"])

        elif (item == "Are the comments made by the contributors equally distributed among contributors?"):
            """
            tab6 = ttk.Frame(tabControl)
            tabControl.add(tab6, text=item)
            """
            open_issue_contributors = []
            closed_issue_contributors = []
            all_issue_contributors = []
            opened_issues_total_comments=0
            closed_issues_total_comments=0
            number_of_total_comment=0
            #calculating total comments
            for issue in open_issues:
                opened_issues_total_comments = opened_issues_total_comments + issue.comments
                
            for issue in closed_issues:
                closed_issues_total_comments = closed_issues_total_comments + issue.comments
                
            number_of_total_comment =  opened_issues_total_comments + closed_issues_total_comments
            
            #calculating contributors
            
            for issue in open_issues:
                open_issue_contributors.append(issue.user.login)
            
            for issue in closed_issues:
                open_issue_contributors.append(issue.user.login)
                
            all_issue_contributors.extend(open_issue_contributors)
            all_issue_contributors.extend(closed_issue_contributors)
            
            unique_list = []
            for x in all_issue_contributors:
                if x not in unique_list:
                    unique_list.append(x)
            
            number_of_contributors = len(unique_list)
            
            distribution_of_comments = number_of_total_comment/number_of_contributors
            
            open_issue_comment_writer = []
            closed_issue_comment_writer = []
            all_issue_comment_writer = []
            
            
            for issue in open_issues:
                for comment in issue.get_comments():
                    open_issue_comment_writer.append(comment.user.login)
            
                
            for issue in closed_issues:
                for comment in issue.get_comments():
                    closed_issue_comment_writer.append(comment.user.login)

                
            all_issue_comment_writer.extend(open_issue_comment_writer)    
            all_issue_comment_writer.extend(closed_issue_comment_writer)
            answer=""
            
            for writer in all_issue_comment_writer:
                count = 0
                for ele in all_issue_comment_writer:
                    if (ele == writer):
                        count = count + 1
                count = count - 1
                if(distribution_of_comments!=count):
                    answer = "No,the comments made by the contributors NOT equally distributed among contributors"
                    print(answer)
                    #write_result(tab6, item, answer)
                    answers_list.append([item, "No"])
                    break
                if(answer!=""):
                    break
            
            if(answer==""):
                answer = "Yes,the comments made by the contributors equally distributed among contributors"
                print(answer)
                #write_result(tab6, item, answer)
                answers_list.append([item, "Yes"])
                    
        
        elif (item == "Is commenting used consistently in all issues?"):
            check = 0
            """
            tab7 = ttk.Frame(tabControl)
            tabControl.add(tab7, text=item)
            """

            for i in open_issues:
                print("Comments: ",i.comments)
                if(i.comments == 0):
                    check = 1
            if(check ==1 ):
                answer = "No, commenting is NOT used consistently in all issues"
                print(answer)
                #write_result(tab7, item, answer)
                answers_list.append([item, "No"])
            else:
                print("Comments: ",i.comments)
                for i in closed_issues:
                    if(i.comments == 0):
                        check = 1
        
                if(check ==1 ):
                    answer = "No, commenting is NOT used consistently in all issues"
                    print(answer)
                    #write_result(tab7, item, answer)
                    answers_list.append([item, "NO"])
                else:
                    answer = "Yes, commenting is used consistently in all issues"
                    print(answer)
                    #write_result(tab7, item, answer)
                    answers_list.append([item, "Yes"])
            

        elif (item == "Are the issues with assigneee completed earlier to compared the ones without assignee?"):
            issue_number=0
            with_assignee=0
            without_assignee=0
            without_assignee_time=0
            with_assignee_time=0
            total_issues = []
            for i in closed_issues:
                #print("Closed: {}, Created: {} çıkarma: {}".format(i.closed_at.timestamp(),i.created_at.timestamp(),(i.closed_at.timestamp()-i.created_at.timestamp())))
                issue_number+=1
                if(i.assignee == None):
                    without_assignee +=1
                    
                    without_assignee_time += (i.closed_at.timestamp() - i.created_at.timestamp())
                else:
                    with_assignee +=1
                    with_assignee_time += i.closed_at.timestamp() - i.created_at.timestamp()
            
            #print("With_assignee_time: {}, without_assignee_time: {}".format(with_assignee_time,without_assignee_time))
            average_with_assignee = with_assignee_time / with_assignee
            average_without_assignee = without_assignee_time / without_assignee
            
            print("Average time with assignee: {}, average time without assignee= {}".format(average_with_assignee,average_without_assignee))

            """
            tab8 = ttk.Frame(tabControl)
            tabControl.add(tab8, text=item)
            """
            if(average_with_assignee > average_without_assignee):
                answer = "No, issues without assignees has been completed earlier"
                print(answer)
                #write_result(tab8, item, answer)
                answers_list.append([item, "No"])
            else:
                answer = "Yes, issues with assignees has been completed earlier"
                print(answer)
                #write_result(tab8, item, answer)
                answers_list.append([item, "Yes"])


        elif (item == "What is the ratio of the opened issues grouped under milestone and those not grouped?"):
            open_issue_number = 0
            with_milestone_number = 0
            without_milestone_nnumber = 0
            
            open_issues_milestone_none = Repo.get_issues(state="open",milestone="none")
            
            for i in open_issues:
                open_issue_number +=1 
            for i in open_issues_milestone_none:
                without_milestone_nnumber +=1
            with_milestone_number = open_issue_number - without_milestone_nnumber
            if(without_milestone_nnumber == 0 and with_milestone_number !=0):
                percentage = 100
            if(without_milestone_nnumber == 0 and with_milestone_number ==0):
                percentage = 0
            if(without_milestone_nnumber != 0):    
                percentage = (with_milestone_number / without_milestone_nnumber) * 100

            """
            tab9 = ttk.Frame(tabControl)
            tabControl.add(tab9, text=item)
            """
            print("Open issue number: {} Open issues without milestones: {} Open issues with milestones: {}".format(open_issue_number, without_milestone_nnumber,with_milestone_number))
            print("Percentage {}".format(percentage))
            #write_result(tab9, item, percentage)
            answers_list.append([item, percentage])


        elif (item == "What does the average time between opening and closing the issue?"):
            Total_closed_issues=[]
            duration = []
            Avg_duration = 0
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            for issue in Total_closed_issues:
                opened = issue.created_at
                closed = issue.closed_at
                temp_duration = closed - opened
                duration.append(temp_duration)
            for x in duration:
                Avg_duration = Avg_duration + x.days
            Avg_duration = Avg_duration/len(Total_closed_issues)
            
            """
            tab10 = ttk.Frame(tabControl)
            tabControl.add(tab10, text=item)
            """
            print("Average time between opening and closing the issue: {}".format(Avg_duration))
            #write_result(tab10, item, Avg_duration)
            answers_list.append([item, Avg_duration])

        elif (item == "What does the average time between opening and closing the milestone?"):
            Total_closed_milestones=[]
            duration = []
            closed_milestones = Repo.get_milestones(state='closed')
            Avg_duration = 0
            for milestone in closed_milestones:
                Total_closed_milestones.append(milestone)
            for issue in Total_closed_milestones:
                opened = milestone.created_at
                closed = milestone.due_on
                temp_duration = closed - opened
                duration.append(temp_duration)
            for x in duration:
                Avg_duration = Avg_duration + x.days
            Avg_duration = Avg_duration/len(Total_closed_milestones)

            """
            tab11 = ttk.Frame(tabControl)
            tabControl.add(tab11, text=item)
            """
            print("Average time between opening and closing the milestone: {}".format(Avg_duration))
            #write_result(tab11, item, Avg_duration)
            answers_list.append([item, Avg_duration])


        elif (item == "Are the comments be posted after the issues are closed or during the process?"):
            open_total_comments = 0
            before_closed_comments = 0
            after_closed_comments = 0
            for issue in open_issues:
                comments = issue.comments
                open_total_comments += comments
            for issue in closed_issues:
                total_closed_comments = issue.comments
                comments2 = issue.get_comments(since=issue.closed_at)
                for comment in comments2:
                    after_closed_comments += len(comment)
                    before_closed_comments += (total_closed_comments - after_closed_comments)

            before_closed_comments += open_total_comments
            """
            tab12 = ttk.Frame(tabControl)
            tabControl.add(tab12, text=item)
            """
            if(before_closed_comments >= after_closed_comments):
                answer = "No, the comments are generally posted during the process for this Repo."
                print(answer)
                #write_result(tab12, item, answer)
                answers_list.append([item, "No"])
            else:
                answer = "Yes, the comments are generally posted after the issues are closed for this Repo."
                print(answer)
                #write_result(tab12, item, answer)
                answers_list.append([item, "Yes"])


        elif (item == "Are the issues grouped under milestone completed earlier compared to the ones not grouped?"):
            Total_milestones=[]
            Total_Issues=[]
            grouped = []
            notgrouped = []

            #opened_issues = Repo.get_issues(state='open')
            opened_milestones = Repo.get_milestones(state='open')
            closed_milestones = Repo.get_milestones(state='closed')

            for milestone in opened_milestones:
                Total_milestones.append(milestone)
            for milestone in closed_milestones:
                Total_milestones.append(milestone)
            """
            for issue in opened_issues:
                Total_Issues.append(issue)
            """
            for issue in closed_issues:
                Total_Issues.append(issue)
            
            for issue in Total_Issues:
                if issue.milestone in Total_milestones:
                    grouped.append(issue)
                else:
                    notgrouped.append(issue)

            grouped_time = 0
            notgrouped_time = 0

            for elem in grouped:
                opened = elem.created_at
                closed = elem.closed_at
                temp_duration = closed - opened
                grouped_time += temp_duration.days
            grouped_time = grouped_time / len(grouped)

            for elem in notgrouped:
                opened = elem.created_at
                closed = elem.closed_at
                temp_duration = closed - opened
                notgrouped_time += temp_duration.days
            notgrouped_time = notgrouped_time / len(notgrouped)
            """
            tab13 = ttk.Frame(tabControl)
            tabControl.add(tab13, text=item)
            """
            if(grouped_time >= notgrouped_time):
                answer = "Yes, the issues grouped under milestone completed earlier compared to the ones not grouped."
                print(answer)
                #write_result(tab13, item, answer)
                answers_list.append([item, "Yes"])
            else:
                answer = "No, the issues not grouped under milestone completed earlier compared to the ones grouped."
                print(answer)
                #write_result(tab13, item, answer)
                answers_list.append([item, "No"])

        else:
            print("Error...")
        
    write_answers(window)
        #tabControl.pack(expand=1, fill="both")


def showSelected_metric(listbox,Repo):
    global selectionArray
    selectionArray = [listbox.get(i) for i in listbox.curselection()]
    calculate_metrics(Repo)
    print_list()

def showSelected_question(listbox,Repo):
    global selectionArray
    selectionArray = [listbox.get(i) for i in listbox.curselection()]
    calculate_questions(Repo)
    print_list()

def print_list():
    global selectionArray
    print(selectionArray)

def export_as_csv(columns, choice):
    global answers_list
    print(answers_list)
    listt = []
    answerx = []
    answery = []
    for item in answers_list:
        answerx.append(item[0])
        answery.append(item[1])

    counter = 0
    for column in columns:
        if column in answerx:
            listt.append(answery[counter])
            counter += 1
        else:
            listt.append("NULL")
    
    if(choice == 1):
        if(os.path.exists('OutputMetrics.csv')):
            values_list=[]
            with open('OutputMetrics.csv', 'a') as file: 
                Output_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for element in listt:
                    values_list.append(element)
                Output_writer.writerow(values_list) 

        else:            
            #In order to write in csv format we are establishing connection 
            with open('OutputMetrics.csv', mode='w',newline='') as file:
                Output_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Empty list for header and colum values
                header_list=[]
                values_list=[]
                
                # Gets the header for the table
                for column in columns:
                    header_list.append(column)
                
                writer = csv.DictWriter(file, fieldnames=header_list)
                writer.writeheader()
                
                # Writes the column values
                for element in listt:
                    values_list.append(element)
                Output_writer.writerow(values_list)
                values_list=[]
    if(choice == 0):
        if(os.path.exists('OutputAnswers.csv')):
            values_list=[]
            with open('OutputAnswers.csv', 'a') as file: 
                Output_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for element in listt:
                    values_list.append(element)
                Output_writer.writerow(values_list) 

        else:            
            #In order to write in csv format we are establishing connection 
            with open('OutputAnswers.csv', mode='w',newline='') as file:
                Output_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Empty list for header and colum values
                header_list=[]
                values_list=[]
                
                # Gets the header for the table
                for column in columns:
                    header_list.append(column)
                
                writer = csv.DictWriter(file, fieldnames=header_list)
                writer.writeheader()
                
                # Writes the column values
                for element in listt:
                    values_list.append(element)
                Output_writer.writerow(values_list)
                values_list=[]
    file.close() 



def New_load_repo_page(root):
    root.destroy()
    main_list = ["Total Opened Issues", "Total Closed Issues", "Difference between opened and closed issues",
                 "Distribution score of issues on contributors", "Number of label types", "Label usage frequency",
                 "Total amount of contributors", "Total number of assignees on specific Repo",
                 "Total number of comments", "Avg. Comment Length", "Total number of used labels",
                 "Mean time to response the issues.", "Total amount of Milestones", "Total Opened Milestones", "Total Closed Milestones"]
    # Create the root window
    questions_list = ["Are labels used for issue management?",
                      "Is the default set of labels sufficient for issue management?",
                      "Is every contributor active in issue management?",
                      "Is the responsibility of opening and closing issues equally distributed among contributors?",
                      "Are the life times of the issues consistent?",
                      "Are the comments made by the contributors equally distributed among contributors?",
                      "Is commenting used consistently in all issues?",
                      "Are the issues with assigneee completed earlier to compared the ones without assignee?",
                      "What is the ratio of the opened issues grouped under milestone and those not grouped?",
                      "What does the average time between opening and closing the issue?",
                      "What does the average time between opening and closing the milestone?",
                      "Are the comments be posted after the issues are closed or during the process?",
                      "Are the issues grouped under milestone completed earlier compared to the ones not grouped?"]
    global file
    window = Tk()

    # Set window title
    window.title('File Explorer')

    # Set window size
    window.geometry("800x600")

    # Set window background color
    window.config(background=color)

    label_file_explorer = Label(window,
                                text="File Explorer using Tkinter",
                                width=115, height=4,
                                fg="blue")
    browseFiles(label_file_explorer)
    label_file_explorer.pack(padx=10, pady=10)
    # label_file_explorer.grid(column=0, row=0)
    print(file)
    # load_repo_from_file(file)
    tabControl = ttk.Notebook(window)
    style = ttk.Style() 
    style.configure('.',background=color)


    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)


    tabControl.add(tab1, text='Metrics')
    tabControl.add(tab2, text='Questions')
    tabControl.pack(expand=1, fill="both")
    
    

    Repo = load_repo_from_file(file)

    listbox1 = Listbox(tab1,width='50', height='23', selectmode='extended')
    

    counter = 1
    for mem in main_list:
        listbox1.insert(counter, mem)
        counter = counter + 1
    listbox1.pack(fill="none", expand=True)
    

    but = Button(tab1, text="Draw Metrics Charts", command=lambda: showSelected_metric(listbox1,Repo))
    but.pack(padx=10, pady=10)
    CreateToolTip(but, text = 'This is for drawing statistics\n'
                 'for each selected metrics above\n'
                 '(for multiple selection press CTRL)')

    but = Button(tab1, text="Export Metrics", command=lambda: export_as_csv(main_list, 1))
    but.pack(padx=10, pady=10)
    CreateToolTip(but, text = 'This is for exporting .csv files\n'
                 'for each selected metrics above\n'
                 '(for multiple selection press CTRL)')



    listbox2 = Listbox(tab2,width='90', height='23', selectmode='extended')
    counter = 1
    for mem in questions_list:
        listbox2.insert(counter, mem)
        counter = counter + 1
    listbox2.pack(fill="none", expand=True)

    but = Button(tab2, text="Answer the Questions", command=lambda: showSelected_question(listbox2,Repo))
    but.pack(padx=10, pady=10)
    CreateToolTip(but, text = 'This is for creating table statistics\n'
                 'for each selected answers above\n'
                 '(for multiple selection press CTRL)')

    but = Button(tab2, text="Export Answers", command=lambda: export_as_csv(questions_list, 0))
    but.pack(padx=10, pady=10)
    CreateToolTip(but, text = 'This is for exporting .csv files\n'
                 'for each selected answers above\n'
                 '(for multiple selection press CTRL)')



    window.mainloop()


file=""
url=""
answers_list = []
selectionArray = []
if __name__ == '__main__':
    MainWindow=EnteringScreen()
    MainWindow.mainloop()
