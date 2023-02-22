
#EbaySDK
from ebaysdk.finding import Connection
import datetime
from deep_translator import GoogleTranslator

#Web scraping
import requests
from bs4 import BeautifulSoup
r = requests.get('https://www.cambioschaco.com.py') #Url de donde obtener los datos
soup = BeautifulSoup(r.text, 'html.parser')
cotizacion = soup.find_all('span', class_="sale", limit = 1) #Dolar
#print(cotizacion[0].text.replace('.', ""))
dolar = float(cotizacion[0].text.replace('.', ""))
print(f"Dolar hoy: {cotizacion[0].text}")
API_KEY = "cARLOSLu-Directod-PRD-a2e2968b1-8eb57663"

obj = input("Que quieres buscar?")
cap = input("De cuantos gb?")
lista = []
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
            response = api.execute('findItemsAdvanced', {'keywords': self.keyword +' '+self.capacity, 'country':'US', 'condition': {'conditionId': '2020'}})
            #print(response) #Comprobar que esta conectando recibindo un objeto
            #print(response.reply) #Resultados con la busqueda del keyword mandado, tambien sirve para ver los objetos disponibles
            #item = response.reply.searchResult.item[0]
            cont = 0
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
                if len(x) == 2:
                    resultado.append(item)
            print("Lista filtrada: ")
            for item in resultado:
                print(f"Title: {item.title}, Price {item.sellingStatus.currentPrice.value}, Condition {item.condition.conditionId}")
            self.resultado = resultado[0]
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
    def parse(self):
        pass

if __name__ == "__main__":
    e = Ebay(API_KEY, obj, cap, "")
    e.fetch()
    busqueda = e.resultado
    #print(busqueda)
    precio = str(int(float(busqueda.sellingStatus.currentPrice.value) * dolar))
    #print(precio)
    a = list(precio)
    nr = ""
    cont = len(precio)
    for i in range(0,len(precio)):
        nr = nr + a[i]
        cont -= 1
        if cont % 3 == 0 and i != len(precio) - 1:
            nr = nr + "."
    print("Mejor elección: ")
    titulo = str(busqueda.title)
    #print(titulo)
    traductor = GoogleTranslator(source='en', target='es')
    titulo = traductor.translate(busqueda.title)
    condicion = traductor.translate(busqueda.condition.conditionDisplayName)
    #print(titulo)
    print(f"Titulo: {busqueda.title}, Precio: {nr} Gs, Condicion: {condicion}")
    #print(f"Title: {busqueda.title}, Price {busqueda.sellingStatus.currentPrice.value}, Condition {busqueda.condition.conditionDisplayName}")
    e.parse()