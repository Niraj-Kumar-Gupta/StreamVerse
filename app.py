# import the necessary packages
# import the necessary packages
from flask import Flask, render_template, Response,request,redirect,url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
# import the necessary packages
# import the necessary packages



# flask app initialization and configuration
# flask app initialization and configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'BJHGTY%$#%$Y%^&YIHUGTY^&*((*)(&*^%FTYGUHJIKO))'

db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)
@login.user_loader
def load_user(sno):
    return user_db.query.get(sno)

# flask app initialization and configuration
# flask app initialization and configuration




# database models
# database models
class user_db(UserMixin, db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    # email=db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def get_id(self):
        return self.sno



class event_db(db.Model):
    
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    date_and_time=db.Column(db.Text)
    
    date=db.Column(db.Text)
    time=db.Column(db.Text)
    
    Overview = db.Column(db.Text)
    Poster_Url = db.Column(db.Text)
    
    cam1 = db.Column(db.Text)
    cam2 = db.Column(db.Text)
    cam3 = db.Column(db.Text)
    cam4 = db.Column(db.Text)
    
    date_created = db.Column(db.DateTime)


class register_events_db(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    user=db.Column(db.Text)
    

    # Admin
    # Admin
admin = Admin(app, name="data base", template_mode='bootstrap3')
admin.add_view(ModelView(user_db, db.session))
admin.add_view(ModelView(event_db, db.session))
admin.add_view(ModelView(register_events_db, db.session))
    # Admin
    # Admin
    
# database models
# database models





#  login logout and signup
#  login logout and signup
@app.route("/login", methods=['Get', 'Post'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = user_db.query.filter_by(
            username=username, password=password).first()  # checking if user exits
        if user:
            login_user(user)  # login that user
            return redirect("/")
        else:
            return render_template("login.html", message="No such user exists")

    return render_template("login.html")


@login_required
@app.route("/logout")
def logout():
    logout_user()  # logout current user
    return redirect("/")


@app.route("/signup", methods=['Get', 'Post'])
def signup():
    if request.method == "POST":
        username = request.form['username']  # requesting data from form
        password = request.form['password']  # requesting data from form
        # requesting data from form
        confirm_password = request.form['confirm_password']
        # checking if username already exists
        user = user_db.query.filter_by(username=username).first()
        if user:
            return render_template("login.html", message="username already exists")
        else:
            if password == confirm_password:
                if len(password) > 5:
                    user = user_db(
                        username=username, password=password)
                    db.session.add(user)  # adding user if not exists
                    db.session.commit()
                    user_object = user_db.query.filter_by(
                        username=username).first()
                    login_user(user_object)  # login new user
                    return redirect("/")
                return render_template("login.html", message="password length is too short")
            else:
                return render_template("login.html", message="password and confirm password are not same")

    return render_template("signup.html")

#  login logout and signup  end
#  login logout and signup  end







from collections import defaultdict
@app.route('/')
def home(message=None):
    user= load_user(current_user.get_id())
    days=defaultdict(list)
    allevents=event_db.query.order_by(
                event_db.date_created).all()
    
    
    
    for event in allevents:
        days[event.date].append(event)
    if message:
        if user:
            return render_template('events.html',days=days,myevents=False,user=user,message=message)
        else:
            return render_template('events.html',days=days,myevents=False,user=False,message=message)
    if user:
        return render_template('events.html',days=days,myevents=False,user=user)
    else:
        return render_template('events.html',days=days,myevents=False,user=False)
        

@app.route('/new/<message>')
def home1(message):
    user= load_user(current_user.get_id())
    days=defaultdict(list)
    allevents=event_db.query.order_by(
                event_db.date_created).all()
    
    
    
    for event in allevents:
        days[event.date].append(event)
    if message:
        if user:
            return render_template('events.html',days=days,myevents=False,user=user,message=message)
        else:
            return render_template('events.html',days=days,myevents=False,user=False,message=message)
    if user:
        return render_template('events.html',days=days,myevents=False,user=user)
    else:
        return render_template('events.html',days=days,myevents=False,user=False)
        




@login_required
@app.route('/myevents')
def events(message=None):
    user= load_user(current_user.get_id())
    if user:
        days=defaultdict(list)
        allevents=event_db.query.order_by(
                    event_db.date_created).all()
        
        
        regiesterEvents=register_events_db.query.filter_by(user=user.username).all()
        for event in allevents:
            if register_events_db.query.filter_by(index=event.index).first():
                days[event.date].append(event)
        if len(days)==0:
            return render_template('events.html',days=days,myevents=True,user=user,message="No events registered")
        if message:
            return render_template('events.html',days=days,myevents=True,user=user,message=message)
        return render_template('events.html',days=days,myevents=True,user=user)
    else:
        return redirect(url_for('home1',message="login First"))



@app.route("/register/<int:id>")
def form(id):
    user= load_user(current_user.get_id())
    if user:
        register=register_events_db.query.filter_by(index=id,user=user.username).first()
        print(register,id)
        if register:
            print(register.user,register.index)
            return redirect(url_for('home1',message="Already Registered"))
        else:
            myevent = register_events_db(
                            index=id,user=user.username)
            db.session.add(myevent)  # adding user if not exists
            db.session.commit()
        return redirect(url_for('home1',message="Registered Successfully"))
    else:
        return redirect(url_for('home1',message="login First"))
    
    
    
@login_required
@app.route("/stream/<id>/<streamid>")
def video(id,streamid):
    stream = event_db.query.filter_by(index=id).first()
    return render_template("video.html",stream=stream,streamid=streamid)


if __name__ == '__main__':
    with app.app_context():
        # Create all database tables
        db.create_all()
    app.run(debug=True,host="0.0.0.0",port="5000")
