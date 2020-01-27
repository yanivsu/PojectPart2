from tkinter.ttk import Combobox
from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
import mongoDB as db
import Main as graph
from PIL import  Image,ImageTk


def createLoginFrame(prevFrame,currentFrame):
    forgetFrame=currentFrame
    forgetFrame.forget()
    loginFrame = Frame(loginScrren) ################### we can use loginframe=prevframe#########
    loginFrame.pack()
    labelUserID = Label(loginFrame, text="Enter user ID").pack()
    spaceLabel = Label(loginFrame, text="").pack()
    textBox = Text(loginFrame, height=2, width=11)
    textBox.pack()
    spaceLabel = Label(loginFrame, text="").pack()
    nextButton = Button(loginFrame, height=1, width=10, text="Login",
                        command=lambda: GetUserID(textBox, loginFrame)).pack()
def presentPrevScreen(prevFrame, userType, currentFrame):
    removeFrame=currentFrame
    removeFrame.forget()
def GetUserID(textBox,loginFrame):
    prevFrame=loginFrame
    userType=""
    id=""
    username=textBox.get("1.0", "end-1c")
    if not username:
        print('Your username invalid')
        return 0
    print("the user name is: "+username)

    db = client['setstudy'].get_collection('users').find({'username': username})

    if db.count() == 0:
        messagebox.showinfo("ERROR",'Username do not exist')
        return 0

    for document in db:
        id=document['_id']
        flagType=str(document['type'])
    print("The user id is: "+str(id))

    if flagType=='1':
        userType="Admin"
        print(userType)
        WelcomePage(userType,prevFrame)
    if flagType=='2':
        userType="Lecturer"
        print(userType)
        WelcomePage(userType,prevFrame)
    if flagType=='0':
        userType="Student"
        print("the user type is: "+userType)
        WelcomePage(userType,prevFrame)
def getSelectedGraph(graphSelection,clusterSelection,usersToCluster,username,userRound,dominateFlag,analysisFlag):
    if(graphSelection=="Heat map"):
        graph.HeatMapFunction(username, userRound, dominateFlag, analysisFlag)
    if (graphSelection == "Eye movment speed"):
        graph.SpeedUpEyes(username,userRound)
        #graph.HeatMapFunction(username, userRound, dominateFlag,analysisFlag)
    if (graphSelection == "Point drawing"):
        graph.PointDrawing(username, userRound, dominateFlag)
        #graph.HeatMapFunction(username, userRound, dominateFlag,analysisFlag)
        #Speed var","Speed of eye movement","Speed var with speed of eye movement
    if(clusterSelection=="Speed var"):
        graph.ClusterDataBySpeedVar(usersToCluster)
    if (clusterSelection == "Speed of eye movement"):
        graph.ClusterDataBySpeedFastMovments(usersToCluster)
        #graph.HeatMapFunction(username, userRound, dominateFlag,analysisFlag)
    if (clusterSelection == "Speed var with speed of eye movement"):
        graph.ClusterDataBySpeedAndFastMovmentAVG(usersToCluster)

        #graph.HeatMapFunction(username, userRound, dominateFlag,analysisFlag)

    #if (graphSelection == "Eye movment speed"):
    #if (graphSelection == "Point drawing"):
def CheckLecturerSelection(graphSelection,roundSelection,clusterSelection,usersToCluster,username,domFlag,analysisFlag):
    if graphSelection =="":
        messagebox.showinfo("ERROR", "Please select graph type")
    if roundSelection =="":
        messagebox.showinfo("ERROR", "Please select round to present")
    if clusterSelection=="":
        messagebox.showinfo("ERROR", "Please select cluster attributes")
    if(graphSelection!="" and roundSelection!="" and clusterSelection!=""):
        getSelectedGraph(graphSelection, clusterSelection, usersToCluster, username,roundSelection, domFlag, analysisFlag)
def GetViewDetailsByRequestedID(texbox, prevFrame, getIDButton):
    forgetFrame = prevFrame
    forgetFrame.forget()
    currentFrame = Frame(loginScrren)  ################### we can use loginframe=prevframe#########
    currentFrame.pack()
    spaceLabel = Label(currentFrame, text="").pack()

    instructionLabel = Label(currentFrame,text="Select values to present",font='Arial 14 bold')
    instructionLabel.pack()
    spaceLabel = Label(currentFrame, text="").pack()
    #(currentFrame, text="").pack()
    username = texbox.get("1.0", "end-1c")
    usersToCluster = ['user1', 'user2', 'user4', 'user5', 'user7', 'user8']
    print("the reqursted id is: " + username)
    #getIDButton.pack_forget()
    numberOfRounds = db.GetNumberOfRoundByUsername(username)
    numberOfRoundArray = []
    for i in range(numberOfRounds):
        numberOfRoundArray.append(i+1)

    roundsLabel = Label(currentFrame, text=username+" rounds").pack()
    var = IntVar()
    var2 = IntVar()
    roundsComboBox = Combobox(currentFrame, values = numberOfRoundArray)
    roundsComboBox.pack()
   # spaceLabel = Label(currentFrame, text="").pack()
    graphSelectionLabel = Label(currentFrame, text="Choose your graph type").pack()
    graphSelectionComboBox = Combobox(currentFrame,
                                      values=["Heat map", "Eye movment speed", "Point drawing"])
    graphSelectionComboBox.pack()
    #spaceLabel = Label(currentFrame, text="").pack()
    clusterSelectionLabel = Label(currentFrame, text="Choose clustering attributes").pack()
    clusterSelectionComboBox = Combobox(currentFrame,
                                      values=["Speed var","Speed of eye movement","Speed var with speed of eye movement"])
    clusterSelectionComboBox.pack()
    spaceLabel = Label(currentFrame, text="").pack()
    checkBoxButton=Checkbutton(currentFrame,text="Show dominate cards",variable=var)
    checkBoxButton.pack()
    checkBoxButton2=Checkbutton(currentFrame,text="Show analysis ",variable=var2)
    #checkBoxButton2.pack()
    spaceLabel = Label(currentFrame, text="").pack()
    next=Button(currentFrame,text="Get graph",
                command=lambda: CheckLecturerSelection(
                graphSelectionComboBox.get(),(int(roundsComboBox.get())-1),clusterSelectionComboBox.get(),usersToCluster,
                username,var.get(),var2.get()))
    next.pack()
    spaceLabel = Label(currentFrame, text="").pack()

    prevButton = Button(currentFrame, text="    Back    ",
                  command=lambda: CreateViewFrame(currentFrame))
    prevButton.pack()
def createAdminsFrame(userType,prevFrame):
    welcomeAdminFrame = Frame(loginScrren)
    currentFrame = welcomeAdminFrame
    welcomeAdminFrame.pack()
    labelUserID = Label(welcomeAdminFrame, text="Enter requested id: " + userType).pack()
    spaceLabel = Label(welcomeAdminFrame, text="").pack()
    texbox = Text(welcomeAdminFrame, height=2, width=11).pack()
    spaceLabel = Label(text="")
    signOutButton = Button(welcomeAdminFrame, height=1, width=10, text="Sign-out",
                           command=lambda: createLoginFrame(prevFrame,currentFrame)).pack()
def CreateViewFrame(prevFrame):
    forgetFrame=prevFrame
    forgetFrame.forget()
    viewFrame=Frame(loginScrren)
    viewFrame.pack()
    currentFrame=viewFrame
    spaceLabelgert = Label(viewFrame, text="").pack()
    spaceLabelgert = Label(viewFrame, text="").pack()
    labelUserID = Label(viewFrame, fg="black", text="Enter candidates name",font='bold').pack()
    spaceLabelgert = Label(viewFrame, text="").pack()
    texbox = Text(viewFrame, height=2, width=11)
    texbox.pack()
    spaceLabelgert = Label(viewFrame, text="").pack()
    getIDButton = Button(viewFrame, height=1, width=10, text="Get details",
                 command=lambda: GetViewDetailsByRequestedID(texbox,viewFrame,getIDButton))
    getIDButton.pack()

def createLecturerFrame(userType,prevFrame):
    welcomeLecturerFrame = Frame(loginScrren)
    currentFrame = welcomeLecturerFrame
    welcomeLecturerFrame.pack()
    spaceLabel = Label(welcomeLecturerFrame, text="").pack()
    spaceLabel = Label(welcomeLecturerFrame, text="").pack()
    spaceLabel = Label(welcomeLecturerFrame, text="").pack()
    labelUserID = Label(welcomeLecturerFrame,text="Welcome " + userType,font='bold').pack()
    spaceLabel = Label(welcomeLecturerFrame, text="").pack()
    viewButton = Button(welcomeLecturerFrame, height=1, width=20,
                          text="View test results",
                          command=lambda: CreateViewFrame(currentFrame)).pack()
    spaceLabel = Label(welcomeLecturerFrame, text="").pack()

    signOutButton = Button(welcomeLecturerFrame, height=1, width=10,
                           text="Sign-out",
                           command=lambda: createLoginFrame(prevFrame,currentFrame)).pack()
def createStudentsFrame(userType,prevFrame):
    welcomeStudentFrame = Frame(loginScrren)
    currentFrame = welcomeStudentFrame
    welcomeStudentFrame.pack()
    labelUserID = Label(welcomeStudentFrame, bg="grey", fg="White", text="HI " + userType).pack()
    spaceLabel = Label(welcomeStudentFrame, text="").pack()
    texbox = Text(welcomeStudentFrame, height=2, width=11).pack()
    spaceLabel = Label(welcomeStudentFrame,text="").pack()
    startTestButton = Button(welcomeStudentFrame, height=1, width=10, text="Start test",).pack()
    spaceLabel = Label(welcomeStudentFrame,text="").pack()
    signOutButton = Button(welcomeStudentFrame, height=1, width=10, text="Sign-out",
                        command=lambda: createLoginFrame(prevFrame,currentFrame)).pack()
    spaceLabel = Label(welcomeStudentFrame,text="",).pack()
def WelcomePage(userType,prevFrame):
    forgetFrame=prevFrame
    forgetFrame.forget()

    if(userType=="Admin"):
        createAdminsFrame(userType,prevFrame)
    if (userType == "Lecturer"):
        createLecturerFrame(userType,prevFrame)
    if (userType == "Student"):
        createStudentsFrame(userType,prevFrame)
def StartPage():
    global loginScrren
    loginScrren=Tk()
    loginScrren.geometry("300x350")
    loginScrren.title("Set game analyzer")
    signOutFram=Frame(loginScrren)
    signOutFram.pack(side=BOTTOM)
    loginFrame=Frame(loginScrren)
    loginFrame.pack()
    spaceLabel = Label(loginFrame, text="").pack()
    spaceLabel = Label(loginFrame, text="").pack()
    spaceLabel = Label(loginFrame, text="").pack()
    labelUserID=Label(loginFrame, text="Enter user ID",font='bold').pack()
    spaceLabel=Label(loginFrame, text="").pack()
    textBox=Text(loginFrame, height=2, width=11)
    textBox.pack()
    spaceLabel = Label(loginFrame, text="").pack()
    nextButton=Button(loginFrame, height=1, width=10, text="Login",
                      command=lambda: GetUserID(textBox, loginFrame)).pack()
    loginScrren.mainloop()
client = MongoClient('mongodb://admin:matanman@ds031822.mongolab.com:31822/admin?authSource=setstudy')
StartPage()
