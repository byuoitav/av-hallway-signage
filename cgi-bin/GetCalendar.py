#!/var/www/venv/bin/python
import cgitb, cgi
import sys
import pandas as pd
import os
import json

returnData = {}
timeOff = {}
projects = {}
def isNaN(num):
    return num!= num

def VerifyCalendar():
    # Getting the current work directory (cwd)
    global returnData
    global timeOff
    global projects
    theDir = '../cgi-bin'
    theFile = ''
    for r, d, f in os.walk(theDir):
        for file in f:
            if file.endswith(("spreadsheet.xlsx")):
                theFile = file
    xls = pd.ExcelFile(theFile)
    df = pd.read_excel(xls, "Weekly Schedule", header=None, nrows=20)
    #print("cell", df.iat[0,0]) #Print a single cell

    dates = df.iloc[2]
    vacation = df.iloc[1]
    installer = df.iloc[4]
    jobs = df.iloc[5]
    notes = df.iloc[6]

    
    #Add dates to columns missing dates
    vacationCount = 0
    installerCount = 0
    newDate = ''
    for i in range(len(dates)):
        if isNaN(dates[i]):
            dates[i] = newDate
        else:
            newDate = dates[i]
            timeOff[dates[i]] = []
            projects[dates[i]] = []
        
        #build vacation dict
        if isNaN(vacation[i]):
            pass
        else:  
            timeOff[dates[i]].append( vacation[i])

        #build project dict    
        if isNaN(jobs[i]):
            jobs[i] = 'Not on Schedule' 
            
        if isNaN(installer[i]):
            pass
        else:  
            projects[dates[i]].append({'installer': installer[i], 'jobs': jobs[i]})

    returnData['timeOff'] = timeOff
    returnData['projects'] = projects
#VerifyCalendar()


form = cgi.FieldStorage()
if form.getvalue('to_send') is not None:
    from_js = form.getvalue('to_send')
else:
    from_js = "nothing received"

if from_js == "verifyCalendar":
    VerifyCalendar()


print('Content-Type: application/json\n\n')
print(json.dumps(returnData))