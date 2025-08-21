import random

cadena = ""

pares = 2

for i in range(2*pares):
    if random.random() < 0.5:
        cadena += "["
    else:
        cadena += "]"

print(cadena)

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
    print("La secuencia está alanceada")
else:
    print("La secuencia no está balanceada")
