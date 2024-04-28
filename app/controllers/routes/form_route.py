from flask import Blueprint, render_template, request, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify
import os
import ssl
import smtplib
from dotenv import load_dotenv

load_dotenv()

form_route = Blueprint('form_route', __name__)

@form_route.get('/')
def home_page():
    return render_template("index.html")

@form_route.post('/submit')
def submit():
    name = request.form['name']

    email_sender = os.getenv("EMAIL_SENDER") 
    email_pass = os.getenv("SMTP_PASSWORD")
    email_reciever = os.getenv("EMAIL_RECIEVER")

    body = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email</title>
    </head>
    <body style="margin: 0; padding: 0; box-sizing: border-box;">
        <main>
            <span>{name}</span>
            <div style="background-color: red; padding: 10px; width: 400px; object-fit: cover;">
                <p style="background-color: cadetblue; width: 400px;">email enviado com sucesso!!</p>
                <div style="background-image: url('https://i.pinimg.com/736x/31/65/f3/3165f3d062c8d43cfdd0c836e1811075.jpg'); background-size: cover; width: 400px; height: 200px;"></div>
            </div>
        </main>
    </body>
    </html>
"""
    em = MIMEMultipart('alternatives')

    em['Subject'] = f'Formulário de Agrado por {name}'

    html_part = MIMEText(body, 'html')

    em.attach(html_part)

    context = ssl.create_default_context()


    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        print("Sending email...")
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_reciever, em.as_string())

    return render_template("index.html")
