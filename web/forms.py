from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AvisoForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos', 'habitaciones', 'banos', 'direccion', 'region', 'comuna', 'tipo_inmueble', 'estado_inmueble','precio','imagen','visitas']
        labels = {
            'nombre': 'Título de la publicación:',
            'descripcion': 'Descripción del Inmueble:',
            'm2_construidos': 'Metros Cuadrados Construidos:',
            'm2_totales': 'Metros Cuadrados Totales:',
            'estacionamientos': 'Cantidad de Estacionamientos:',
            'habitaciones': 'Cantidad de Habitaciones:',
            'banos': 'Cantidad de Baños:',
            'direccion': 'Dirección del inmueble:',
            'region': 'Región:',
            'comuna': 'Comuna:',
            'tipo_inmueble': 'Tipo de Inmueble:',
            'estado_inmueble': 'Estado disponibilidad:',
            'precio': 'Precio',
            'imagen': 'Fotografía de la propiedad:',
            'visitas': 'Cantidad de visualizaciones:',
        }

        error_messages ={
            'nombre': {
                'required': 'Este dato es obligatorio.',
                'max_length': 'Excede el máximo de caracteres',
            },
            'descripcion': {
                'required': 'Este dato es obligatorio.',
            },
            'm2_construidos': {
                'required': 'Este dato es obligatorio.',
            },
            'm2_totales': {
                'required': 'Este dato es obligatorio.',
            },
            'estacionamientos': {
                'required': 'Este dato es obligatorio.',
            },
            'precio': {
                'required': 'Este dato es obligatorio.',
            },
            'habitaciones': {
                'required': 'Este dato es obligatorio.',
            },
            'banos': {
                'required': 'Este dato es obligatorio.',
            },
            'direccion': {
                'required': 'Este dato es obligatorio.',
            },
            'region': {
                'required': 'Este dato es obligatorio.',
                'invalid_choice': 'Ingreso no válido.',
            },
            'comuna': {
                'required': 'Este dato es obligatorio.',
                'invalid_choice': 'Ingreso no válido.',
            },
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        aviso = super().save(commit=False)
        aviso.arrendador_id = self.request.user.id
        if commit:
            aviso.save()
        return aviso


class NuevoUsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Ingrese su nombre.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Ingrese su Apellido.')

    class Meta:
        model = Usuario
        fields = ('username','first_name', 'last_name','password1','password2','rut', 'direccion','telefono','tipo_usuario')
        labels = {
            'username':'Nombre de usuario (correo electrónico):',
            'first_name': 'Nombre(s):',
            'last_name':'Apellido(s):',
            'password1':'Ingrese su contraseña:',
            'password2':'Repita su contraseña:',
            'rut':'Rut:',
            'telefono':'Número de contacto:',
            'direccion':'Dirección particular:',
            'tipo_usuario':'Tipo de perfil:',
        }

        error_messages = {
            'username': {
                'unique': 'El nombre de usuario ya existe',
            },
            'first_name': {
                'required': 'Este dato es obligatorio.'
            },
            'last_name': {
                'required': 'Este dato es obligatorio.'
            },
            'rut': {
                'required': 'Este dato es obligatorio.',
                'unique': 'El rut ya existe',
                'max-lenght': 'Excede el tamaño de caracteres (%max_length%).',
            },
            'direccion': {
                'required': 'Este dato es obligatorio.',
            },
            'telefono': {
                'required': 'Este dato es obligatorio.',
            },
            'password1': {
                'required': 'Este dato es obligatorio.',
                'password_mismatch': 'Las contraseñas no coinciden',
                'password_too_short': 'La contraseña debe tener al menos 8 caracteres',
                'password_entirely_numeric': 'La contraseña debe tener a lo menos letra y/o un símbolo',
                'password_entirely_alphanumeric': 'La contraseña debe tener a lo menos un número y/o símbolo',
                'password_entirely_symbolic': 'La contraseña debe tener a lo menos un número y/o letra',
                'password_too_common': 'La contraseña es muy común',
            },
            'password2': {
                'required': 'Este dato es obligatorio.',
                'password_mismatch': 'Las contraseñas no coinciden',
                'password_too_short': 'La contraseña debe tener al menos 8 caracteres',
                'password_entirely_numeric': 'La contraseña debe tener a lo menos letra y/o un símbolo',
                'password_entirely_alphanumeric': 'La contraseña debe tener a lo menos un número y/o símbolo',
                'password_entirely_symbolic': 'La contraseña debe tener a lo menos un número y/o letra',
                'password_too_common': 'La contraseña es muy común',
            },
            'tipo_usuario': {
                'required': 'Este dato es obligatorio.',
            },
        }

    # Acá se replicará el nombre de usuario en el campo correo.
    def save(self, commit=True):
        user = super().save(commit=True)
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user
    
    
# class ContactoForm(forms.ModelForm):
#     class Meta:
#         model = Mensajes
#         fields = ['NombreCliente','EmailCliente', 'Mensaje']
#         labels = {
#             'NombreCliente': 'Su nombre:',
#             'EmailCliente':'Correo electrónico:',
#             'Mensaje':'Motivo de su contacto:'
#         }


# forms.py

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'rut', 'tipo_usuario', 'is_staff', 'is_active']

    password = forms.CharField(required=False, widget=forms.PasswordInput, help_text='Dejar en blanco para no cambiar.')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
