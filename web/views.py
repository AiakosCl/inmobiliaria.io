from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from web.models import *
from web.forms import *

# Create your views here.

iconos = {
    'ok':'👌🏼',
    'mal':'👎🏼'
}

class Login(LoginView):
    template_name="registration/login.html"

class Logout(LogoutView):
    next_page="/"

# -- Funciones auxiliares -- #

def index(request):
    inmuebles = Inmueble.objects.filter(estado_inmueble = 'disponible').order_by('-fecha_creacion')
    if request.user.is_authenticated and request.user.tipo_usuario == 'arrendador':
        inmuebles_arrendador = Inmueble.objects.filter(arrendador_id = request.user.id)
        #Determina cuántos mensajes pendientes tiene el arrendador, relacionando los mensajes registrados en sus inmuebles.
        mensajes_pendientes = Mensajes.objects.filter(estado = 'pendiente', inmueble__in = inmuebles_arrendador).count()
    else:
        mensajes_pendientes = 0

    return render(request, 'index.html', {'inmuebles': inmuebles, 'mensajes_pendientes': mensajes_pendientes})


# --- Vistas de Dashboard ---
@login_required
def dashboard_arrendador(request):
    if request.user.is_authenticated:
        inmuebles = Inmueble.objects.filter(arrendador=request.user)
        inmuebles_disponibles = inmuebles.filter(estado_inmueble='disponible').count()
        inmuebles_arrendados = inmuebles.filter(estado_inmueble='arrendado').count()
        ocupacion = (inmuebles_arrendados / inmuebles.count())*100
        total_arriendos = inmuebles.filter(estado_inmueble='arrendado').aggregate(Sum('precio'))['precio__sum']

        
        context = {
            'inmuebles_disponibles': inmuebles_disponibles,
            'inmuebles_arrendados': inmuebles_arrendados,
            'ocupacion': ocupacion,
            'cobro_total': total_arriendos
        }
        
        return render(request, 'dashboard_arrendador.html', context)
    else:
        # Manejar el caso cuando el usuario no está autenticado
        return render(request, 'acceso_denegado.html')



# --- Vistas de Avisos / Publicaciones ---
@login_required
def nuevo_aviso(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    es_edicion = False

    if request.method == 'POST':
        formulario = AvisoForm(request.POST, request.FILES, request=request)

        if formulario.is_valid():
            aviso = formulario.save(commit=False)
            aviso.save()
            messages.success(request, f'{iconos["ok"]}\t¡La publicación se ha creado con éxito!')
            return redirect('PreviewAviso', id_publicacion=aviso.id_publicacion)
        else:
            messages.error(request,f'{iconos["mal"]}\tUPS! Por favor, revisar la información ingresada.')
    else:
        formulario = AvisoForm(request=request)
    
    contextos = {
        'formulario': formulario,
        'regiones': regiones,
        'comunas': comunas,
        'es_edicion': es_edicion

    }
    return render(request, 'publicacion_form.html', contextos)

@login_required
def editar_aviso(request, aviso_id):
    inmueble = get_object_or_404(Inmueble, pk=aviso_id)
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    es_edicion = True
    if request.method == 'POST':
        formulario = AvisoForm(request.POST, request.FILES, instance=inmueble, request=request)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'{iconos["ok"]}\tSe ha editado la publicación.')
            return redirect('ListaAvisos')
        else:
            messages.error(request,f'{iconos["mal"]}\tUps! Algo salió mal. Revisar la inforamción ingresada.')
    else:
        formulario = AvisoForm(instance=inmueble, request=request)
    
    contextos = {
        'formulario': formulario,
        'regiones': regiones,
        'comunas': comunas,
        'es_edicion': es_edicion

    }

    return render(request, 'publicacion_form.html',contextos)

def obtener_comunas(request, region_id):
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
    return JsonResponse(list(comunas), safe=False)

def filtrar_inmuebles(request):
    criterio = request.GET.get('q')
    inmuebles = Inmueble.objects.filter(estado_inmueble='disponible').order_by('-fecha_creacion')

    if criterio:
        seleccion = inmuebles.filter(
                Q(comuna_id__nombre__icontains=criterio)|Q(region_id__nombre__icontains=criterio)
            )

        if not seleccion:
            messages.error(request, f'{iconos["mal"]}\tNo se encontraron resultados para "{criterio}"')
        else:
            messages.success(request, f'{iconos["ok"]}\tSe encontraron {len(seleccion)} resultados para "{criterio}"')
    else:
        seleccion = inmuebles

    return render(request, 'index.html', {'inmuebles':seleccion, 'seccion':'contenido'})

@login_required
def detalle_aviso(request, id_publicacion):
    inmueble = get_object_or_404(Inmueble, id_publicacion=id_publicacion)
    return render(request, 'aviso_detalle.html', {'inmueble':inmueble})

@login_required
def vista_aviso(request, id_publicacion):
    inmueble = get_object_or_404(Inmueble, id_publicacion=id_publicacion)
    inmueble.visitas +=1
    inmueble.save()
    return render(request, 'detalle_inmueble.html', {'inmueble':inmueble})

@login_required
def lista_avisos(request):
    avisos = Inmueble.objects.all().order_by('-fecha_creacion')
    return render(request, 'lista_avisos.html', {'avisos':avisos})

@login_required
def filtraravisos(request):
    criterio = request.GET.get('q')
    if request.user.is_staff or request.user.is_superuser:
        avisos = Inmueble.objects.all().order_by('-fecha_creacion')
    else:
        avisos = Inmueble.objects.filter(arrendador=request.user).order_by('-fecha_creacion')

    if criterio:
        avisos = avisos.filter(
                Q(comuna_id__nombre__icontains=criterio)|Q(region_id__nombre__icontains=criterio)|
                Q(nombre__icontains=criterio)|Q(arrendador_id__first_name__icontains=criterio)|Q(arrendador_id__last_name__icontains=criterio)|
                Q(estado_inmueble__icontains=criterio)
            )
        if not avisos:
            messages.error(request, f'{iconos["mal"]}\tUPS!No se encontraron resultados para "{criterio}"')
    
    return render(request, 'lista_avisos.html', {'avisos':avisos, 'seccion':'avisos'})

@login_required
def eliminar_aviso(request, aviso_id):
    if request.user.is_superuser or request.user.is_staff:    
        try:
            aviso = Inmueble.objects.get(pk=aviso_id)
        except Inmueble.DoesNotExist:
            return "Producto no se encuenta"
        
        if request.method == 'POST':
            aviso.delete()
            messages.success(request, f'{iconos["ok"]}\tSe ha eliminado la publicación.')
            return redirect('ListaAvisos')
        
        return render(request, 'aviso_eliminar.html', {'aviso':aviso})
    else:
        messages.warning(request,f'{iconos["mal"]}\tUsted no está autorizado para esta operación')
        return redirect('inicio')





# --- Vistas de usuarios ---
def nuevo_usuario(request):
    if request.method=='POST':
        formulario = NuevoUsuarioForm(request.POST)
        if formulario.is_valid():
            try:
                usuario = formulario.save(commit=False)
                usuario.save()
                # login(request, usuario) #Para iniciar sesión automáticamente, si se desea.
                messages.success(request, f'{iconos["ok"]}\t¡Se ha registrado al nuevo usuario!')
                if request.user.is_authenticated:
                    if request.user.is_staff:
                        return redirect('Ficha', usuario_id=usuario.id)
                    else:
                        return redirect('inicio')
                else:
                    return redirect('login')
            except ValueError as e:
                messages.error(request, f'{iconos["mal"]}\tError al crear el usuario: {str(e)}')
        else:
            messages.warning(request,f'{iconos["mal"]}\tUps! Algo salió mal. Revisar la inforamción ingresada.')
    else:
        formulario = NuevoUsuarioForm()
    
    return render(request, 'usuario_nuevo.html', {'formulario':formulario})

@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html',{'lista':usuarios})

@login_required
def vista_ficha(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    return render(request, 'detalle_usuario.html', {'usuario':usuario})

@login_required
def editar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return "Usuario no Existe"
    
    if request.method == 'POST':
        usuario.first_name = request.POST['first_name']
        usuario.last_name = request.POST['last_name']
        usuario.email = request.POST['email']
        usuario.telefono = request.POST['telefono']
        usuario.direccion = request.POST['direccion']
        if request.user.is_superuser or request.user.is_staff:
            usuario.rut = request.POST['rut']
            usuario.tipo_usuario = request.POST['tipo_usuario']
            usuario.is_staff = request.POST['is_staff']
            usuario.is_active = request.POST['is_active']
        
        if request.POST['password']:
            usuario.set_password(request.POST['password']) #set_password establece una password encriptada para la tabla User

        usuario.save()
        
        messages.success(request, f'{iconos["ok"]}\t¡Actualización de datos correcta!')
        
        if request.user.is_superuser or request.user.is_staff: 
            return redirect('ListaUsuarios')
        else:
            return redirect('Ficha', usuario_id=usuario.id)
    
    return render(request, 'usuario_editar.html', {'formulario':usuario})

@login_required
def eliminar_usuario(request, usuario_id):
    if request.user.is_superuser or request.user.is_staff:    
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            return "Usuario no existe"
        
        if request.method == 'POST':
            usuario.delete()
            messages.success(request, f'{iconos["ok"]}\t¡Se ha eliminado el usuario!')
            return redirect('ListaUsuarios')
        
        return render(request, 'usuario_eliminar.html', {'usuario':usuario})
    else:
        messages.warning(request,f'{iconos["mal"]}\tUsted no está autorizado para esta operación')
        return redirect('inicio')

@login_required    
def filtrarUsuarios(request):
    termino = request.GET.get('q')
    usuarios = Usuario.objects.all()

    if termino:
        usuarios = usuarios.filter(
            Q(first_name__icontains=termino)|Q(last_name__icontains=termino)
        )
    
    return render(request, 'lista_usuarios.html',{'lista':usuarios})




@login_required
def publicacion(request, id_publicacion=None):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    if id_publicacion:
        # Edición de publicación
        try:
            publicacion = Inmueble.objects.get(id_publicacion=id_publicacion)
        except Inmueble.DoesNotExist:
            messages.error(request,f'{iconos["mal"]}\tLa publicación solicitada no existe.')
            return redirect('inicio')  # Redirigir si la publicación no existe
        
        formulario = AvisoForm(instance=publicacion)
        es_edicion = True
    else:
        # Nueva publicación
        formulario = AvisoForm()
        es_edicion = False

    if request.method == 'POST':
        if es_edicion:
            formulario = AvisoForm(request.POST, request.FILES, instance=publicacion)
        else:
            formulario = AvisoForm(request.POST, request.FILES)

        if formulario.is_valid():
            aviso = formulario.save(commit=False)
            aviso.save()
            if es_edicion:
                messages.success(request, f'{iconos["ok"]}\tLa publicación ha sido actualizada exitosamente.')
                return ('ListaAvisos')
            else:
                messages.success(request, f'{iconos["ok"]}\tLa publicación ha sido creada exitosamente.')
            return redirect('PreviewAviso', id_publicacion=aviso.id_publicacion)

    context = {
        'formulario': formulario,
        'es_edicion': es_edicion,
        'regiones': regiones,
        'comunas': comunas
    }
    return render(request, 'publicacion_form.html', context)