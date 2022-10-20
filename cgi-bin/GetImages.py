#!/var/www/venv/bin/python
import cgitb, cgi
import sys
import pandas as pd
import os
import json

returnData = []

def GetImages():
    # Getting the current work directory (cwd)
    global returnData
    theDir = "/var/www/html/signage/img"
    # r=root, d=directories, f = files
    for r, d, f in os.walk(theDir):
        for file in f:
            if file.endswith((".jpg", ".JPG", ".jfif", ".JFIF", ".jpeg", ".JPEG", ".png", ".PNG")):
                returnData.append(file)
    returnData.sort()


form = cgi.FieldStorage()
if form.getvalue('to_send') is not None:
    from_js = form.getvalue('to_send')
    GetImages()
else:
    from_js = "nothing received"

print('Content-Type: application/json\n\n')
print(json.dumps(returnData))

