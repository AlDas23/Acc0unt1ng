def ParseCurrRatesNames(data, appendCurr):
    finalList = []
    for row in data:
        date = row[0]
        currency = row[1]
        rate = row[2]
        
        currency = f"{currency}->{appendCurr}"
        finalList.append((date, currency, rate))
    
    return finalList

def AppendToListElements(originalList, appendValue):
    return [f"{item}->{appendValue}" for item in originalList]

def GetCurrentYear():
    from datetime import datetime
    return datetime.now().year