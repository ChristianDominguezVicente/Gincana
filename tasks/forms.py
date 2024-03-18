from django import forms
from .models import Gincana, Profesor
from django.contrib.admin.widgets import AdminDateWidget

class GincanaForm(forms.ModelForm):
    class Meta:
        model = Gincana
        fields = ['titulo']

class GincanaConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Gincana
        fields = ['titulo', 'descripcion', 'visibilidad', 'duracion', 'imagen']
        widget = {
            'titulo': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nombre'
                }
            ),
            'descripcion': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descripción '
                }
            ),
            'duracion': forms.TimeInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese la duración '
                }
            )
        }

class ProfesorForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(label = 'Fecha de nacimiento', widget = forms.DateInput(
        attrs = {
            'class': 'form-control',
            'type': 'date',
            'id': 'fecha_nacimiento',
            'required': 'required'
        }
    ))

    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required'
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de confirmación', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required'
        }
    ))

    class Meta:
        model = Profesor
        fields = ['email', 'nombre', 'apellidos', 'genero', 'pais', 'ciudad', 'organizacion']
        widget = {
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Correo Electrónico'
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre'
                }
            ),
            'apellidos': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos'
                }
            ),
            'genero': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su género'
                }
            ),
            'pais': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su pais'
                }
            ),
            'ciudad': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su ciudad'
                }
            ),
            'organizacion': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese la organización a la que pertenece'
                }
            )
        }
