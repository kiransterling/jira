from pymongo import MongoClient

import xlrd
from dateutil.parser import parse


#import simplejson as json

wb = xlrd.open_workbook('JiraData.xlsx')
# Print the sheet names
#print (wb.sheet_names())

sh = wb.sheet_by_index(0)
flag=0
data_list = []

DBDoc= {}

add=[]
rec={}
def unique(list):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
            # print list
    return unique_list

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")



# database
db = conn.IssueTracker
db.IssueDetails.drop()
# Created or Switched to collection names:
collection = db.IssueDetails






# Iterate through each row in worksheet and fetch values into dict
for rownum in range(1,sh.nrows):
    #print( sh.row_values(rownum))
    data=sh.cell(rownum, 0).value
    data_list.append(data)



for item in unique(data_list):
    flag = 0
    DBDoc={}
    add = []
    rec = {}
    for rownum in range(1,sh.nrows):
        if item==sh.cell(rownum, 0).value:
            if flag==0:

               data1=sh.cell(rownum, 0).value
               DBDoc['PagerDutyIncidentNumber']=data1.strip()
               data1 = sh.cell(rownum, 1).value
               DBDoc['Opened']=parse(data1.strip())
               data1= sh.cell(rownum, 2).value
               DBDoc['Bulletin']=data1.strip()
               data1= sh.cell(rownum, 3).value
               DBDoc['JiraIncidentNumber']=data1.strip()
               data1=sh.cell(rownum, 4).value
               DBDoc['SlackChannelNumber']=data1.strip()

               #DBDoc['Comments']=[{'abc':'123'},{'fsd':'324'}]
               data1 = sh.cell(rownum, 5).value
               rec['UpdatedBy']=data1.strip()
               data1 = sh.cell(rownum, 6).value
               rec['PagerDutyDataTime'] = parse(data1.strip())
               data1= sh.cell(rownum, 7).value
               rec['ImpactedServices']=data1.strip()
               data1 = sh.cell(rownum, 8).value
               rec['AssignedTo'] =data1.strip()
               data1 = sh.cell(rownum, 9).value
               rec['CurrentStatus'] = data1.strip()
               add.append(rec)
               DBDoc['Comments']=add
               flag = 1
            else:
                data1 = sh.cell(rownum, 5).value
                rec['UpdatedBy'] = data1.strip()
                data1 = sh.cell(rownum, 6).value
                rec['PagerDutyDataTime'] = parse(data1.strip())
                data1 = sh.cell(rownum, 7).value
                rec['ImpactedServices'] = data1.strip()
                data1 = sh.cell(rownum, 8).value
                rec['AssignedTo'] = data1.strip()
                data1 = sh.cell(rownum, 9).value
                rec['CurrentStatus'] = data1.strip()
                add.append(rec)
                DBDoc['Comments'] = add
    print (DBDoc)
    collection.insert_one(DBDoc)
    print("Data inserted Successfully")
#print (DBDoc)
#print (json.dumps(DBDoc))

# Printing the data inserted
cursor = collection.find()
for record in cursor:
        print(record)




