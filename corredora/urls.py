"""
URL configuration for corredora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from web.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name='inicio'),
    path('preview-avosp/<uuid:id_publicacion>/', nuevo_aviso, name="PreviewAviso"),
    path('nuevo_aviso/', nuevo_aviso, name="NuevoAviso"),
    path('registro/', nuevo_usuario, name='NuevoUsuario'),
    path('ficha/<int:usuario_id>/', vista_ficha, name='Ficha'),
    path('usuarios/', lista_usuarios, name="ListaUsuarios" ),
    path('editar-usuario/<int:usuario_id>/', editar_usuario, name='EditarUsuario'),
    path('eliminar-usuario/<int:usuario_id>/', eliminar_usuario, name='EliminarUsuario'),
    path('filtrousuarios/', filtrarUsuarios, name='FiltroUsuarios'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
