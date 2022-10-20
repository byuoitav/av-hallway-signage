#!/var/www/venv/bin/python
from boxsdk import Client, OAuth2
import http.client
import json, os
import requests

appToken = os.environ.get('BOX_AV_SIGNAGE')

def GetImageList():
    conn = http.client.HTTPSConnection("api.box.com")
    payload = ''
    headers = {
    'Authorization': 'Bearer {token}'.format(token = appToken)
    }
    conn.request("GET", "/2.0/folders/177182767655/items", payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonData = json.loads(data)

    #print(json.dumps(jsonData['entries'], indent=4))
    boxFileList = []
    localFileList = []
    boxFileSaveNameList = []

    #get list of files in box
    for f in jsonData['entries']:
        if f['type'] == 'file':
            fileListItem = {}
            fileListItem['id'] = f['id']
            fileListItem['name'] = f['name']
            fileListItem['versionId'] = f['file_version']['id']
            fileListItem['saveName'] = f['id'] + '_' + f['file_version']['id'] + '_' + f['name']
            
            boxFileSaveNameList.append(fileListItem['saveName'])
            boxFileList.append(fileListItem)
    #print(boxFileList)
    
    theDir = "../html/signage/img/"

    #get list of files in local storage
    # r=root, d=directories, f = files
    for r, d, f in os.walk(theDir):
        for file in f:
            if file.endswith((".jpg", ".JPG", ".jfif", ".JFIF", ".jpeg", ".JPEG", ".png", ".PNG", ".txt", ".TXT")):
                localFileList.append(file)

    #delete items not in box
    for item in localFileList:
        if item not in boxFileSaveNameList:
            path = '../html/signage/img/' + item
            if os.path.exists(path):
                os.remove(path)
                print("Removed: " + path)

    #Add items not in local storage from Box to local storage
    for item in boxFileList:
        #print(item['saveName'])
        if item['saveName'] in localFileList:
            #print(item['saveName'])
            pass
        else:
            GetFile(item['id'], item['saveName'], '../html/signage/img/')
            print("Added: " + item['saveName'])
    #print(localFileList)



def GetExcelFile():
    conn = http.client.HTTPSConnection("api.box.com")
    payload = ''
    headers = {
    'Authorization': 'Bearer {token}'.format(token = appToken)
    }
    conn.request("GET", "/2.0/files/890583431547/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonData = json.loads(data)
    saveName = jsonData['id'] + '_' + jsonData['file_version']['id'] + '_' + 'spreadsheet.xlsx'
    #print(saveName)
    theDir = '../cgi-bin'
    needToDownload = False
    for r, d, f in os.walk(theDir):
        for file in f:
            if file.endswith((".xlsx", ".XLSX")):
                if file != saveName:
                    os.remove(file)
                    needToDownload = True
    if needToDownload:                
        GetFile('890583431547', saveName, '../cgi-bin/')
        print("Got new Excel file")


    
            

def GetFile(file, storeName, storeLocation):
    conn = http.client.HTTPSConnection("api.box.com")
    url = "/2.0/files/{f}/content".format(f=file)
    payload = ''
    headers = {
    'Authorization': 'Bearer {token}'.format(token = appToken)
    }
    conn.request("GET", url, payload, headers)
    res = conn.getresponse()
    #print("Status:", res.status)
    if res.status == 302:
        downloadLocation = res.getheader('location')
        data = requests.get(downloadLocation)
        #print(data)
        StoreLocally(storeName, storeLocation, data.content)


def StoreLocally(fileName, location, data, user=1000, group=1000):
    filePath = '{location}{file}'.format(location=location, file=fileName)
    with open(filePath, 'wb') as file:
        file.write(data)
    os.chown(filePath, user, group)


GetImageList()
GetExcelFile()