from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from sweater import db, app
from sweater.models import User, Service, Masters, AccessRights, IdAccess, Time, AllServ


@app.route("/")
def index():

    idaccess = IdAccess.query.filter_by(idAccess=2).all()
    masters = []
    for i in idaccess:
        masters.append(User.query.filter_by(id=i.idUser).first())
    count = len(masters)

    all_serv = AllServ.query.all()

    return render_template("main.html", masters=masters, count=count, all_serv=all_serv)


@app.route("/new_order")
@login_required
def two_buttons():
    return render_template('new_order.html')


@app.route("/new_order/masters")
@login_required
def choose_master():
    masters = []

    idaccess = IdAccess.query.filter_by(idAccess=2).all()

    for i in idaccess:
        z = User.query.filter_by(id=i.idUser).first()
        masters.append(z)

    return render_template("choose_master.html", masters=masters)


@app.route("/new_order/services")
@login_required
def choose_services():
    all_serv = AllServ.query.all()
    return render_template('choose_serv.html', all_serv=all_serv)

@app.route("/masters", methods=['GET', 'POST'])
def choose_datetime():
    datetime = request.form.get('datetime')

    print(datetime)
    return render_template('choose_datetime.html')


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

# @app.route("/signup", methods=["GET", "POST"])
# @login_required
# def signup():
#     masters = Masters.query.all()
#     return render_template('signup.html', masters=masters)


# @app.route('/signup/<int:id>/')
# @login_required
# def signup1(id):
#     masters1 = Masters.query.get(id)
#     return render_template('signup_time.html', masters1=masters1)
#
# @app.route('/signup/<int:id>/<time>')
# @login_required
# def signup2(id, time):
#     print(id)
#     print(time)
#     masters2 = Masters.query.get(id)
#
#     return render_template('signup_serv.html', masters2=masters2, time=time)
#
# @app.route('/signup/<int:id>/<time>/<serv>/<int:user_id>', methods=["GET", "POST"])
# @login_required
# def signup3(id, time, serv, user_id):
#     new_serv = Service(serv=serv, time=time, id_user=user_id, id_master=id)
#
#     db.session.add(new_serv)
#     db.session.commit()
#
#     return render_template('main.html')
