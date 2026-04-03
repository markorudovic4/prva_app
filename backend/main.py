from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='/home/mrudovic/prva_app/frontend')
# Sve se smešta u jedan fajl: e_poslovanje.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e_poslovanje.db'
db = SQLAlchemy(app)

# Modeli - Sve u jednoj bazi
class Zaposleni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime_prezime = db.Column(db.String(100), nullable=False)
    pozicija = db.Column(db.String(100))
    odmori = db.relationship('Odmor', backref='zaposleni', lazy=True)

class Ugovor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(50)) # Zaposleni ili Projekat
    naslov = db.Column(db.String(200))
    datum_kreiranja = db.Column(db.DateTime, default=datetime.utcnow)

class Odmor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zaposleni_id = db.Column(db.Integer, db.ForeignKey('zaposleni.id'))
    pocetak = db.Column(db.String(20))
    kraj = db.Column(db.String(20))

# Kreiranje baze pri pokretanju
with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    zaposleni = Zaposleni.query.all()
    ugovori = Ugovor.query.all()
    return render_template('index.html', zaposleni=zaposleni, ugovori=ugovori)

@app.route('/dodaj_zaposlenog', methods=['POST'])
def dodaj_zaposlenog():
    novo_ime = request.form.get('ime')
    novi = Zaposleni(ime_prezime=novo_ime, pozicija="Software Engineer")
    db.session.add(novi)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
