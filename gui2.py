#imports
import PySimpleGUI as sg
#Web scraping para cotizacion del dolar del dia
import requests
from bs4 import BeautifulSoup
#EbaySDK
from ebaysdk.finding import Connection
import datetime
from deep_translator import GoogleTranslator

r = requests.get('https://www.cambioschaco.com.py') #Url de donde obtener los datos
soup = BeautifulSoup(r.text, 'html.parser')
cotizacion = soup.find_all('span', class_="sale", limit = 1) #Dolar
#print(cotizacion[0].text.replace('.', ""))
dolar = float(cotizacion[0].text.replace('.', ""))

API_KEY = ""

#Leer la key del txt.. "key.txt"
with open('key.txt', 'r') as f:
    API_KEY = f.readline().strip()
    #print(API_KEY)

class Ebay(object):
    def __init__(self, API_KEY, keyword, capacity, resultado):
        self.api_key = API_KEY
        self.keyword = keyword
        self.capacity = capacity
        self.resultado = resultado
    def fetch(self):
        try:
            api = Connection(appid=self.api_key, config_file=None)
            #conditionId 2020 es Very Good
            #response = api.execute('findItemsAdvanced', {'keywords': 'Iphone X 64GB Very Good', 'country':'US', 'condition.conditionId':'2020', 'capacity':'64'})
            response = api.execute('findItemsAdvanced', {'keywords': self.keyword +' '+self.capacity + 'GB', 'country':'US', 'condition': {'conditionId': '2020'}})
            #print(response) #Comprobar que esta conectando recibindo un objeto
            #print(response.reply) #Resultados con la busqueda del keyword mandado, tambien sirve para ver los objetos disponibles
            #item = response.reply.searchResult.item[0]
            cont = 0
            lista = []
            for item in response.reply.searchResult.item: #De los resultados, imprime el titulo y el precio actual.
                if item.condition.conditionId == "2020":
                    #print(item)
                    #Todos los resultados
                    x = self.keyword.split("Pro")
                    x1 = self.keyword.split("Max")
                    if len(x1) > 1 or len(x) > 1:
                        if len(x1) > 1 and len(x) > 1:
                            c = item.title.split("Pro Max")
                            if len(c) > 1:
                                #print(f"Title: {item.title}, Price {item.sellingStatus.currentPrice.value}, Condition {item.condition.conditionId}, Capacidad {item.capacity}")
                                lista.append(item)
                        if len(x) > 1:
                            c = item.title.split("Pro Max")
                            if len(c) == 1:
                                #print(f"Title: {item.title}, Price {item.sellingStatus.currentPrice.value}, Condition {item.condition.conditionId}")
                                lista.append(item)
                    else:
                        x = item.title.split("Pro Max")
                        x1 = item.title.split("Pro")
                        if len(x1) == 1 and len(x) == 1:
                            #print(f"Title: {item.title}, Price {item.sellingStatus.currentPrice.value}, Condition {item.condition.conditionId}")
                            lista.append(item)
            resultado = []
            for item in lista:
                x = item.title.split("GB")
                x2 = item.title.split(f"{self.capacity}")
                if len(x) == 2 and len(x2) > 1:
                    resultado.append(item)
            #print("Lista filtrada: ")
            for item in resultado:
                x = item.title.split("mini")
                if len(x) == 1:
                    #print(f"Title: {item.title}, Price {item.sellingStatus.currentPrice.value}, Condition {item.condition.conditionId}")
                    if cont == 0:
                        self.resultado = item
                        cont += 1

        except ConnectionError as e:
            print(e)
            print(e.response.dict())
    def parse(self):
        pass  
    
#Convertir el precio a un numero con puntos y redondeado
def pre_puntos(precio):
    a = list(precio)
    nr = ""
    cont = len(precio)
    for j in range(0, len(precio)):
        if j > 3:
            nr = nr + "0"
        else:
            nr = nr + a[j]
        cont -= 1
        if cont % 3 == 0 and j != len(precio) - 1:
            nr = nr + "."
    #print(nr)
    return nr  
#tema simplegui
sg.theme("reddit")

#Cabecera, Productos
headings= ['Producto', 'Capacidad','Costo', 'Venta', 'Condición']
data = []
def make_win1():
    # Columna 1:
    col1 = [[sg.Text("Cotización del dia:")],
            [sg.Text(f"Dolar: {cotizacion[0].text} Gs")],
            [sg.Text("Producto:"), sg.Input(key='pro', size=(20, 1))],
            [sg.Button('Buscar'), sg.Button('Borrar'), sg.Button('Modificar'),],
            ]
     # Columna 2:

    col2 = [[sg.Text(" ",key='bus_p'), sg.Text(" ",key='bus_c')],
            [sg.Table(data, headings=headings, justification='left', key='ta_p', enable_events=True, col_widths=[60, 10, 15, 60])],
            [sg.Text("Costo total:  "), sg.Text(" ",key='ttv'), sg.Text("Ganancias:  "), sg.Text(" ",key='ttg'), sg.Button('Exportar presupusto')]]

    layout = [[sg.Column(col1), sg.Column(col2, element_justification='')]]

    return sg.Window('Cotizaciones de productos', layout, location=(800,600), finalize=True)


window1= make_win1(), None

# Definimos una lista para almacenar los productos
productos = []
#Actualizacion tabla de productos
def act():
    window["ta_p"].update(values=productos)
    window.refresh()

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Salir':
        window.close()
        ##if window == window2:       # if closing win 2, mark as closed
            ##window2 = None
        if window == window1: # if closing win 1, exit program
            break    
    elif event == 'Buscar' :
        pro = (values['pro']).lower()   #minisculas
        capacidades = []
        if pro == "iphone x" or pro == "iphone 10":
                capacidades = ["64", "256"]
        if pro == "iphone 11":
                capacidades = ["64","128","256"]
        if pro == "iphone 12":
                capacidades = ["64","128", "256"]
        if pro == "iphone 13":
                capacidades = ["128","256"]
        ##print(capacidades)
        for x in range(0, len(capacidades)):
                #Conexion a la API y busqueda del celular
                e = Ebay(API_KEY, pro, capacidades[x], "")
                e.fetch()
                e.parse()
                #Mejor resultado
                busqueda = e.resultado
                #print(busqueda)
                # Tiene 7% de taxes  y 50mil cuesta el envio, recargar eso
                precio = str(int(float(busqueda.sellingStatus.currentPrice.value) * dolar))
                preciov = str((int((float(busqueda.sellingStatus.currentPrice.value) + 70) * dolar)))
                # print(precio)
                a = list(precio)
                # print(precio)
                #print(preciov)
                preciob = pre_puntos(precio)
                preciov = pre_puntos(preciov)
                print("Mejor elección: ")
                titulo = str(busqueda.title)
                # print(titulo)
                traductor = GoogleTranslator(source='en', target='es')
                titulo = traductor.translate(busqueda.title)
                condicion = traductor.translate(busqueda.condition.conditionDisplayName)
                # print(titulo)
                print(f"Titulo: {busqueda.title}, Precio de Ebay: {preciob}, Precio de venta: {preciov} Gs, Condicion: {condicion}")
                # Agregamos eñ producto a la lista
                nombre = busqueda.title.split()
                producto = [nombre[1] + " " + nombre[2],capacidades[x] + " GB",preciob, preciov, condicion]
                productos.append(producto)
                act()
                producto = []
