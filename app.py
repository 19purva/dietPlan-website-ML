from flask import Flask,render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import  DataRequired,Email,ValidationError
from bcrypt
from flask_mysqldb import MYSQL

app=Flask(__name__)

# MYSQL Configuraton
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='mydatabase'
app.secret_key='your_secret_key'

mysql=MYSQL(app)

class RegisterForm(FlaskForm):
    name=StringField("Username",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=StringField("Password",validators=[DataRequired()])
    submit= submitField("Register")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        Username=form.Username.data
        email=form.email.data
        password=form.password.data
        
        hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
         
        # store  data into database
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO users (Username,email,password) 
                       VALUES(%s,%s,%s),(Username,email,password)")
        mysql.connect.commit()
        cursor.close() 
        
        return redirect(url_for('login'))
        
    return render_template('register.html',form=form)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('login.html')


if __name__ =='__main__':
    app.run(debug=True)