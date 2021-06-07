import csv

def checkIfItemExist(jsonArray, item):
    keys = list(jsonArray[0].keys())
    count = 0
    for i in jsonArray:
        for key in keys:
            if(i[key] != item[key]):
                break
            else:
                count += 1
        if(count == len(keys)):
            return True
        count = 0
    return False

def convertCSV (filepath):
    jsonArray = []
    #read csv file
    with open(filepath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    
    return removeInconsistentData(jsonArray)

def removeInconsistentData(jsonArray):
    keys = list(jsonArray[0].keys())
    for key in keys:
        length = len(jsonArray)
        temp = []
        othertemp = [] 
        for i in range (length):
            try:
                data = float(jsonArray[i][key])
                othertemp.append(jsonArray[i])
            except ValueError:  
                # print('masuk error di', jsonArray[i][key])
                temp.append(jsonArray[i])
        # remove num value
        if len(temp) > len(othertemp):
            jsonArray = temp.copy()
        elif (len(temp) > 0):
            jsonArray = othertemp.copy()
        temp.clear()
        othertemp.clear()
    return jsonArray
