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
    path('aviso_detalle/<uuid:id_publicacion>/', detalle_aviso, name="PreviewAviso"),
    path('nuevo_aviso/', nuevo_aviso, name="NuevoAviso"),
    path('avisos/', lista_avisos, name="ListaAvisos"),
    path('lista-avisos/', filtraravisos, name="FiltroAvisos"),
    path('eliminar-aviso/<uuid:aviso_id>/', eliminar_aviso, name="EliminarAviso"),
    path('editar-aviso/<uuid:aviso_id>/', editar_aviso, name="EditarAviso"),
    path('aviso/<uuid:id_publicacion>/', vista_aviso, name="VistaAviso"),
    path('registro/', nuevo_usuario, name='NuevoUsuario'),
    path('ficha/<int:usuario_id>/', vista_ficha, name='Ficha'),
    path('dashboard/', dashboard_arrendador, name='Dashboard'),
    path('usuarios/', lista_usuarios, name="ListaUsuarios" ),
    path('editar-usuario/<int:usuario_id>/', editar_usuario, name='EditarUsuario'),
    path('eliminar-usuario/<int:usuario_id>/', eliminar_usuario, name='EliminarUsuario'),
    path('filtrousuarios/', filtrarUsuarios, name='FiltroUsuarios'),
    path('filtro/', filtrar_inmuebles, name='filtro'),
    path('obtener-comunas/<int:region_id>/', obtener_comunas, name='ObtenerComunas'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
