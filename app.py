# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:54:06 2022

@author: DELL
"""
import os
from flask import Flask, render_template,request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/path/to/the/uploads' 
ALLOWED_EXTENTIONS = ['png','jpeg','jpg']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cemdqefrcxidwi:20e62dd2b7b83daae4dc1eab0144e9eb690cacdb165357b8293a1daea5e4a32d@ec2-44-209-24-62.compute-1.amazonaws.com:5432/ddgru7s7jfdhlv'
app.config['SECRET_KEY']= 'secretkey'
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

db = SQLAlchemy(app)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fn = db.Column(db.String(50), nullable=False)
    ln = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    ministration = db.Column(db.String(50), nullable=False)
    fellowship = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    date_registered = db.Column(db.DateTime, nullable = False, default= datetime.utcnow)
    
@app.route('/index', methods=["POST","GET"])
def register():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        _email = request.form['email']
        _location = request.form['location']
        _ministration = request.form['ministration']
        _fellowship = request.form['fellowship']
        phoneno = request.form['phonenumber']
        _unit = request.form['unit']
        _gender = request.form['gender']
        file = request.files['file']
        
        filename = secure_filename(file.filename)
            
        user = Registration.query.filter_by(email=_email).first()
        if user:
            flash("Email already exist", category="error")
            
        elif file == " ":
            flash("Picture not uploaded", category="error")
        
        else:
            details = Registration(fn=firstname,ln=lastname,email=_email,location=_location,ministration=_ministration,fellowship=_fellowship,phonenumber=phoneno,unit=_unit,gender=_gender)
            db.session.add(details)
            db.session.commit()
            flash("Successful", category="success")
            return redirect('/index')
        return render_template("index.html")
    else:
        all_details = Registration.query.all()
        return render_template("index.html", reg=all_details)
    
@app.route('/profile', methods=["POST","GET"])
def profile():
    all_details = Registration.query.all()
    return render_template("profile.html", reg=all_details)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=(True))