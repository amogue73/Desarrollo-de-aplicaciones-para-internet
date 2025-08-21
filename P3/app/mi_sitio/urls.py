# mi_sitio/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
  
urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('recetas.urls')),
  path('detalles/', include('recetas.urls')),
  path('prueba/', include('recetas.urls')),
  path('__debug__/', include('debug_toolbar.urls')),
  path('accounts/', include('django.contrib.auth.urls')),

]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


