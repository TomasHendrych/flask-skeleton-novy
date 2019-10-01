"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template
from .forms import LogUserForm, secti,masoform,vstupnitestform
from ..data.database import db
from ..data.models import LogUser
blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')

@blueprint.route('/loguserinput',methods=['GET', 'POST'])
def InsertLogUser():
    form = LogUserForm()
    if form.validate_on_submit():
        LogUser.create(**form.data)
    return render_template("public/LogUser.tmpl", form=form)

@blueprint.route('/loguserlist',methods=['GET'])
def ListuserLog():
    pole = db.session.query(LogUser).all()
    return render_template("public/listuser.tmpl",data = pole)

@blueprint.route('/secti', methods=['GET','POST'])
def scitani():
    form = secti()
    if form.validate_on_submit():
        return render_template('public/vystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/secti.tmpl', form=form)

@blueprint.route('/maso', methods=['GET','POST'])
def masof():
    form = masoform()
    if form.validate_on_submit():
        return render_template('public/masovystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/maso.tmpl', form=form)

@blueprint.route('/vstupni_test', methods=['GET','POST'])
def vstupnitest():
    from ..data.models import Vysledky
    from flask import flash
    form = vstupnitestform()
    if form.validate_on_submit():
        vysledek = 0
        if form.otazka1.data == 40:
            vysledek += 1
        if form.otazka2.data == 81:
            vysledek += 1
        if form.otazka3.data.upper() == "PONDELI":
            vysledek += 1
        i = Vysledky(username=form.Jmeno.data, hodnoceni=vysledek)
        db.session.add(i)
        db.session.commit()
        flash("Vysledek ulozen", category="Error")
        return "ok"
    return render_template('public/vstup.tmpl', form=form)

@blueprint.route('/nactenijson', methods=['GET','POST'])
def nactenijson():
    from flask import jsonify
    import requests, os
    os.environ['NO_PROXY'] = '127.0.0.1'
    proxies = {
        "http": None,
        "https": "http://192.168.1.1:800"
    }
    response = requests.get("http://192.168.10.1:5000/nactenijson")
    json_res = response.json()
    data = []
    for radek in json_res["list"]:
        data.append(radek["main"]["temp"])
    return render_template("public/dataprint.tmpl",data=data)
    #return jsonify(json_res)

@blueprint.route("/simple_chart")
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)

from flask import flash
from ..data.models import Parent
from ..data.models import Child

@blueprint.route('/vstup_rodic',methods=['GET','POST'])
def rodic():
    from .forms import ValidateParent
    form = ValidateParent()
    if form.is_submitted():
        Parent.create(**form.data)
        flash(message="Ulozeno",category="info")
    return render_template('public/rodic.tmpl', form=form)

@blueprint.route('/vstup_dite',methods=['GET','POST'])
def dite():
    from .forms import ValidateChild
    form = ValidateChild()
    form.parent_id.data = db.session.query(Parent).all()
    if form.is_submitted():
        Child.create(**form.data)
        flash(message="Ulozeno",category="info")
    return render_template('public/dite.tmpl', form=form)
