from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta

#  Connect to DB
client = MongoClient('mongodb://admin:matanman@ds031822.mongolab.com:31822/admin?authSource=setstudy')

def GetBoard(username, roundNumber):
    roundID = GetRoundIDByUserName(username=username, roundNumber=roundNumber)
    return GetListOfCardRoundID(roundID=roundID)
def GetListOfCardRoundID(roundID):
    db = client['setstudy'].get_collection('round_projbs').find({'_id': ObjectId(roundID)})
    for doc in db:
        return doc['cards']
def GetRoundIDByUserName(username, roundNumber):
    if not username:
        print('Your username invalid')
        return 0
    db = client['setstudy'].get_collection('users').find({'username': username})
    if db.count() == 0:
        print('Your username dose not exist')
        return 0
    for document in db:
        return document['resultsB'][roundNumber]['round']
def GetNumberOfRoundByUsername(username):
    if not username:
        print('Your username invalid')
        return 0
    db = client['setstudy'].get_collection('users').find({'username': username})
    if db.count() == 0:
        print('Your username dose not exist')
        return 0
    for document in db:
        return document['resultsB'].__len__()
def GetTimeDeatilsPerRound(username, roundNumber):
    startTimeRound = 0
    totalTimeRound = 0
    success = False
    detailsRound = []
    db = client['setstudy'].get_collection('users').find({'username': username})
    if db.count() == 0:
        print('Your username dose not exist')
        return 0
    for document in db:
        roundStartTime = document['resultsB'][roundNumber]['roundStartTime']
        totalTimeRound = document['resultsB'][roundNumber]['timeToSubmit']
        success = document['resultsB'][roundNumber]['success']
    startTimeRound = TimestampConvert(roundStartTime)
    detailsRound.append(startTimeRound)
    detailsRound.append(totalTimeRound)
    detailsRound.append(success)
    return detailsRound
def GetDatesAndTimes(username):
    datesAndTimesArray = []
    if not username:
        print('Your username invalid')
        return 0
    db = client['setstudy'].get_collection('users').find({'username': username})
    if db.count() == 0:
        print('Your username dose not exist')
        return 0
    for document in db:
        for i in range(document['resultsB'].__len__()):
            datesAndTimesArray.append(TimestampConvert(document['resultsB'][i]['roundStartTime']))
    datesOnly = GetUserDates(datesAndTimesArray)
    values = GetUsersRoundsPerDate(datesOnly, datesAndTimesArray)

def GetUserDates(datesAndTimesArray):
    dates = []
    i = 1
    dates.append(datesAndTimesArray[0].date())
    for  i in range(len(datesAndTimesArray)):
        if dates.__contains__(datesAndTimesArray[i].date()):
            print()
        else:
            dates.append(datesAndTimesArray[i].date())
    return dates
def GetUsersRoundsPerDate(datesOnly, datesAndTimesArray):
    matrix = CreateMatrix(datesAndTimesArray, datesOnly)
    for i in range(len(datesOnly)):
        matrix[i][0] = datesOnly[i]
    for i in range(len(datesOnly)):
        for j in range( len(datesAndTimesArray)):
            dateCheck = datesAndTimesArray[j].date()
            if (dateCheck == datesOnly[i]):
               matrix[i][j+1] = j
    return matrix
    roundTimes = GetTimeDeatilsPerRound()
def TimestampConvert(timeS):
    timeS = int(int(timeS) / 1000)
    timeS = datetime.fromtimestamp(timeS)
    return timeS
def CreateMatrix(col, row):
    mat = []
    for i in range(len(row)):
        mat.append([])
    for i in range(len(row)):
        for j in range(len(col)+1):
            mat[i].append(j)
            mat[i][j] = -1
    for i in range(len(row)):
        for j in range(len(col)):
            # mat[i][j] = i * j
            print(mat[i][j])
    return mat
def GetCoordinateByRoundNumber(username, roundNumber):
    xCor = []
    yCor = []
    dataPerRound = GetTimeDeatilsPerRound(username=username, roundNumber=roundNumber)
    roundStartTime = dataPerRound[0]+(timedelta(seconds=20))
    roundLength = dataPerRound[1]  # [1] is delta for round length
    roundEndTime = roundStartTime + timedelta(seconds=roundLength)
    roundEndTime = roundEndTime.time()
    roundStartTime = roundStartTime.time()
    strFile = username
    strFile += dataPerRound[0].date().strftime("%d%m%y")
    strFile += '.txt'
    f = open(strFile, "r")
    #  Jump the first Line
    f = f.readlines()[2:]
    i = 0
    for line in f:
        tempLine = line.split()
        timeTemp = tempLine[2]
        timeTemp = datetime.strptime(timeTemp, '%H:%M:%S').time()
        if (timeTemp >= roundStartTime and timeTemp <= roundEndTime):
            xCor.append(tempLine[0])
            yCor.append(tempLine[1])
        if (timeTemp > roundEndTime):
            break
    return (xCor, yCor)



    return