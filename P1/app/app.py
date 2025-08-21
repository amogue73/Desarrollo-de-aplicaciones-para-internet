#./app/app.py
#from msilib.schema import LockPermissions
from flask import Flask
import random
import re

app = Flask(__name__)
          
@app.route('/')
def hello_world():
  return 'Hello, World!'

#Calcula los numeros primos comprendidos entre 1 y 100
#utilizando el método de Eratóstenes

@app.route('/eratostenes')
def eratostenes():
  max = 100

  #crea una lista de 100 elementos, todos con el valor True
  primo = [True for i in range(max+1)]

  p = 2
  #se 'tachan' los números que son múltiplos
  #de cada primo que esté comprendido entre 1
  #y la raíz cuadrada de max
  while (p*p <= max):

      if (primo[p] == True):
        #no es necesario comprobar los números menores
        #al cuadrado del primo del que se están tachando
        #sus múltiplos porque ya habrán sido tachados
        #al hacer lo mismo con un número primo menor
          for i in range(p * p, max+1, p):
              primo[i] = False
      
      p += 1

  numeros = []
  for p in range(2, max+1):
      if primo[p]:
          numeros.append(p)

  return numeros

#calcula los números de la sucesión de Fibonacci
#hasta el de la posición especificada por la url
@app.route('/fibonacci/<int:entrada>')
def fibonacci(entrada):
  numero = entrada

  posicion1 = 0
  posicion2 = 1
  nesimo = -1
  for i in range(numero):
      nesimo = posicion1
      aux = posicion2
      posicion2 = posicion1 + posicion2
      posicion1 = aux

  return str(nesimo)

#comprueba si una secuencia de corchetes está balanceada
#para ello, comprueba que hay el mismo número de corchetes
#que abren y que cierran y también comprueba con cada
#corchete que hay mayor o igual número de corchetes
#que abren que corchetes que cierran.
@app.route('/corchetes/<int:pares>')
def corchetes(pares):
  cadena = ""

  for i in range(2*pares):
      if random.random() < 0.5:
          cadena += "["
      else:
          cadena += "]"

  resultado = cadena
  cerrables = 0
  balanceada = True
  i = 0
  while (i < 2*pares and balanceada):
      if (cadena[i] == "["):
          cerrables += 1
      elif (cadena[i] == "]"):
          cerrables -= 1
      else:
          balanceada = False
      
      if cerrables < 0:
          balanceada = False
      if ( (i == 2*pares -1) and cerrables != 0):
          balanceada = False
      i+=1

  if(balanceada):
      resultado += " => La secuencia esta balanceada"
  else:
      resultado += " => La secuencia no esta balanceada"

  return resultado

#devuelve todas las coincidencias de una palabra seguida
#por un espacio en blanco y una letra mayúscula de un texto
#predeterminado
@app.route('/regex')
def regex():
    texto = "Lorem ipsum dolor Sit amet, consectetur Adipiscing elit. Suspendisse tempor sodales Arcu ac eleifend. Vivamus eget blandit eros, nec pulvinar velit."
    lista = re.findall('[A-Za-z]+\s[A-Z]', texto)
    resultado = texto

    for elemento in lista:
        resultado = resultado + "<p>" + elemento + "</p>"
    return resultado

#comprueba si un email pasado por la url es válido o no
@app.route('/verificar_email/<string:email>')
def verificar_email(email):
    expresion_regular = '^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+$'
    resultado = re.match(expresion_regular,email)
    mensaje = 'El email NO es valido'
    if resultado != None:
        mensaje = "El email es valido"

    return mensaje

#comprueba si un número de tarjeta pasado por la url
#es válido, en el sentido de que se componga por
#secuencias de cuatro números separados por un
#espacio en blanco o por un guion
@app.route('/verificar_numero/<string:numero>')
def verificar_numero(numero):
    expresion_regular = '^([0-9]{4}[\s\-])*[0-9]{4}$'
    resultado = re.match(expresion_regular,numero)
    mensaje = 'El numero de la tarjeta NO es valido'
    if resultado != None:
        mensaje = "El numero de la tarjeta es valido"

    return mensaje

@app.route('/imagen')
def imagen():
    pagina = "<!DOCTYPE html>\
    <html lang='en'>\
    <head>\
        <meta charset='UTF-8'>\
        <meta http-equiv='X-UA-Compatible' content='IE=edge'>\
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>\
        <title>Pagina</title>\
    </head>\
    <body>\
        <img src='static/ugr.jpg'>\
    </body>\
    </html>"

    return pagina
#devuelve un texto que indica que la página no existe
#en caso de que se de el error 404
@app.errorhandler(404)
def page_not_found(error):
    return "La pagina no existe"
