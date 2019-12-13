from pymongo import MongoClient
from bson.objectid import ObjectId
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
