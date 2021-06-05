import csv
from flask import json
import pandas as pd
import os

def parseCSV(filePath):
    jsonArray = []
    #read csv file
    with open(filePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 
        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
    jsonArray = clean_incosistent(jsonArray)
    return jsonArray

def clean_incosistent(jsonArray):
    for header,_ in jsonArray[0].items():
        emp=[]
        for i in range(len(jsonArray)):
            tmp=jsonArray[i][header]
            try:
                float(tmp)
            except:
                emp.append(i)
        if emp:
            if (len(emp)*2)<=len(jsonArray):
                emp.reverse()
                for i in range(len(emp)):
                    jsonArray.pop(emp[i])
    return jsonArray