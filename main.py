
#EbaySDK
from ebaysdk.finding import Connection
import datetime
from deep_translator import GoogleTranslator

#Web scraping para cotizacion del dolar del dia
import requests
from bs4 import BeautifulSoup
r = requests.get('https://www.cambioschaco.com.py') #Url de donde obtener los datos
soup = BeautifulSoup(r.text, 'html.parser')
cotizacion = soup.find_all('span', class_="sale", limit = 1) #Dolar
#print(cotizacion[0].text.replace('.', ""))
dolar = float(cotizacion[0].text.replace('.', ""))
print(f"Dolar hoy: {cotizacion[0].text}")

#API KEY
API_KEY = "cARLOSLu-Directod-PRD-a2e2968b1-8eb57663"

#Pillow para crea imagenes
from PIL import Image #Para cargar las imagenes
from PIL import ImageDraw #para dibujar
from PIL import ImageOps #Reescalado
from PIL import ImageFont #Fuentes
dir_img = "./imagenes/" #carpeta de imagenes
dir_rec = "./recursos/" #carpeta de recursos
dir_save = "./post/" #carpeta de guardado de img
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


def conv_img(ruta, nombre, precios):
    #Crea una imagen del producto con su precio...
    print(f"Procesando: {nombre}")

    #Background
    image = Image.open(dir_img + f"{nombre}.png")
    draw = ImageDraw.Draw(image)


    #Escribimos precio y titulo #500, 900

    precio1 = precios[0] + " Gs"
    precio2 = precios[1] + " Gs"
    if len(precios) == 2:
        fuente = ImageFont.truetype(dir_rec + "Antonio-Bold.ttf", size=67, encoding="UTF-8")
        ancho, alto = draw.textsize(precio1, font=fuente)
        draw.text((800 - ancho // 2, 318 - alto // 2), precio1, font=fuente,fill=(39, 39, 39))
        draw.text((805 - ancho // 2, 684 - alto // 2), precio2, font=fuente,fill=(39, 39, 39))
    else:
        precio3 = precios[2] + " Gs"
        fuente = ImageFont.truetype(dir_rec + "Antonio-Bold.ttf", size=60, encoding="UTF-8")
        ancho, alto = draw.textsize(precio1, font=fuente)
        draw.text((800 - ancho // 2, 267 - alto // 2), precio1, font=fuente,fill=(39, 39, 39))
        draw.text((805 - ancho // 2, 538 - alto // 2), precio2, font=fuente,fill=(39, 39, 39))
        draw.text((805 - ancho // 2, 775 - alto // 2), precio3, font=fuente,fill=(39, 39, 39))
    #guardamos la imagen del producto
    image.save(dir_save + nombre + ".png")
    print("Success")
    return 0

if __name__ == "__main__":
    # Buscador
    celulares = ["Iphone X", "Iphone 11", "Iphone 12", "Iphone 13"]
    capacidades = ["64","256","128"]
    #11 tiene los 3, X 64 y 256, 12 los 3, 13 solo 128 y 256
    for i in range(0, len(celulares)):
        precios_imagen = []
        for x in range(0, len(capacidades)):
            #Ya que algunos no poseen las mismas capacidades
            if i == 0 and x == 2:
                break
            if i == 2 and x != 0:
                if x == 2:
                    break
                x += 1
            if i == 3:
                if x == 2:
                    break
                if x == 0 or x==1:
                    x += 1
            print(f"Busqueda: {celulares[i]} de {capacidades[x]}")
            #Conexion a la API y busqueda del celular
            e = Ebay(API_KEY, celulares[i], capacidades[x], "")
            e.fetch()
            e.parse()
            #Mejor resultado
            busqueda = e.resultado
            # print(busqueda)
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
            precios_imagen.append(preciov)
        print(precios_imagen)
        dir_im = dir_img + celulares[i]
        conv_img(dir_im, celulares[i], precios_imagen)


