from enum import unique
from flask import Flask,render_template,request,flash,redirect
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///studentdatabase.db"
app.config['SQLALCHEMY_BINDS']={
    'two' : 'sqlite:///teacherdatabase.db',
    'three' : 'sqlite:///book.db',
    'four' : 'sqlite:///wanttoissue.db',
    'five' : 'sqlite:///hasbeenissued.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Form.query.get(int(user_id))

@app.route("/")
def welcome():
    return render_template("homepage.html")

#___________________________________________STUDENT FORM CLASS FOR ADD CATEGORY IN DATABASE_______________________________________________________
class Form(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    middlename = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=False)
    nad = db.Column(db.String(80), unique=True, nullable=False)
    collegename = db.Column(db.String(100),nullable=False)
    course = db.Column(db.String(80), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    phone = db.Column(db.String(10),nullable=False,unique=True)
    password = db.Column(db.String(50), nullable=False)
    studentuniquecode = db.Column( db.String(80),nullable=False )
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"{self.firstname, self.lastname}"                           

#___________________________________________STUDENT REGISTER PAGE FOR ADD DATA IN DATABASE_______________________________________________________

@app.route("/register",methods=['GET','POST'])
def registerpage():
    if request.method=='POST':
        firstname=request.form.get('firstname')
        middlename=request.form.get('middlename')
        lastname=request.form.get('lastname')
        nad=request.form.get('nad')
        collegename=request.form.get('collegename')
        course=request.form.get('course')
        semester=request.form.get('semester')
        email=request.form.get('email')
        phone=request.form.get('phone')
        password=request.form.get('password')
        studentuniquecode = request.form.get('uniqueid')
        user=Form(firstname=firstname,middlename=middlename,lastname=lastname,nad=nad,collegename=collegename,course=course,semester=semester,email=email,phone=phone,password=password,studentuniquecode=studentuniquecode)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template("newform.html")    
    

#___________________________________________     STUDENT LOGIN     _______________________________________________________    

@app.route("/login",methods=['GET','POST'])
def loginpage():
    if request.method == 'POST':
        firstname=request.form.get('firstname')
        middlename=request.form.get('middlename')
        lastname=request.form.get('lastname')
        password=request.form.get('password')
        tuniqueid=request.form.get('tuniqueid')
        userinfo=Form.query.filter_by(firstname=firstname,middlename=middlename,lastname=lastname).first()
        if (userinfo and password == userinfo.password and tuniqueid == 'BCA1234'):
            login_user(userinfo)
            return render_template('mainpageofstudent.html')
        else:
            flash('Login nahi hua hai entries check kro fir se','danger')
            return redirect('/login')    
    return render_template("Sloginpage.html")

#___________________________________________   STUDENT FUNCTIONS    _______________________________________________________

@app.route("/mainpageofstudent")
def mainpageofstudent():
    return render_template("mainpageofstudent.html")

class Issued(db.Model):
    __bind_key__ = 'five'
    id=db.Column(db.Integer,primary_key=True)
    issuename = db.Column(db.String(80), nullable=False)    
    issuedbookname = db.Column(db.String(80),  nullable=False)
    bcode = db.Column(db.String(80), nullable=False)
    studentuniquecode = db.Column(db.String(80), nullable=False)
    bissuedate = db.Column(db.String(80),  nullable=False)
    breturndate = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"{self.issuename}"


@app.route("/Smybook")      
def Smybook():
    hasissued = Issued.query.all()
    return render_template("Smybook.html",hasissued=hasissued )  

class Want(db.Model): 
    __bind_key__ = 'four'
    id=db.Column(db.Integer,primary_key=True)
    studentname = db.Column(db.String(80), nullable=False)
    bname = db.Column(db.String(80), nullable=False)
    studsem = db.Column(db.String(100),primary_key=False)
    suniquecode = db.Column(db.String(100), primary_key=False)        
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"{self.studentname}"          

@app.route("/library",methods=['GET','POST'])
def Slibraryinfo():
    __bind_key__='four'
    studentname=request.form.get('studentname')
    bname=request.form.get('bname')
    studsem=request.form.get('studsem')
    suniquecode=request.form.get('suniquecode')
    stud = Want(studentname=studentname,bname=bname,studsem=studsem,suniquecode=suniquecode)
    db.session.add(stud)
    db.session.commit()
    book = Book.query.all() 
    return render_template("Slibraryinfo.html",book=book)

#___________________________________________________TEACHER CLASS FOR ADD CATEGORY IN DATABASE_______________________________________________________        

class Teacher(UserMixin,db.Model):
    __bind_key__ = 'two'
    id=db.Column(db.Integer,primary_key=True)
    teachername = db.Column(db.String(80), nullable=False)
    course = db.Column(db.String(80), nullable=False)
    temail = db.Column(db.String(120),unique=True, nullable=False)
    tphone= db.Column(db.String(10),nullable=False,unique=True)
    tpassword = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"{self.teachername}"

#___________________________________________TEACHER FORM CLASS FOR ADD CATEGORY IN DATABASE_______________________________________________________

@app.route("/teacherform",methods=['GET','POST'])
def teacherform():
    __bind_key__ = 'two'
    if request.method=='POST':
        teachername=request.form.get('teachername')
        course=request.form.get('course')
        temail=request.form.get('temail')
        tphone=request.form.get('tphone')
        tpassword=request.form.get('tpassword')
        teacher=Teacher(teachername=teachername,course=course,temail=temail,tphone=tphone,tpassword=tpassword)
        db.session.add(teacher)
        db.session.commit()
        return redirect('/tlogin')
    return render_template('teacherform.html')
#_________________________________________________________TEACHER LOGIN____________________________________________________________________________


@app.route("/tlogin",methods=['GET','POST'])
def tloginpage():
    __bind_key__ = 'two'
    if request.method == 'POST':
        teachername = request.form.get('teachername')
        tpassword = request.form.get('tpassword')
        teacherinfo = Teacher.query.filter_by(teachername = teachername).first()
        if (teacherinfo and tpassword == teacherinfo.tpassword ):
            login_user(teacherinfo)
            return render_template('mainpageofteacher.html')
        else:
            flash('Login nahi hua hai entries check kro fir se','danger')
            return redirect('/tlogin')
    return render_template("Tloginpage.html")

#___________________________________________________ TEACHER FUCTIONS _______________________________________________________

@app.route("/mainpageofteacher")
def teacherdashboard():
    return render_template("mainpageofteacher.html")

@app.route("/Tlibrary",methods=['GET','POST'])
def Tlibraryinfo():
    if request.method=='POST':
        bookname=request.form.get('bookname')
        author=request.form.get('author')
        numberofbooks=request.form.get('numberofbooks')
        semester=request.form.get('semester')
        book=Book(bookname=bookname,author=author,numberofbooks=numberofbooks,semester=semester)
        db.session.add(book)
        db.session.commit()
    book = Book.query.all()
    return render_template("Tlibraryinfo.html", book=book)

@app.route("/TStudentinfo",methods=['GET','POST'])            
def Tstudentinfo(): 
     __bind_key__='five'
     if request.method=='POST':
        issuename=request.form.get('issuename')
        issuedbookname=request.form.get('issuedbookname')
        bcode=request.form.get('bcode')
        studentuniquecode=request.form.get('studuniquecode') 
        bissuedate=request.form.get('bissuedate')
        breturndate=request.form.get('breturndate')
        issued = Issued(issuename=issuename, issuedbookname=issuedbookname,bcode=bcode,studentuniquecode=studentuniquecode,bissuedate=bissuedate,breturndate=breturndate)
        db.session.add(issued)
        db.session.commit()
     user = Form.query.all()  
     issue = Want.query.all() 
     counter = Form.query.count() 
     return render_template("Tstudentinfo.html",user=user,issue=issue,counter=counter)             
                        

#__________________________________________BOOK MODEL TO ADD BOOK______________________________________________________

class Book(db.Model):
    __bind_key__ = 'three'
    id=db.Column(db.Integer,primary_key=True)
    bookname = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    numberofbooks = db.Column(db.String(100),primary_key=False)
    semester = db.Column(db.String(100),primary_key=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"{self.bookname}"

@app.route("/delete/<int:id>")
def deleterecord(id):
    book=Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/Tlibrary")

@app.route("/deleteissue/<int:id>")
def deleterequest(id):
    request=Want.query.filter_by(id=id).first()
    db.session.delete(request)
    db.session.commit()
    return redirect("/TStudentinfo") 

# @app.route("/test/<name>")
# def test(name):
#     return 'Hello %s! ' % name


if (__name__=="__main__"):
    app.run(debug=True)                