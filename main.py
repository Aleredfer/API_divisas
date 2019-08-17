from tkinter import *
from tkinter import ttk

import configparser  #parsear?
import json
import requests  #para realizar peticiones


DEFAULTPADDING = 4

class Exchanger(ttk.Frame):  #intercambiador
    def __init__(self, parent):
        ttk.Frame.__init__(self, width="400", height="150")
        config = configparser.ConfigParser()
        config.read('config.ini')  #accedes a 'config.ini y por tanto a la key y las 2 urls
        self.api_key = config['fixer.io']['API_KEY']
        self.all_symbols_ep = config['fixer.io']['ALL_SYMBOLS_EP']
        self.rate_ep = config['fixer.io']['RATE_LATEST_EP']
        self.pack_propagate(0)   #PAra que mande el 400x150 

       

        #variables de control:
        self.strInQuantity = StringVar(value="")   #StringVar es una variable propia del Tkinter
        self.oldInQuantity = self.strInQuantity.get()
        self.strInQuantity.trace('w', self.validarCantidad) # metodo trace, 'w' es cada vez que se escribe o modifica. ## LLama a self.convertirDivisas

        self.strInCurrency = StringVar()
        self.strOutCurrency = StringVar()
        
        #ErrorLabel
        Errores = ttk.Frame(self, height=40,)    #frInCurrency, bold = negrita
        Errores.pack(side=BOTTOM, fill=X)
        Errores.pack_propagate(0)
        self.lblErrores = ttk.Label(Errores, foreground='red', anchor=CENTER, width=50)
        self.lblErrores.pack(side=BOTTOM, fill=BOTH, expand=True)

        '''
        self.all_symbols_ep =self.all_symbols_ep.format(self.api_key)

        response = requests.get(self.all_symbols_ep)  #hazme una peticion a url
        self.currencies = json.loads(response.text)
        #if response.status_code ==200:
            #print(response.text)
            #currencies = json.loads(response.text)   # .text = al jason, la información que buscamos
            #print(currencies)
            #print(currencies['symbols']['USD'])'''

        frInCurrency = ttk.Frame(self)
        frInCurrency.pack_propagate(0)  # Mantiene el tamaño, no depende de sus 'hijos'
        frInCurrency.pack(side=LEFT, fill=BOTH, expand=True) #empaquetado a la izquierda, rellenando todo el espacio disponible y expandido en vertical
        
        #Texto fijo
        lblQ = ttk.Label(frInCurrency, text='Cantidad')   #frInCurrency
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        #Entrada
        self.inQuantityEntry = ttk.Entry(frInCurrency, font=('Helvetica', 24, 'bold'),  width=18, textvariable=self.strInQuantity)    #frInCurrency, bold = negrita
        self.inQuantityEntry.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
       
       #Combobox
        self.inCurrencyCombo = ttk.Combobox(frInCurrency, width=25, height=5, textvariable=self.strInCurrency)
        self.inCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
        self.inCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)    #bind para asociar evento/funcion

    ############ DERECHA
        frOutCurrency = ttk.Frame(self)         
        frOutCurrency.pack_propagate(0)
        frOutCurrency.pack(side=LEFT, fill=BOTH, expand=True)  #como ya hay uno a la izquierda, este se irá a la derecha. 

        #Texto fijo
        lblQ = ttk.Label(frOutCurrency, text='Resultado')   #frInCurrency
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        #Salida
        self.outQuantityLbl = ttk.Label(frOutCurrency, font=('Helvetica', 24), anchor=E, width=10)    #frInCurrency, bold = negrita
        self.outQuantityLbl.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING, ipady=2)  #ipady=2 es interno
       
        #Combobox
        self.OutCurrencyCombo = ttk.Combobox(frOutCurrency, width=25, height=5, textvariable=self.strOutCurrency)
        self.OutCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
        self.OutCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas) 

        url = self.all_symbols_ep.format(self.api_key)
        self.accesoAPI(url, self.getCurrencies)        # url, callback
        

    def validarCantidad(self, *args):
        try:
            v = float(self.strInQuantity.get())
            self.oldInQuantity = v
            self.convertirDivisas()
        except:
            self.strInQuantity.set(self.oldInQuantity)   # get coger, set meter.
    

    def accesoAPI(self, url, callback):    #recoge la url y comprueba que es correcta =200
        response = requests.get(url)

        if response.status_code ==200:
            callback(response.text)     #self.getCurrencies
        else:
            msgError ='Error en acceso a {}. response-code: {}'.format(url, response.status_code)
            raise Exception(msgError)    # EXception es para capturar cualquier excepción IMPORTANTE, msgError el mensajer que saldrá



    def convertirDivisas(self,  *args):
        base = 'EUR'
        _from =self.strInCurrency.get()
        _from = _from[0:3]
        _to = self.strOutCurrency.get()
        _to = _to[0:3]

        symbols = _from+','+_to
       
        if self.strInCurrency.get() and self.strOutCurrency and self.strInQuantity:   # comprueba que tenga todos los valores antes de intentar realizar los calculos
            # strInCurrency
            self.lblErrores.config(text='Conectando...')

            url = self.rate_ep.format(self.api_key, base, symbols)
            self.accesoAPI(url, self.showConversionRate)

           
            

    def showConversionRate(self, textdata):
        data = json.loads(textdata)
        if data['success']:
            tasa_conversion = (data['rates'][_from])    #Devuelve el valor de _from
            tasa_conversion2 = (data['rates'][_to])    #Devuelve el valor de _to
            self.lblErrores.config(text='')
        else:
            msgError = '{} - {}'.format(data['error']['code'], data['error']['type'])
            print(msgError)
            raise Exception(msgError)

        valor_label = round(float(self.strInQuantity.get()) / tasa_conversion * tasa_conversion2, 5)
        self.outQuantityLbl.config(text=valor_label)   #mete en el label de salida el resultado con un config(text=...)

    def getCurrencies(self, textdata):       # textdata = callback(response.text)  linea 101
        currencies = json.loads(textdata)    #pasa el json para darle estructura de diccionario.
        result = []
        self.symbols = currencies['symbols']  #accede al listado de todas las monedas
        for symbol in self.symbols:
            text = '{} - {}'.format(symbol, self.symbols[symbol])   #  symbol para las claves de symbols   y symbols[symbol]) para los valores.
            result.append(text)
        
        self.inCurrencyCombo.config(values=result)
        self.OutCurrencyCombo.config(values=result)
      
           
        
    
            #print(response.text)
            #currencies = json.loads(response.text)   # .text = al jason, la información que buscamos
            #print(currencies)



class MainApp(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        self.geometry('400x150')
        self.title('Exchanger fixer.io')

        self.exchanger = Exchanger(self)
        self.exchanger.place(x=0, y=0)

    def start(self):
        self.mainloop()


if __name__ == '__main__':
    exchanger = MainApp()
    exchanger.start()



'''config = configparser.ConfigParser()
config.read('config.ini')  #accede la key y 2 urls

inSymbol = input('Qué moneda quieres converir: ')
outSymbol = input('En qué otra moneda: ')

url = config['fixer.io']['RATE_LATEST_EP']
api_key = config['fixer.io']['API_KEY']

url = url.format(api_key, inSymbol, outSymbol)   #direccion compuesta para hacer la llamada

response = requests.get(url)  #hazme una peticion a url

if response.status_code ==200:
        print(response.text)
        #currencies = json.loads(response.text)   # .text = al jason, la información que buscamos
        #print(currencies)
        #print(currencies['symbols']['USD'])
else:
    print('está dando un error', response.status_code)  #codigo del estado

a = 1
 DE BASE SOLO PUEDE CONVERTIR 'EUR' '''