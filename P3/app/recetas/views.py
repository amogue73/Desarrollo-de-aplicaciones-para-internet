# recetas/views.py

from django.shortcuts import  HttpResponse, render, redirect, get_object_or_404
from recetas.models import Receta, Ingrediente
from .forms import RecetaForm
from django.utils import timezone
from django.contrib import messages


#función para asignar colores
#comprueba si hay una cookie que indique el tema preferido: claro y oscuro
#comprueba si se acaba de seleccionar un cambio del tema
#los colores por defecto son los del tema claro

def asignar_colores(request):
    bg_color_light1 = "bg-light"
    bg_color_light2 = "bg-white"
    text_color_light1 = "text-dark"
    text_color_light2 = "text-primary"

    bg_color_dark1 = "bg-dark"
    bg_color_dark2 = "bg-black"
    text_color_dark1 = "text-light"
    text_color_dark2 = "text-info"

    bg_color1 = bg_color_light1
    bg_color2 = bg_color_light2
    text_color1 = text_color_light1
    text_color2 = text_color_light2
    color_actual = "claro"

    if "modo_color_actual" in request.COOKIES and request.COOKIES['modo_color_actual'] == "oscuro":
        bg_color1 = bg_color_dark1
        bg_color2 = bg_color_dark2
        text_color1 = text_color_dark1
        text_color2 = text_color_dark2
        color_actual = "oscuro"

    if "cambio_color" in request.GET:
        if request.GET["color_actual"] == "claro":
            bg_color1 = bg_color_dark1
            bg_color2 = bg_color_dark2
            text_color1 = text_color_dark1
            text_color2 = text_color_dark2
            color_actual = "oscuro"
        elif request.GET["color_actual"] == "oscuro":
            bg_color1 = bg_color_light1
            bg_color2 = bg_color_light2
            text_color1 = text_color_light1
            text_color2 = text_color_light2
            color_actual = "claro"
    return bg_color1, bg_color2, text_color1, text_color2, color_actual


#vista principal
#muestra todas las recetas o el resultado de la búsqueda realizada
def index(request):
    lista_recetas = list(Receta.objects.all())
    lista_resultados = []
    if "busqueda" in request.GET:
        resultado_busqueda = request.GET["busqueda"]
        for receta in lista_recetas:
            coincidencia = False
            if receta.nombre.upper().find(resultado_busqueda.upper()) != -1:
                coincidencia = True

            if coincidencia:
                lista_resultados.append(receta)
    else:
        lista_resultados = lista_recetas

    #asignación de colores claros u oscuros


    bg_color1, bg_color2, text_color1, text_color2, color_actual = asignar_colores(request)

    response = render(request, "busqueda.html", {
        "recetas":lista_resultados, 
        "bg_color1":bg_color1, 
        "bg_color2":bg_color2, 
        "text_color1":text_color1, 
        "text_color2":text_color2,
        "color_actual":color_actual})

    if "cambio_color" in request.GET:
        response.set_cookie( 'modo_color_actual', color_actual)
    
    return response

#vista que muestra los detalles de una receta

def detalles(request):
    lista_recetas = list(Receta.objects.all())
    receta = None

    for r in lista_recetas:
        if r.id == int(request.GET["id"]):
            receta = r
            break

    lista_ingredientes = list(Ingrediente.objects.all())
    lista_ingredientes_receta = []

    for i in lista_ingredientes:
        if i.receta.id == int(request.GET["id"]):
            lista_ingredientes_receta.append(i)
    
    bg_color1, bg_color2, text_color1, text_color2, color_actual = asignar_colores(request)

    response = render(request, "detalles.html", {
        "receta":receta,
        "bg_color1":bg_color1, 
        "bg_color2":bg_color2, 
        "text_color1":text_color1, 
        "text_color2":text_color2,
        "color_actual":color_actual,
        "id":receta.id,
        "ingredientes":lista_ingredientes_receta})

    if "cambio_color" in request.GET:
        response.set_cookie( 'modo_color_actual', color_actual)
    
    return response

#vista con la que se añade una receta

def receta_new(request):
    error = False
    if request.method =="POST":
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():

            receta = form.save(commit=False)
            receta.author = request.user
            receta.published_date = timezone.now()
            receta.save()
            id = receta.id
            url = '/detalles/?id=' + str(id)
            messages.success(request, "Receta creada con éxito" )
            return redirect(url)
        messages.error(request, "Error. No se ha podido crear la receta.")
        error = True
    else:
        form = RecetaForm()

    bg_color1, bg_color2, text_color1, text_color2, color_actual = asignar_colores(request)

    response = render(request, 'receta_edit.html', {
        'form': form,
        'error': error,
        'mensajeError': "La receta no ha sido creada",
        "bg_color1":bg_color1, 
        "bg_color2":bg_color2, 
        "text_color1":text_color1, 
        "text_color2":text_color2,
        "color_actual":color_actual})

    if "cambio_color" in request.GET:
        response.set_cookie( 'modo_color_actual', color_actual)

    return response

#vista con la que se edita una receta

def receta_edit(request):
    receta = get_object_or_404(Receta, pk=int(request.GET["id"]))
    error = False
    if request.method =="POST":
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():

            receta = form.save(commit=False)
            receta.author = request.user
            receta.published_date = timezone.now()
            receta.save()
            id = receta.id
            url = '/detalles/?id=' + str(id)
            messages.success(request, "Receta editada con éxito" )
            return redirect(url)
        messages.error(request, "Error. La receta no ha sido editada.")
        error = True

    else:
        form = RecetaForm(instance=receta)

    bg_color1, bg_color2, text_color1, text_color2, color_actual = asignar_colores(request)

    response = render(request, 'receta_edit.html', {
        'form': form,
        'error': error,
        'mensajeError': "La receta no se ha podido editar",
        "bg_color1":bg_color1, 
        "bg_color2":bg_color2, 
        "text_color1":text_color1, 
        "text_color2":text_color2})
        
    if "cambio_color" in request.GET:
        response.set_cookie( 'modo_color_actual', color_actual)
    return response

#vista para eliminar una receta

def receta_delete(request):
  receta = Receta.objects.get(id=int(request.GET["id"]))
  receta.delete()
  return redirect("/")
