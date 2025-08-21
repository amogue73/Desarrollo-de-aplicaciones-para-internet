entrada = open("entrada" , "r")
numero = int(entrada.readline())
entrada.close()

posicion1 = 0
posicion2 = 1
nesimo = -1
for i in range(numero):
    nesimo = posicion1
    aux = posicion2
    posicion2 = posicion1 + posicion2
    posicion1 = aux

salida = open("salida", "w")
salida.write(str(nesimo))
salida.close()
