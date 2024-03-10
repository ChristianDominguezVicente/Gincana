from django import forms
from .models import Gincana, Profesor
from django.contrib.admin.widgets import AdminDateWidget

class GincanaForm(forms.ModelForm):
    class Meta:
        model = Gincana
        fields = ['titulo', 'descripcion', 'visibilidad']

class ProfesorForm(forms.ModelForm):
    telefono = forms.IntegerField(label = 'Telefóno', widget=forms.NumberInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su telefono',
            'id': 'telefono',
            'required': 'required'
        }
    ), initial=0) 

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
        fields = ['email', 'nombre', 'apellidos', 'genero', 'organizacion']
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
            'organizacion': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese la organización a la que pertenece'
                }
            )
        }
