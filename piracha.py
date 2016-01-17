from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3


#configuration
DATABASE = '/home/edgar/PythonProjects/piracha/piracha.db'
DEBUG = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# create our little application :)

app = Flask(__name__)
app.config.from_object(__name__)

def db_functions(sql, data):
	conn = sqlite3.connect(app.config['DATABASE'])
	cursor = conn.cursor()
	cursor.execute(sql, data)
	conn.commit()#saves changes
	cursor.close()


def db_functions_read(sql, data):
	conn = sqlite3.connect(app.config['DATABASE'])
	cursor = conn.cursor()
	results = cursor.execute(sql, data)
	query_result = results.fetchall()
	return query_result

def db_admin_functions(sql):
	conn = sqlite3.connect(app.config['DATABASE'])
	cursor = conn.cursor()
	results = cursor.execute(sql)
	query_result = results.fetchall()
	return query_result



def get_user(email):
	sql = "select email, password from users where email = :email"
	data = {'email':email}
	user = db_functions_read(sql, data)
	return user

def get_user_profile(email):
	sql = "select username, email password from users where email = :email"
	data = {'email':email}
	user = db_functions_read(sql, data)
	return user

def get_user_ideas(username):
	sql = "select idea, brief, status from ideas where username = :username"
	data = {'username':username}
	idea = db_functions_read(sql, data)
	return idea

def login_user(email, password):
	user = get_user(email)
	if not user:
		return False

	if (user[0][0] == email) and (user[0][1] == password):
		return True
	else:
		return False


def check_admin(admin, password):
	if admin == 'edantonio505' and password == 'Ed23021989':
		return True
	else:
		return False



def saves_users(username, email, password):
	sql = 'insert into users (username, email, password) values (:username, :email, :password)'
	data = {'username':username, 'email':email, 'password':password}
	db_functions(sql, data)

def saves_ideas(idea, brief, description, username):
	sql = 'insert into ideas (idea, brief, description, username, status) values\
	(:idea, :brief, :description, :username, :status)'
	status = 0 #not accepted
	data = {'idea':idea, 'brief':brief, 'description':description, 'username':username, 'status':status}
	db_functions(sql, data)

def get_all_ideas():
	sql  = "select * from ideas"
	response = db_admin_functions(sql)
	return response

def get_idea_data(idea):
	sql = "select * from ideas where id = :id"
	data = {'id': idea}
	idea = db_functions_read(sql, data)
	return idea[0]


def positive_idea(idea):
	sql = "update ideas set status = '1' where id = :id"
	data = {'id': idea}
	db_functions(sql, data)


def negative_idea(idea):
	sql = "update ideas set status = '2' where id = :id"
	data = {'id': idea}
	db_functions(sql, data)
#------------------------------------------------------------------------------------------------------

@app.route('/')
def welcome():
	if session:
		return redirect(url_for('dashboard', username = session['username']))
	return render_template('welcome.html')




@app.route('/signup',  methods=['GET', 'POST'])
def signup():
	if request.method == "POST":
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		saves_users(username, email, password)
		session['username'] = username
		return render_template('add_idea.html', username = username)
	return render_template('signup.html')






@app.route('/add_idea', methods=['GET', 'POST'])
def add_idea():
	if not session:
		return redirect(url_for('welcome'))
	username  = session['username']
	if request.method == "POST":
		idea = request.form['idea']
		brief = request.form['brief']
		description = request.form['description']

		saves_ideas(idea, brief, description, username)
		flash('You have sucessfully submitted your idea {username}'.format(username = username))
		return redirect(url_for('dashboard', username = username))
	return render_template('add_idea.html', username = username)





@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('welcome'))






@app.route('/login',  methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		email = request.form['email']
		password = request.form['password']
		authorization = login_user(email, password)
		if not authorization:
			flash('Retry again, or else...')
			session.pop('username', None)
			return redirect(url_for('login'))
		else:
			user = get_user_profile(email)
			username = user[0][0]
			session['username'] = username
			flash('you have sucessfully logged in')
			return redirect(url_for('dashboard', username = username))
	return render_template('login.html')






@app.route('/dashboard/<username>')
def dashboard(username):
	if not session:
		return redirect(url_for('welcome'))
	ideas = get_user_ideas(username)
	return render_template('dashboard.html', username = username, ideas = ideas)





@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if session and session['username'] != 'edantonio505':
		return redirect(url_for('welcome'))

	elif session and session['username'] == 'edantonio505':
		admin = session['username']
		ideas = get_all_ideas()
		return render_template('admin_dashboard.html', ideas = ideas, admin = admin)


	if request.method == "POST":
		admin = request.form['admin']
		password = request.form['password']
		if not check_admin(admin, password):
			return redirect(url_for('welcome'))
		else:
			session['username'] = admin
			ideas = get_all_ideas()
			return render_template('admin_dashboard.html', ideas = ideas, admin = admin)
			
	return render_template('admin.html')


@app.route('/check/<idea>')
def check_idea(idea):
	idea = get_idea_data(idea)
	return render_template('check_idea.html', idea = idea)


@app.route('/accept/<idea>')
def accept_idea(idea):
	positive_idea(idea)

	flash('The idea has been accepted')
	return redirect(url_for('admin'))


@app.route('/reject/<idea>')
def reject_idea(idea):
	negative_idea(idea)

	flash('The idea has been rejected')
	return redirect(url_for('admin'))

if __name__ == '__main__':
	app.debug = True
	app.run()