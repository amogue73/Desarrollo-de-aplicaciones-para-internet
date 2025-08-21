# recetas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detalles/', views.detalles, name='detalles'),
    path('receta/new/', views.receta_new, name='receta_new'),
    path('receta/edit/', views.receta_edit, name='receta_edit'),
    path('receta/delete/', views.receta_delete, name='receta_delete'),
]
