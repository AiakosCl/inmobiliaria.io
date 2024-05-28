from django.contrib import admin
from .models import *

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'tipo_usuario', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')

class InumeblesAdmin(admin.ModelAdmin):
    list_display = ('id_publicacion', 'nombre', 'tipo_inmueble', 'estado_inmueble')




admin.site.register(Usuario, UsersAdmin)
admin.site.register(Inmueble, InumeblesAdmin)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Mensajes)
admin.site.register(SolicitudArriendo)
admin.site.register(Respuestas)