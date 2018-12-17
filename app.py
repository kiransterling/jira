from flask import Flask,abort,render_template,request,redirect,url_for,send_file,session, jsonify
import os
import ReadMongo
from flask_wtf import Form
from flask_session import Session
from ldap3 import *
from datetime import timedelta

app = Flask(__name__)


@app.before_request
def make_session_permanent():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=60)

	
@app.route('/')
def index():
    if 'logged_in' in session and 'username' in session and session['logged_in']==True:
        return redirect(url_for('home_page'))

    if('authorized' in session):
        temp = session['authorized']
        session.pop('authorized',None)
        return render_template('login.html',authorized=temp)
    else:
        return render_template('login.html',authorized=1)

@app.route('/authentication',methods=['POST'])
def ldapAuth():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    session['username'] = str(POST_USERNAME)
    session['email'] = str(POST_USERNAME)
    session['logged_in'] = True
    return redirect(url_for('home_page'))


    server = Server('ldap://bluepages.ibm.com', get_info=ALL)
    c = Connection(server, user="", password="", raise_exceptions=False)
    noUseBool = c.bind()

    checkUserIBM = c.search(search_base = 'ou=bluepages,o=ibm.com',
         search_filter = '(mail=%s)'%(POST_USERNAME),
         search_scope = SUBTREE,
         attributes = ['dn','givenName'])

    if(checkUserIBM==False):
        session['authorized'] = 0
        return redirect(url_for('index'))


    # get the username of the emailID and authenticate password
    userName = c.entries[0].givenName[0]
    uniqueID = c.response[0]['dn']
    c2 = Connection(server,uniqueID,POST_PASSWORD)
    isPassword = c2.bind()

    if(isPassword == False):
        session['authorized'] = 0
        return redirect(url_for('index'))

    # now search group
    checkIfAdminGroup = c.search(search_base = 'cn=RSC_B2B,ou=memberlist,ou=ibmgroups,o=ibm.com',
     search_filter = '(uniquemember=%s)'%(str(uniqueID)),
     search_scope = SUBTREE,
     attributes = ['dn'])
    checkIfAdminGroup=True
	 
    if(checkIfAdminGroup==False):
        session['authorized'] = 0
        return(redirect(url_for('index')))

    #control reaches here if user password and group authentication is successful
   

    session['username'] = str(userName)
    session['email']    = str(POST_USERNAME)
    session['logged_in']= True

    return redirect(url_for('home_page'))

	
@app.route('/options',methods = ['GET'])
def home_page():
    if request.method =='GET':
        return render_template('select.html',user=session['username'])
		
@app.route('/home', methods = ['POST'])
def home():
    option = request.form['dropdown']
    if option:
        return render_template("home.html",options=option, user=session['username'])

@app.route('/processdata', methods = ['GET','POST'])
def processdata():
    if request.method == 'GET':
        issue_no = request.args.get('issue_no')
        if issue_no:
            data = ReadMongo.MongoRead(issue_no)
            if data==0:
                return render_template("ShowSingleIncident.html",isdata = 0,posts=issue_no, user=session['username'])
            else:
                return render_template("ShowSingleIncident.html",isdata =1,posts = data,user=session['username'])
        else:
            return render_template("ShowSingleIncident.html",isdata = 0,posts="Empty Data", user=session['username'])
    if request.method == 'POST':
        issue_no = request.form['issue_no']
        if issue_no:
            data = ReadMongo.MongoRead(issue_no)
            if data==0:
                return render_template("ShowSingleIncident.html",isdata = 0,posts=issue_no, user=session['username'])
            else:
                return render_template("ShowSingleIncident.html",isdata =1,posts = data,user=session['username'])
        else:
            return render_template("ShowSingleIncident.html",isdata = 0,posts="Empty Data", user=session['username'])

@app.route('/list', methods = ['POST'])
def list():
    number = int(float(request.form['number']))
    data = ReadMongo.ListIncident(number)
    if data==0:
        return render_template("ShowList.html",isdata = 0,posts = data, user=session['username'])
    else:
        return render_template("ShowList.html",isdata =1,posts = data,user=session['username'])


@app.route('/logout',methods=['GET'])
def logout():
    session.pop("email",None)
    session.pop("username",None)
    session.pop("logged_in",None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'sadasdha90sdasd98as90da8sd231kjw@!@!@!#$@#SADASFD'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    app.run(host='0.0.0.0',port=8888,debug=True)
