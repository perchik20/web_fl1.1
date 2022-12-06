from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from calendar import monthrange
from datetime import datetime, date

from sweater import db, app
from sweater.models import User, Service, IdAccess, AllServ


@app.route("/", methods=['POST', 'GET'])
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

@app.route("/reviews")
@login_required
def reviews():
    return render_template('pages_for_chr/review.html')

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
    # print(today)

    return render_template('Mas/choose_serv.html', today=today, allserv=allserv, level=level, id=id)


@app.route("/new_order/masters/<level>/<id>/<today>/<mas_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def choose_datetime1(id, today, level, mas_id, user_id):

    time = ['11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00',
            '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00']
    month_name = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ', 'ИЮНЬ', 'ИЮЛЬ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯБ', 'ДЕК' ]

    date1 = request.form.get('datetime')


    if request.method == 'POST':

        masters = User.query.filter_by(levelmas=level).all()
        serv = AllServ.query.filter_by(id=id).first()

        All_time = dict()

        for el in masters:
            set_time = Service.query.filter_by(dat=date1, id_master=el.id).all()
            time1 = []
            time2 = []
            for i in set_time:
                time1.append(str(i.time))
            for z in time:
                if z not in time1:
                    time2.append(z)
            All_time[el.id] = [time2]

        month = date.today()
        month = month.month

        month_name1 = month_name[month-1]

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
                               level=level,
                               month_name=month_name1
                               )
    else:

        masters = User.query.filter_by(levelmas=level).all()
        serv = AllServ.query.filter_by(id=id).first()

        dt = datetime.strptime(today, '%Y-%m-%d')

        All_time = dict()

        for el in masters:
            set_time = Service.query.filter_by(dat=dt.date(), id_master=el.id).all()
            time1 = []
            time2 = []
            for i in set_time:
                time1.append(str(i.time))
            for z in time:
                if z not in time1:
                    time2.append(z)
            All_time[el.id] = [time2]

        month = date.today()
        month = month.month

        month_name1 = month_name[month-1]

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
                               level=level,
                               month_name=month_name1
                               )

# //////////////////////Зпись через выбор услуги////////////////////////////


@app.route("/new_order/services")
@login_required
def choose_services():
    all_serv = AllServ.query.all()
    today = date.today()
    # print(today)

    return render_template('Serv/choose_serv1.html', all_serv=all_serv, today=today)


@app.route("/masters/<int:level>/<int:id>/<today>", methods=['GET', 'POST'])
@login_required
def choose_datetime(id, today, level):
    time = ['11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00',
            '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00']
    month_name = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ', 'ИЮНЬ', 'ИЮЛЬ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯБ', 'ДЕК']

    date1 = request.form.get('datetime')

    if request.method == 'POST':

        masters = User.query.filter_by(levelmas=level).all()
        serv = AllServ.query.filter_by(id=id).first()

        # dt = datetime.strptime(today, '%Y-%m-%d')

        All_time = dict()

        for el in masters:
            set_time = Service.query.filter_by(dat=date1, id_master=el.id).all()
            time1 = []
            time2 = []
            for i in set_time:
                time1.append(str(i.time))
            print(time1)
            for z in time:
                if z not in time1:
                    time2.append(z)

            All_time[el.id] = [time2]

        month = date.today()
        month = month.month

        month_name1 = month_name[month - 1]

        current_year = datetime.now().year
        month1 = month
        days = monthrange(current_year, month1)[1]

        today1 = date.today()
        today1 = today1.day
        days_arr = []
        for i in range(today1, days + 1):
            days_arr.append(i)

        return render_template('Serv/choose_datetime1.html',
                               All_time=All_time,
                               masters=masters,
                               serv=serv,
                               id=id,
                               today=today,
                               days=days_arr,
                               level=level,
                               month_name=month_name1
                               )
    else:
        masters = User.query.filter_by(levelmas=level).all()
        serv = AllServ.query.filter_by(id=id).first()

        dt = datetime.strptime(today, '%Y-%m-%d')

        All_time = dict()


        for el in masters:
            set_time = Service.query.filter_by(dat=dt.date(), id_master=el.id).all()
            time1 = []
            time2 = []
            for i in set_time:
                time1.append(str(i.time))
            print(time1)
            for z in time:
                if z not in time1:
                    time2.append(z)

            All_time[el.id] = [time2]

        month = date.today()
        month = month.month

        month_name1 = month_name[month-1]

        current_year = datetime.now().year
        month1 = month
        days = monthrange(current_year, month1)[1]

        today1 = date.today()
        today1 = today1.day
        days_arr = []
        for i in range(today1, days+1):
            days_arr.append(i)

        return render_template('Serv/choose_datetime1.html',
                               All_time=All_time,
                               masters=masters,
                               serv=serv,
                               id=id,
                               today=today,
                               days=days_arr,
                               level=level,
                               month_name=month_name1
                               )

# ////////////////////////Добовление данных в базу//////////////////////////////////

@app.route("/masters/<int:id>/<today>/<time>/<master>/<int:user>", methods=['GET', 'POST'])
@login_required
def new_signup(id, today, time, user, master):

    dt = datetime.strptime(today, '%Y-%m-%d')
    print(time)
    tm = datetime.strptime(time, '%H:%M:%S')
    print(tm.time())
    print(type(tm))

    new_signup = Service(serv=id, dat=dt, time=tm.time(), id_user=user, id_master=master)

    db.session.add(new_signup)
    db.session.commit()

    return redirect(url_for('index'))

# ///////////////////////////////Страница записей для мастера///////////////////////////////////////////////

@app.route("/list_of_servs/<int:id>", methods=['GET', 'POST'])
@login_required
def list_of_servs(id):
    servs=Service.query.filter_by(id_master=id).all()

    mass1=[]

    for i in servs:
        mass=[]
        mass.append(i.serv)
        mass.append(i.dat)
        mass.append(i.time)
        mass.append(i.id_user)
        mass1.append(mass)

    for i in mass1:
        z=0
        while z < len(i):
            if z == 0:
                serv=AllServ.query.filter_by(id=int(i[z])).first()
                i[z] = serv.name_serv
            if z == 3:
                user = User.query.filter_by(id=i[z]).first()
                name = str(user.name) + ' ' + str(user.number)
                i[z] = name
            z+=1



    return render_template("pages_for_chr/list_of_servs.html", mass=mass1)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    number = request.form.get('number')
    password = request.form.get('password')

    if number and password:
        user = User.query.filter_by(number=number).first()
        id_us = user.id
        access = IdAccess.query.filter_by(idUser=id_us)

        mass_chek = []
        for z in access:
            mass_chek.append(z)

        if len(mass_chek) == 1:
            if check_password_hash(user.password, password):
                login_user(user)

                return render_template("pages_for_chr/user.html")
            else:
                flash('Login or password is not correct')
        else:
            for i in mass_chek:
                if i.idAccess == 2 and password == 'alina':
                    login_user(user)
                    return render_template("pages_for_chr/master.html")
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
