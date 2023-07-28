import PySimpleGUI as sg

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="test"
)

sg.theme("reddit")
#Cabecera 1, Tabla de Costos
headings = ['Tipo', 'Costo']
costos = []
data_values = []

#Cargar tabla de costos
mycursor = mydb.cursor()
mycursor.execute('SELECT des_c, cb_c FROM costos ')
myresult = mycursor.fetchall()
mycursor.close()
costos = myresult

#Cabecera 2, Pago
headings2= ['Numero', 'Tipo', 'Costo','Dias','Sub-Total', '% Descuento',
            'Total']
data = []


def make_win1():
    # Columna 1:
    col1 = [[sg.Text("Nro Habitacion:"), sg.Input(key='nro_h', size=(10, 1))],
            [sg.Table(costos, headings=headings, justification='left', key='ta_co', enable_events=True)],
            [sg.Text("Dias de Estadia:"), sg.Input(key='dia_e', size=(10, 1))],
            [sg.Radio('Contado', "pago", default=False, key="me_p")],
            [sg.Radio('Credito', "pago", default=True)],
            [sg.Button('Cargar'), sg.Button('Borrar'),sg.Button('Crear')],
            [sg.Button('Modificar'), sg.Input(key='mod', size=(10, 1)), sg.Button('Act')]
            ]

    # Columna 2:

    col2 = [[sg.Table(data, headings=headings2, justification='left', key='ta_r', enable_events=True)],
            [sg.Text("Total:  "), sg.Text(" ",key='ttg')]]

    layout = [[sg.Column(col1), sg.Column(col2, element_justification='')]]

    return sg.Window('Window Title', layout, location=(800,600), finalize=True)

def make_win2():

    layout = [[sg.Text('Cargar Habitaciones:')],
              [sg.Text('Tipo:'), sg.Input(key='tipo_h', enable_events=True)],
              [sg.Text('Costo:'), sg.Input(key='costo_h', enable_events=True)],
              [ sg.Button('Ingresar'), sg.Button('Limpiar'), sg.Button('Salir')]]
    return sg.Window('Cargar Habitaciones', layout, finalize=True)




window1, window2 = make_win1(), None


data_selected = []
data_selected2 = []
global totalg
totalg = 0
def act():
    mycursor = mydb.cursor()
    mycursor.execute('SELECT nm,tp,co,di,st,ds,tt FROM pago ')
    result = mycursor.fetchall()
    # print(result)
    mycursor.close()
    window["ta_r"].update(values=result)
    window.refresh()
def actt(total):
    print(total)
    global totalg
    totalg = total + totalg
    totalg = int(totalg)
    window["ttg"].update(totalg)

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Salir':
        mycursor = mydb.cursor()
        mycursor.execute('DELETE FROM pago')
        mydb.commit()
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1: # if closing win 1, exit program
            mycursor = mydb.cursor()
            mycursor.execute('DELETE FROM pago')
            mydb.commit()
            break

    elif event == 'Crear' and not window2:
        window2 = make_win2()
    elif event == 'ta_r':
        mycursor.close()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM pago ')
        asd = mycursor.fetchall()
        data_selected2 = [asd[row] for row in values[event]]
    elif event == 'ta_co':
        data_selected = [costos[row] for row in values[event]]
        sel = data_selected[0]
        print(sel)
    elif event == 'Ingresar':
        tipo = (values['tipo_h'])
        costo = (values['costo_h'])
        if tipo and costo:
            mycursor = mydb.cursor()
            sql = "INSERT INTO costos (des_c, cb_c) VALUES (%s, %s)"
            val = (tipo, costo)
            mycursor.execute(sql, val)
            mydb.commit()
    elif event == 'Act':
        mycursor = mydb.cursor()
        mycursor.execute('SELECT des_c, cb_c FROM costos ')
        result = mycursor.fetchall()
        window["ta_co"].update(values=result)
        window.refresh()

    elif event == 'Cargar' :
        nroh = (values['nro_h'])
        dias = (values['dia_e'])

        if data_selected and nroh and dias:
            nroh = int(nroh)
            dias = int(dias)
            cb = int(sel[1])
            #Si es true significa que paga al contado, false credito
            if values['me_p'] == True:
                descp = cb * 0.10
                desc = 10
            else:
                descp = cb * 0.05
                desc = 5
            print(descp)
            descd = 0
            if dias > 10:
                desc = desc + 2
                descd = cb * 0.02
            dsct = descd + descp
            st = cb * dias
            total = st - dsct
            total = int(total)
            mycursor = mydb.cursor()
            sql = "INSERT INTO pago (nm,tp,co,di,st,ds,tt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nroh, sel[0],sel[1],dias,st,desc,total)
            mycursor.execute(sql, val)
            mydb.commit()
            print(totalg)
            act()
            actt(total)

    elif event == 'Limpiar':
        window['tipo_h'].update('')
        window['costo_h'].update('')
    elif event == 'Modificar':
        aux = data_selected2[0]

        mod = (values['mod'])
        if data_selected2 and mod:
            id = aux[0]
            dias = int(mod)
            nhro = aux[1]
            if data_selected and nroh and dias:
                nroh = int(nroh)
                dias = int(dias)
                cb = int(sel[1])
                if values['me_p'] == True:
                    descp = cb * 0.10
                    desc = 10
                else:
                    descp = cb * 0.05
                    desc = 5
                print(descp)
                descd = 0
                if dias > 10:
                    desc = desc + 2
                    descd = cb * 0.02
                dsct = descd + descp
                st = cb * dias
                total = st - dsct
                total = int(total)
                mycursor = mydb.cursor()
                sql = "UPDATE pago SET nm= %s, tp= %s, co= %s, di = %s, st= %s, ds= %s, tt= %s" \
                      " WHERE id_pago = %s"
                val = (nroh, sel[0],sel[1],dias,st,desc,total, id)
                mycursor.execute(sql, val)
                mydb.commit()
                print(totalg)
                act()
                actt(total)
            act()

    elif event == 'Borrar':
        aux = data_selected2[0]
        if data_selected2:
            print(aux)
            id = aux[0]
            rest = aux[7]
            mycursor = mydb.cursor()
            sql = "DELETE FROM pago WHERE id_pago = %s"
            val = [id]
            mycursor.execute(sql, val)
            mydb.commit()
            rest = rest * -1
            print(rest)
            actt(rest)
            act()

window.close()
