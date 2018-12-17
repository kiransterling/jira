from pymongo import MongoClient
import jira_details


def getDBCollection():
    try:
        conn = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = conn.IssueTracker
        # Created or Switched to collection names:
    col = db.IssueDetails
    return col


def MongoRead(incident_no):
    collection = collection=getDBCollection()
    data={}
    cursor = collection.find({"JiraIncidentNumber": incident_no})
    if cursor.count()==0:
        return 0
    else:
        data['pagerdutydata']=cursor[0]
        data['jiradata']=jira_details.issue_details(incident_no)
        return data

def ListIncident(number):
    if number <=0:
        return 0
    else:
        collection = getDBCollection()
        cursor=collection.find().sort('Opened',-1).limit(number);
        return cursor
