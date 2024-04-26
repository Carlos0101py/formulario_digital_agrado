from flask import Blueprint, render_template, request
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

    body = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email</title>
    </head>
    <style>
        * {
            box-sizing: border-box;
            padding: 0;
            margin: 0;
        }
        section {
            font-family: Lucida Sans;
            display: flex;
            flex-wrap: wrap;
            flex-direction: column;
            box-shadow: -1px 1px 5px 1px;
            padding: 1rem;
            gap: 1rem;
        }

        .info {
            display: flex;
            gap: 1rem;
        }

        .title a{
            text-decoration: none;
            color: black;
        }

    </style>
    """ + f"""
    <body>
        <main>
            <span>{name}</span>
            <p>email enviado com sucelsso!!</p>

            <img src="https://petitgato.com.br/img/webp/gatos-persas-em-sao-paulo-img-3780.webp" alt="">
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
