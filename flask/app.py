from flask import Flask,render_template, flash, redirect , url_for , session ,request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField , TextAreaField ,PasswordField , validators
from passlib.hash import sha256_crypt
from functools import wraps


app = Flask(__name__)
app.debug = True


#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MYSQL
mysql = MySQL(app)


#Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():

        #create cursor
        cur = mysql.connection.cursor()

        #get articles
        result = cur.execute("SELECT * FROM articles")

        articles = cur.fetchall()

        if result > 0:
            return render_template('articles.html',articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('articles.html',msg=msg)
        #close connection
        cur.close()

@app.route('/article1')
def article1():

        #create cursor
        cur = mysql.connection.cursor()

        #get articles
        result = cur.execute("SELECT * FROM article1")

        articles = cur.fetchall()

        if result > 0:
            return render_template('article1.html',article1=article1)
        else:
            msg = 'No Articles Found'
            return render_template('article1.html',msg=msg)
        #close connection
        cur.close()


@app.route('/article/<string:id>/')
def article(id):
    #create cursor
    cur = mysql.connection.cursor()

    #get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s",[id])

    article = cur.fetchone()

    return render_template('article.html',article=article)

class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=4,max=25)])
    email = StringField('Email',[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [ validators.DataRequired (),validators.EqualTo('confirm',message ='passwords do not match')])
    confirm = PasswordField('Confirm password')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create crusor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))

        # commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()

        flash("You are now Registered and you can login" , 'success')

        redirect(url_for('login'))
    return render_template('register.html',form=form)

class RegisterForm2(Form):
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=4,max=25)])
    email = StringField('Email',[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [ validators.DataRequired (),validators.EqualTo('confirm',message ='passwords do not match')])
    confirm = PasswordField('Confirm password')

@app.route('/register2', methods=['GET','POST'])
def register2():
    form = RegisterForm2(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create crusor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))

        # commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()

        flash("You are now Registered and you can login" , 'success')

        redirect(url_for('login'))
    return render_template('register2.html',form=form)

class RegisterForm3(Form):
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=4,max=25)])
    empid = StringField('Employee ID',[validators.Length(min=4,max=25)])
    email = StringField('Email',[validators.Length(min=4,max=25)])
    num = StringField('Mobile number',[validators.Length(min=4,max=25)])
    password = PasswordField('Password', [ validators.DataRequired (),validators.EqualTo('confirm',message ='passwords do not match')])
    confirm = PasswordField('Confirm password')

@app.route('/register3', methods=['GET','POST'])
def register3():
    form = RegisterForm3(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        empid = form.empid.data
        email = form.email.data
        num = form.num.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create crusor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO emp_reg(name,empid,email,num,username,password) VALUES(%s,%s,%s,%s,%s,%s)",(name,empid,email,num,username,password))

        # commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()

        flash("You are now Registered and you can login" , 'success')

        redirect(url_for('login'))
    return render_template('register3.html',form=form)

# user login
@app.route('/login',methods =['GET','POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor

        cur = mysql.connection.cursor()

        #Get user by username

        result = cur.execute("SELECT * FROM users WHERE username = %s" ,[username])

        if result > 0:
        # Get Stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate,password):
                #Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in ','success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Username not found'
                return render_template('login.html',error=error)
                #close connection
            cur.close()

        else:
            error = 'Username not found'
            return render_template('login.html',error=error)

    return render_template('login.html')

#check if user logged in

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login','danger')
            return redirect(url_for('login'))
    return wrap



#logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('you are now logged out ','success')
    return redirect(url_for('login'))
# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():

    #create cursor
    cur = mysql.connection.cursor()

    #get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html',articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html',msg=msg)
    #close connection
    cur.close()

#Article form class

class ArticleForm(Form):
    year = StringField('year',[validators.Length(min=1,max=10)])
    operator = StringField('operator',[validators.Length(min=4,max=100)])
    pax_to = StringField('pax_to',[validators.Length(min=1,max=10)])
    pax_from = StringField('pax_from',[validators.Length(min=1,max=10)])
    pax_total = StringField('pax_total',[validators.Length(min=1,max=10)])
    freight_to = StringField('freight_to',[validators.Length(min=1,max=10)])
    freight_from = StringField('freight_from',[validators.Length(min=1,max=10)])
    freight_total = StringField('freight_total',[validators.Length(min=1,max=10)])

#Add Article1

@app.route('/edit_article1', methods=['GET','POST'])
@is_logged_in
def edit_article1():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        year = form.year.data
        operator = form.operator.data
        pax_to = form.pax_to.data
        pax_form = form.pax_from.data
        pax_total = form.pax_total.data
        freight_to = form.freight_to.data
        freight_from = form.freight_from.data
        freight_total = form.freight_total.data

        # Create a cursor

        cur = mysql.connection.cursor()

        #execute

        cur.execute("INSERT INTO article1(year,operator,pax_to,pax_from,pax_total,freight_to,freight_from,freight_total) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(year, operator, pax_to, pax_from, pax_total, freight_to, freight_from, freight_total))

        #commit to db

        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Article created ','success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article1.html',form=form)

#Edit Article1

@app.route('/edit_article/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        year = form.year.data
        operator = form.operator.data
        pax_to = form.pax_to.data
        pax_from = form.pax_from.data
        pax_total = form.pax_total.data
        freight_to = form.freight_to.data
        freight_from = form.freight_from.data
        freight_total = form.freight_total.data

        # Create a cursor

        cur = mysql.connection.cursor()

        #execute

        cur.execute("INSERT INTO article1(year,operator,pax_to,pax_from,pax_total,freight_to,freight_from,freight_total) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(year, operator, pax_to, pax_from, pax_total, freight_to, freight_from, freight_total))

        #commit to db

        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Data Added ','success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html',form=form)



#Edit Article2

@app.route('/edit_article2/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_article2(id):
    # Create cursor
    cur = mysql.connection.cursor()
    #get article by id
    result = cur.execute("SELECT * FROM article2")

    article = cur.fetchone()

    #get form
    form = ArticleForm(request.form)

    #populate article form fields
    form.year.data = article['year']
    form.air_hrs.data = article['air_hrs']
    form.air_kms.data = article['air_kms']
    form.pax_from.data = article['pax_from']
    form.pax_total.data = article['pax_total']
    form.freight_to.data = article['freight_to']
    form.freight_from.data = article['freight_from']
    form.freight_total.data = article['freight_total']

    if request.method == 'POST' and form.validate():
        year = request.form['year']
        operator = request.form['operator']
        pax_to = request.form['pax_to']
        pax_from = request.form['pax_from']
        pax_total = request.form['pax_total']
        pax_to = request.form['freight_to']
        freight_from = request.form['freight_from']
        freight_total = request.form['freight_total']
        # Create a cursor

        cur = mysql.connection.cursor()

        #execute

        cur.execute("UPDATE article2 SET year=%d, operator=%s, pax_to=%d, pax_from=%d, pax_total=%d, freight_to=%d, freight_from=%d, freight_total=%d", (year,operator,pax_to,pax_from,pax_total,freight_to,freight_from,freight_total))

        #commit to db

        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Article Updated ','success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article2.html',form=form)



if __name__ =='__main__':
    app.secret_key='secret123'
    app.run()
