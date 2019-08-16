from tkinter import *
from tkinter import ttk

import configparser  #parsear?
import json
import requests  #para realizar peticiones

config = configparser.ConfigParser()
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

# DE BASE SOLO PUEDE CONVERTIR 'EUR'