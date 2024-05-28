from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AvisoForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos', 'habitaciones', 'banos', 'direccion', 'region', 'comuna', 'tipo_inmueble', 'precio']
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
            'precio': 'Precio',
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
        aviso = super().save(commit=True)
        aviso.arrendador = self.request.user
        aviso.estado_inmueble = 'disponible'
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


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'rut', 'tipo_usuario', 'is_staff', 'is_active']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'rut': 'RUT',
            'tipo_usuario': 'Tipo de Usuario',
            'is_staff': '¿Es miembro del Staff?',
            'is_active': '¿Está activo?',
        }
        widgets = {
            'tipo_usuario': forms.Select(choices=Usuario.TIPO_USUARIO),
            'is_staff': forms.CheckboxInput(),
            'is_active': forms.CheckboxInput(),
        }
        error_messages = {
            'first_name': {
                'required': 'El campo Nombre es obligatorio.',
                'max_length': 'El Nombre no puede tener más de 30 caracteres.',
            },
            'last_name': {
                'required': 'El campo Apellido es obligatorio.',
                'max_length': 'El Apellido no puede tener más de 30 caracteres.',
            },
            'email': {
                'required': 'El campo Correo Electrónico es obligatorio.',
                'invalid': 'Ingrese un Correo Electrónico válido.',
                'unique': 'Este Correo Electrónico ya está en uso.',
            },
            'telefono': {
                'required': 'El campo Teléfono es obligatorio.',
                'max_length': 'El Teléfono no puede tener más de 20 caracteres.',
            },
            'direccion': {
                'required': 'El campo Dirección es obligatorio.',
                'max_length': 'La Dirección no puede tener más de 255 caracteres.',
            },
            'rut': {
                'required': 'El campo RUT es obligatorio.',
                'unique': 'Este RUT ya está en uso.',
                'max_length': 'El RUT no puede tener más de 9 caracteres.',
            },
            'tipo_usuario': {
                'required': 'El campo Tipo de Usuario es obligatorio.',
                'invalid_choice': 'Seleccione un Tipo de Usuario válido.',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user