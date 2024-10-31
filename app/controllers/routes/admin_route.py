from app.controllers.configuration.configuration import *


admin_route = Blueprint('admin_route', __name__)

def get_json():
    with open('itens.json', 'r') as arquivo_json:
        itens = json.load(arquivo_json)

    return itens

@admin_route.get('/admin')
def admin_page():

    itens = get_json()

    return render_template('admin.html', itens=itens)


@admin_route.post('/add_itens')
def add_itens():


    return 1


@admin_route.post('/delete_itens')
def delete_itens():

    print('chegou aqui')

    itens = get_json()

    return render_template('admin.html', itens=itens)