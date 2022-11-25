from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from datetime import datetime
from calendar import monthrange

from sweater import db, app
from sweater.models import User, Service, IdAccess, AllServ


@app.route("/")
def index():

    idaccess = IdAccess.query.filter_by(idAccess=2).all()
    masters = []
    for i in idaccess:
        masters.append(User.query.filter_by(id=i.idUser).first())
    count = len(masters)

    all_serv = AllServ.query.all()

    servs = 0
    for i in all_serv:
        servs += 1
    servs = str(servs)


    today = date.today()
    today = today.day

    return render_template("main.html", masters=masters, count=count, all_serv=all_serv, today=today, servs=servs)


@app.route("/new_order")
@login_required
def two_buttons():
    return render_template('new_order.html')

# //////////////////////Зпись через выбор мастера////////////////////////////


@app.route("/new_order/masters")
@login_required
def choose_master():
    masters = []

    idaccess = IdAccess.query.filter_by(idAccess=2).all()

    for i in idaccess:
        z = User.query.filter_by(id=i.idUser).first()
        masters.append(z)

    return render_template("Mas/choose_master.html", masters=masters)


@app.route("/new_order/masters/<int:level>/<int:id>", methods=['GET', 'POST'])
@login_required
def choose_serv1(level, id):
    allserv = AllServ.query.filter_by(level_mas=level).all()
    today = date.today()
    today = today.day

    return render_template('Mas/choose_serv.html', today=today, allserv=allserv, level=level, id=id)


@app.route("/new_order/masters/<level>/<id>/<today>/<mas_id>/<user_id>", methods=['GET', 'POST'])
def choose_datetime1(id, today, level, mas_id, user_id):
    # datetime = request.form.get('datetime')
    time = ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00']

    masters = User.query.filter_by(levelmas=level).all()
    serv = AllServ.query.filter_by(id=id).first()

    All_time = dict()

    for el in masters:
        set_time = Service.query.filter_by(dat=today, id_master=el.id).all()
        time1 = []
        time2 = []
        for i in set_time:
            time1.append(i.time)
        for z in time:
            if z not in time1:
                time2.append(z)
        All_time[el.id] = [time2]

    month = date.today()
    month = month.month
    current_year = datetime.now().year
    month1 = month
    days = monthrange(current_year, month1)[1]

    today1 = date.today()
    today1 = today1.day
    days_arr = []
    for i in range(today1, days+1):
        days_arr.append(i)

    return render_template('Mas/choose_datetime.html',
                           All_time=All_time,
                           masters=masters,
                           serv=serv,
                           id=id,
                           today=today,
                           days=days_arr,
                           level=level
                           )


# //////////////////////Зпись через выбор услуги////////////////////////////


@app.route("/new_order/services")
@login_required
def choose_services():
    all_serv = AllServ.query.all()
    today = date.today()
    today = today.day

    return render_template('Serv/choose_serv.html', all_serv=all_serv, today=today)


@app.route("/masters/<int:level>/<int:id>/<int:today>", methods=['GET', 'POST'])
def choose_datetime(id, today, level):
    # datetime = request.form.get('datetime')
    time = ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00']

    masters = User.query.filter_by(levelmas=level).all()
    serv = AllServ.query.filter_by(id=id).first()

    All_time = dict()

    for el in masters:
        set_time = Service.query.filter_by(dat=today, id_master=el.id).all()
        time1 = []
        time2 = []
        for i in set_time:
            time1.append(i.time)
        for z in time:
            if z not in time1:
                time2.append(z)

        All_time[el.id] = [time2]

    month = date.today()
    month = month.month
    current_year = datetime.now().year
    month1 = month
    days = monthrange(current_year, month1)[1]

    today1 = date.today()
    today1 = today1.day
    days_arr = []
    for i in range(today1, days+1):
        days_arr.append(i)

    return render_template('Serv/choose_datetime.html',
                           All_time=All_time,
                           masters=masters,
                           serv=serv,
                           id=id,
                           today=today,
                           days=days_arr,
                           level=level
                           )

@app.route("/masters/<int:id>/<int:today>/<time>/<master>/<int:user>", methods=['GET', 'POST'])
def new_signup(id, today, time, user, master):

    new_signup = Service(serv=id, time=time, id_user=user, id_master=master, dat=today)

    db.session.add(new_signup)
    db.session.commit()

    return redirect(url_for('index'))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    number = request.form.get('number')
    password = request.form.get('password')

    if number and password:
        user = User.query.filter_by(number=number).first()

        if check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('index'))

        else:
            flash('Login or password is not correct')
    else:
        flash('please fill login and password fields')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    name = request.form.get('name')
    surname = request.form.get('surname')
    second_name = request.form.get('second_name')
    number = request.form.get('number')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (name or surname or second_name or number):
            flash('Please, fill the gaps')
        elif (password != password2):
            flash('Please, check your password')
        else:
            psw = generate_password_hash(password)
            new_user = User(name=name, surname=surname, second_name=second_name, number=number, password=psw)

            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(number=number).first()

            new_access = IdAccess(idUser=user.id, idAccess=1)

            db.session.add(new_access)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response
