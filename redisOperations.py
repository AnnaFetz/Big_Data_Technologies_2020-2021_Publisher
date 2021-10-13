from redis import StrictRedis
import redis
from datetime import datetime

#hostname = 'bdt2021.redis.cache.windows.net'
#access = 'm47NcmWesLSpCwA2DagnRuCVFnrevw5YImMkFSfGgnM='
#r = redis.StrictRedis(host=hostname,
#        port=6380, db=0, password=access, ssl=True)

# def writeToRedis(ts, prediction):
#        r.set(ts, prediction)

# def readRedis(ts):
#         r.get(ts)

def deleteRedis(obj):
    keys = obj.keys()
    for key in keys:
        obj.delete(key)
        
def printAll(obj):
    for key in obj.scan_iter():
        print(key)
    
def getAll(obj):
    allValues = []
    for key in obj.keys():
        value = obj.get(key)   
        print(value)
        allValues.append(value)
    return allValues
        
def getAllKeyValuePairs(obj):
    dic = dict()
    for key in obj.keys():
        value = obj.get(key)   
        print("{}:{}".format(key,value))
        dic[key] = value
    return dic

def getLastValue(obj):
    keys = obj.keys()
    last_key = keys[-1]
    last_value = int(obj.get(last_key))
    last_key = float(last_key)
    return last_key, last_value

def getSortedKeyValuePairs(obj, convString):
    dic = dict()
    for key in obj.keys():
        value = int(obj.get(key))
        if(convString):
            if(value == 0):
                value = "Sell"
            elif(value == 1):
                value = "Buy"
#        print("{}:{}".format(key,value))
        dic[datetime.fromtimestamp(float(key)).strftime("%Y-%m-%d %H:%M")] = value
    a = dic.items()
    sort = sorted(a)
    return sort

def getLastPrediction(obj):
    sort = getSortedKeyValuePairs(obj, False)
    lastPrediction = int(sort[len(sort)-1][1])
    lastUpdate = sort[-1][0]
    return lastUpdate, lastPrediction

def getLastPreds(obj, n = 10):
    l = getSortedKeyValuePairs(obj, True)
    l = l[-n:] 
    return l


    
