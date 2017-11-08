from flask import Flask, render_template,redirect,url_for, request,session
import sqlite3
import sys
import imaplib
import getpass
import email
import datetime
import email.header
from HTMLParser import HTMLParser
import json



M = imaplib.IMAP4_SSL('imap.gmail.com')


app = Flask(__name__)
app.secret_key = 'yolo'

@app.route("/")
def init():
    return render_template('login.html')

def getmails():
	M.login('excesschel@gmail.com','nihar4276')
	session['message']=''
	M.select('INBOX')
	typ, data = M.search(None, '(UNSEEN)')

	if typ != 'OK':
		session['mails']="no messages found"
	msg=data[0].split();
	n=0
	subjects=[]
    
	for num in msg:
		n=n+1
		if n==5:
			break
		typ, data = M.fetch(num, '(RFC822)')
		for response_part in data:
			if isinstance(response_part, tuple):
				original = email.message_from_string(response_part[1])
				# if original.is_multipart():
				# 	# for payload in original.get_payload():
				# 	# 	print payload.get_payload()		
				subjects.append(original['Subject'])
        
    		
	M.close()
	session['subjects']=subjects
	M.logout()

@app.route("/register",methods = ['POST', 'GET'])
def register():
	message=''
	#database init
	conn=sqlite3.connect("ITT.db")
	if request.method == 'POST':
		username = str(request.form['name']);
		password = str(request.form['password']);
		email    = str(request.form['email']);
		emailpass = str(request.form['emailpass']);


				
		#Insert
		if conn.execute("INSERT into details values(?,?,?,?)",(username,password,email,emailpass)):
			message="You have been successfully Registered!"
		else:
			message="Error! Please try again"

		session['message']=message;

	conn.commit()
	conn.close();
	return redirect('http://localhost:5000')

@app.route("/login",methods = ['POST', 'GET'])
def login():
	#database init
	conn=sqlite3.connect("ITT.db")
	message=''
	if request.method == 'POST':
		username = str(request.form['nameL']);
		password = str(request.form['passwordL']);

		content=conn.cursor()
		content.execute("SELECT * from details where username=? and password=? ",(username,password));
		cursor=content.fetchall()

		if len(cursor)==1:
			#return render_template for dashboard.html and replace return render_template
			for row in cursor:

				session['email']=row[2];
				session['emailpass']=row[3];
				session['user']=row[0];


				
			getmails()
			cursor=conn.execute("SELECT * from "+session['user']+"")
			a="['amount', 'date']"
			for row in cursor:
				a=a+",['"+str(row[1])+"',"+str(row[2])+"]";
			session['list']=a;


			conn.close();
			return redirect("http://localhost:5000/dashboard")

		else:
			conn.close();
			session['message']='User not registered!'
			return redirect('http://localhost:5000')

@app.route('/expense',methods=['POST','GET'])
def sendexpense():
	#database init
	session['message']=''
	name=str(request.form['Name']);
	date=str(request.form['Date']);
	amount=str(request.form['Comments']);

	if not amount.isdigit():
		session['message']="Amount should be a number!"
		return redirect('http://localhost:5000/update')
   
       
   
	conn=sqlite3.connect("ITT.db")

	conn.execute("CREATE table IF NOT EXISTS " + session['user'] + "( name TEXT NOT NULL, date1 TEXT NOT NULL, Amount TEXT)")

	conn.execute("INSERT into " + session['user'] + " values(?,?,?)",(name,date,amount))

	conn.commit()
	conn.close()
	session['message']="Details Successfully Added !"
	return redirect('http://localhost:5000/update')








@app.route('/dashboard')
def loadindex():
	return render_template("index.html")

@app.route('/calendar')
def loadcalendar():
	return render_template('calendar.html')

@app.route('/typography')
def loadtypography():
	return render_template('typography.html')
@app.route('/table')
def loadtable():
	return render_template('table.html')

@app.route('/chart')
def loadchart():
	return render_template('chart.html')
@app.route('/update')
def loadupdate():
	return render_template('updateExpense.html')

@app.route('/getlogin',methods=['GET','POST'])
def loadlogin():
	session['message']=''
	if request.args.get('logout'):
		session['message']="You have successfully logged out!"

	return render_template("login.html")
if __name__ == "__main__":
    app.run()
