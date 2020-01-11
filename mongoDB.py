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
        return document['resultsB'][int(roundNumber)]['round']
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
        roundStartTime = document['resultsB'][int(roundNumber)]['roundStartTime']
        totalTimeRound = document['resultsB'][int(roundNumber)]['timeToSubmit']
        success = document['resultsB'][int(roundNumber)]['success']
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
    #  roundStartTime = dataPerRound[0]+(timedelta(seconds=20))  Im not sure if its correct line
    roundStartTime = dataPerRound[0]
    roundLength = dataPerRound[1]  # [1] is delta for round length
    roundEndTime = roundStartTime + timedelta(seconds=roundLength)
    roundEndTime = roundEndTime.time()
    roundStartTime = roundStartTime.time()
    strFile = username
    strFile += '_'
    strFile += dataPerRound[0].date().strftime("%d%m%y")
    strFile += '.txt'
    try:
        f = open(strFile, "r")
        print('Tobii file load successfully')
    except:
        print("File dont exist in DB please check you DB")
        return
    #  Jump the first Line
    f = f.readlines()[2:]
    for line in f:
        tempLine = line.split()
        timeTemp = tempLine[2]
        print(line)
        timeTemp = datetime.strptime(timeTemp, '%H:%M:%S').time()
        if (timeTemp >= roundStartTime and timeTemp <= roundEndTime):
            xCor.append(tempLine[0])
            yCor.append(tempLine[1])
        if (timeTemp > roundEndTime):
            break
    return (xCor, yCor)
def DominatValue(username, roundNumber):
    #  [3] => Number of elements
    #  [2] => Color of elements
    #  [1] => Fill of elements
    #  [0] => Shape of elements
    #  Example of roundID = 5d66bc413ace1114004b0731
    numberElements = [0, 0, 0]  # [0] => 1 element , [1] => 2 elements , [2] => 3 elements
    colorElements = [0, 0, 0]   # [0] => Red , [1] => Green , [2] => Purple
    fillElements  = [0, 0, 0]   # [0] => Empty, [1] => Full fill , [2] => Strips
    shapeElements = [0, 0, 0]   # [0] => Diamond , [1] => Circle , [2] => Wave
    dominantArray = [0, 0, 0, 0]
    dominantFlag = -1
    numberInArray = 0
    maxDominant = 0;
    cardsList = GetBoard(username=username, roundNumber=roundNumber)
    for card in cardsList:
        numberElements[int(cardsList[card][3])] += 1
        colorElements[int(cardsList[card][2])] += 1
        fillElements[int(cardsList[card][1])] += 1
        shapeElements[int(cardsList[card][0])] += 1
    for i in range(3):
        if (numberElements[i] > 4 and numberElements[i] > maxDominant):
            dominantFlag = 3
            maxDominant = numberElements[i]
            numberInArray = i
            dominantArray[0] += 1
        if (colorElements[i] > 4 and colorElements[i] > maxDominant):
            dominantFlag = 2
            numberInArray = i
            maxDominant = colorElements[i]
            dominantArray[1] += 1
        if (fillElements[i] > 4 and fillElements[i] > maxDominant):
            dominantFlag = 1
            numberInArray = i
            maxDominant = fillElements[i]
            dominantArray[1] += 1
        if (shapeElements[i] > 4 and shapeElements[i] > maxDominant):
            dominantFlag = 0
            numberInArray = i
            maxDominant = shapeElements[i]
            dominantArray[1] += 1
    if (dominantFlag > -1):
        if(dominantFlag == 3):
            print('The most common value is array is Number: ', numberInArray + 1)
        if (dominantFlag == 2):
            print('The most common value is array is Color: ')
            if(numberInArray == 0):
                print('Red')
            if(numberInArray == 1):
                print('Green')
            if(numberInArray == 2):
                print('Purple')
        if (dominantFlag == 1):
            print('The most common value is array is Fill: ')
            if(numberInArray == 0):
                print('Empty')
            if(numberInArray == 1):
                print('Full fill')
            if(numberInArray == 2):
                print('Strips')
        if (dominantFlag == 0):
            print('The most common value is array is Shape: ')
            if(numberInArray == 0):
                print('Diamond')
            if(numberInArray == 1):
                print('Circle')
            if(numberInArray == 2):
                print('Wave')
    else:
        print('There is no dominant value')
        return False
    return GetdominantCardArray(dominantArray, cardsList, numberInArray, dominantFlag)
def GetdominantCardArray(dominantArray, cardsList, numberInArray, dominatFlag):
    dominantCardArray = []
    for card in cardsList:
        if(int(cardsList[card][dominatFlag]) == numberInArray):
            dominantCardArray.append(cardsList[card])
    return dominantCardArray

