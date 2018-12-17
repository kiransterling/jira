from jira import JIRA


def issue_details(issue_no):
    record1 = {}
    data1 = []
    jira = JIRA('https://jsd-dev.wce.ibm.com/')
    key_cert_data = None
    key_cert = 'jira_privatekey.pem'
    with open(key_cert, 'r') as key_cert_file:
        key_cert_data = key_cert_file.read()

    oauth_dict = {
        'access_token': 'JQ7ackw2VRq0P8s1BpuINZqkTPzj7sY1',
        'access_token_secret': 'z1CL4KsvnGCrfrTmXwaZVkMtqEUhnaOc',
        'consumer_key': 'B2B Automation Reporting',
        'key_cert': key_cert_data,
        }

    auth_jira = JIRA(oauth=oauth_dict,
                     options={'server': 'https://jsd-dev.wce.ibm.com'})

    try:

        issue = auth_jira.issue(issue_no)

        for data in issue.fields.comment.comments:

            record1['emailAddress']=data.author.emailAddress
            record1['displayName']=data.author.displayName
            record1['created'] =data.created
            record1['updated'] =data.updated
            record1['body'] =data.body
            data1.append(record1)
            record1={}
        return data1
		
    except:
        return 0

