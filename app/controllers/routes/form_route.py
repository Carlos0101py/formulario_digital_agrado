from flask import Blueprint, render_template, request, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os,ssl, smtplib, json
import pandas as pd
from email.mime.base import MIMEBase
from email import encoders
import requests

load_dotenv()

form_route = Blueprint('form_route', __name__)
admin_route = Blueprint('admin_route', __name__)

@form_route.get('/')
def home_page():
    with open('itens.json', 'r') as arquivo_json:
        itens = json.load(arquivo_json)
    
    return render_template('index.html', itens=itens)

@form_route.post('/create_pdf')
def create_pdf():
    data = request.get_json()
    list = data.get('itens')
    name = data.get('nome')
    email = data.get('email')

    print('name: ',name)
    print('email: ',email)

    # cores = list['cores']
    estampas = list['estampas']
    # fontes = list['fontes']
    itens = list['itens']

    print('itens: ',itens)
    print('estampas: ',estampas)

    # df_cores = pd.DataFrame(cores, columns=['Cores'])
    # df_estampas = pd.DataFrame(estampas, columns=['Estampas'])
    # df_fontes = pd.DataFrame(fontes, columns=['Fontes'])
    df_itens = pd.DataFrame(itens, columns=['itens'])
    df_estampas = pd.DataFrame(estampas, columns=['estampas'])

    print(df_itens)
    print(df_estampas)

    def create_pdf_file(dfs, file_name):
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("Formulario Agrado", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))

        for df in dfs:
            format_data = [df.columns.values.tolist()] + df.values.tolist()
            table = Table(format_data)

            col_widths = [400] * len(df.columns)
            format_data = [df.columns.values.tolist()] + df.values.tolist()
            table = Table(format_data, colWidths=col_widths)

            table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.green),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            table.setStyle(table_style)
            elements.append(table)
            elements.append(Spacer(1, 20))
            
        doc.build(elements)

    create_pdf_file([df_itens, df_estampas], 'Formulario.pdf')

    with open('Formulario.pdf', 'rb') as file:
        pdf_data = file.read()

    files = {'pdf_file': pdf_data}
    response = requests.post('http://127.0.0.1:5000/send_email', files=files)

    return response.text

@form_route.post('/send_email')
def send_email():
    email_sender = os.getenv("EMAIL_SENDER") 
    email_pass = os.getenv("SMTP_PASSWORD")
    email_reciever = os.getenv("EMAIL_RECIEVER")

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_reciever
    msg['Subject'] = 'Formulário de Agrado'

    with open('Formulario.pdf', 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename=Formulario.pdf')
    msg.attach(part)

    with open('itens.json', 'r') as arquivo_json:
        itens = json.load(arquivo_json)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            print("Sending email...")
            smtp.login(email_sender, email_pass)
            smtp.sendmail(email_sender, email_reciever, msg.as_string())

        return jsonify({
            'status': 'ok',
            'message': 'email enviado com sucesso'
        }), 200

    except:
        return jsonify({
            'status': 'Error',
            'message': 'email não enviado'
        }), 500
