from flask import Blueprint, render_template, request
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from email.mime.base import MIMEBase
from email import encoders
import os,ssl, smtplib, json
import pandas as pd
import requests

load_dotenv()

form_route = Blueprint('form_route', __name__)
admin_route = Blueprint('admin_route', __name__)

@form_route.get('/')
def home_page():
    itens = get_json()
    return render_template('index.html', itens=itens)

@form_route.get('/get_json')
def get_json():
    with open('itens.json', 'r') as arquivo_json:
        itens = json.load(arquivo_json)

    return itens

@form_route.post('/create_pdf')
def create_pdf():

    useremail = request.form['email']
    username = request.form['nome']

    itens = request.form.getlist('produtos[itens][]')
    patterns = request.form.getlist('produtos[estampas][]')
    color = request.form.getlist('produtos[cores][]')

    if not itens or not patterns or not color:
        itensJson = get_json()
        response_text = 'Todos os campos devem ser preenchidos!'
        return render_template('index.html', itens=itensJson, response_text=response_text)
    
    quant = len(itens)
    if(quant > 1):
        itensJson = get_json()
        response_text = 'Quantidade de produtos maior que o solicitado!'
        return render_template('index.html', itens=itensJson, response_text=response_text)

    df_itens = pd.DataFrame(itens, columns=['Itens'])
    df_patterns = pd.DataFrame(patterns, columns=['Estampas'])
    df_color = pd.DataFrame(color, columns=["Cores Escolhidas"])

    def create_pdf_file(dfs, file_name):
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("Formulário Agrado", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))

        body_style = styles['Normal']
        name_text = f"Nome: {username}"
        email_text = f"E-mail: {useremail}"

        paragraph_name = Paragraph(name_text, body_style)
        paragraph_email = Paragraph(email_text, body_style)

        elements.append(paragraph_name)
        elements.append(paragraph_email)
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

    create_pdf_file([df_itens, df_patterns, df_color], 'Formulario.pdf')

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

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            print("Sending email...")
            smtp.login(email_sender, email_pass)
            smtp.sendmail(email_sender, email_reciever, msg.as_string())

            itensJson = get_json()
            response_text = 'Pedido enviado com sucesso!'

            os.remove('Formulario.pdf')

            return render_template('index.html', itens=itensJson, response_text=response_text)

    except:
        itensJson = get_json()
        response_text = 'Erro ao tentar enviar o pedido!'
        return render_template('index.html', itens=itensJson, response_text=response_text)
