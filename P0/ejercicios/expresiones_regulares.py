def regex():
    texto = "Lorem ipsum dolor Sit amet, consectetur Adipiscing elit. Suspendisse tempor sodales Arcu ac eleifend. Vivamus eget blandit eros, nec pulvinar velit."
    lista = re.findall('[A-Za-z]+\s[A-Z]', texto)
    resultado = texto

    for elemento in lista:
        resultado = resultado + "<p>" + elemento + "</p>"
    return resultado

def verificar_email(email):
    expresion_regular = '^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9]+(\.[A-Z|a-z]{2,})+$'
    resultado = re.match(expresion_regular,email)
    mensaje = 'El email NO es valido'
    if resultado != None:
        mensaje = "El email es valido"

    return mensaje

def verificar_numero(numero):
    expresion_regular = '^([0-9]{4}[\s\-])*[0-9]{4}$'
    resultado = re.match(expresion_regular,numero)
    mensaje = 'El numero de la tarjeta NO es valido'
    if resultado != None:
        mensaje = "El numero de la tarjeta es valido"

    return mensaje