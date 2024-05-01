from flask import Blueprint, render_template, request, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
import os,ssl, smtplib, json
import pandas as pd

load_dotenv()

form_route = Blueprint('form_route', __name__)
admin_route = Blueprint('admin_route', __name__)

@form_route.get('/')
def home_page():
    with open('itens.json', 'r') as arquivo_json:
        itens = json.load(arquivo_json)
    
    return render_template('index.html', itens=itens)

@form_route.post('/send_pdf')
def send_pdf():
    # Receber os dados JSON do formulário
    data = request.get_json()
    list = data.get('itens')

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

    def create_pdf(dfs, file_name):
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        elements = []

        for df in dfs:
            format_data = [df.columns.values.tolist()] + df.values.tolist()
            
            table = Table(format_data)


            table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
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

    # create_pdf([df_itens, df_estampas, df_cores, df_fontes], 'exemplo.pdf')
    create_pdf([df_itens, df_estampas], 'Formulario.pdf')

    return jsonify({
        'mensagem': 'PDF criado com sucesso',
        'status': 200
    })

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
