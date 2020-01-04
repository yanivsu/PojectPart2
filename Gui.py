from pymongo import MongoClient
from tkinter import  *

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
        print('Your username dose not exist')
        return 0
    for document in db:
        id=document['_id']
    print("The user id is: "+str(id))

    if str(id)==("5cf50956e3cb94889e658755"):
        userType="Admin"
        print(userType)
        WelcomePage(userType,prevFrame)

    if str(id)==("593462243aa2ad1100b17605"):
        userType="Lecturer"
        print(userType)
        WelcomePage(userType,prevFrame)

    if str(id)==("593462243aa2ad1100b17606"):
        userType="Student"
        print("the user type is: "+userType)
        WelcomePage(userType,prevFrame)

def createAdminsFrame(userType,prevFrame):
    welcomeAdminFrame = Frame(loginScrren)
    currentFrame = welcomeAdminFrame
    welcomeAdminFrame.pack()
    labelUserID = Label(welcomeAdminFrame, bg="green", fg="White", text="HI " + userType).pack()
    spaceLabel = Label(welcomeAdminFrame, text="").pack()
    texbox = Text(welcomeAdminFrame, height=2, width=11).pack()
    spaceLabel = Label(text="")
    signOutButton = Button(welcomeAdminFrame, height=1, width=10, text="Sign-out",
                           command=lambda: createLoginFrame(prevFrame,currentFrame)).pack()

def createLecturerFrame(userType,prevFrame):
    welcomeLecturerFrame = Frame(loginScrren)
    currentFrame = welcomeLecturerFrame
    welcomeLecturerFrame.pack()
    labelUserID = Label(welcomeLecturerFrame, bg="blue", fg="White", text="HI " + userType).pack()
    spaceLabel = Label(welcomeLecturerFrame, text="").pack()
    # texbox = Text(welcomeLecturerFrame, height=2, width=11).pack()

    #  spaceLabel = Label(text="").pack()
    createButton = Button(welcomeLecturerFrame, height=1, width=20, text="Create Test").pack()

    # spaceLabel = Label(text="").pack()
    viewButton = Button(welcomeLecturerFrame, height=1, width=20, text="View test results").pack()

    # spaceLabel = Label(text="").pack()
    requestButton = Button(welcomeLecturerFrame, height=1, width=20, text="Send request for report").pack()
    signOutButton = Button(welcomeLecturerFrame, height=1, width=10, text="Sign-out",
                           command=lambda: createLoginFrame(prevFrame,currentFrame)).pack()

def createStudentsFrame(userType,prevFrame):
    welcomeStudentFrame = Frame(loginScrren)
    currentFrame = welcomeStudentFrame
    welcomeStudentFrame.pack()
    labelUserID = Label(welcomeStudentFrame, bg="grey", fg="White", text="HI " + userType).pack()
    spaceLabel = Label(welcomeStudentFrame, text="").pack()
    # texbox = Text(welcomeStudentFrame, height=2, width=11).pack()
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
    loginScrren.title("Login page")

    loginFrame=Frame(loginScrren)
    loginFrame.pack()
    labelUserID=Label(loginFrame,text="Enter user ID").pack()
    spaceLabel=Label(loginFrame,text="").pack()
    textBox=Text(loginFrame,height=2,width=11)
    textBox.pack()
    spaceLabel = Label(loginFrame,text="").pack()
    nextButton=Button(loginFrame, height=1, width=10, text="Login",
                      command=lambda: GetUserID(textBox,loginFrame)).pack()
    loginScrren.mainloop()

client = MongoClient('mongodb://admin:matanman@ds031822.mongolab.com:31822/admin?authSource=setstudy')
StartPage()