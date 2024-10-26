from django import forms
from .models import Gincana, Profesor, Verificacion, Pregunta, Respuesta, Parada
from bootstrap_datepicker_plus.widgets import TimePickerInput

class AuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': "input-box",
                'placeholder': "Ingrese su Corro Electrónico",
            }
        )
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': "input-box",
                'placeholder': "Ingrese su Contraseña"
            }
        )
    )
    username.label=""
    password.label=""

class VerificacionForm(forms.ModelForm):
    max_length=4,
    code = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': "input-box",
                'placeholder': "Ingrese su Código"
            }
        )
    )
    code.label=""

    class Meta:
        model = Verificacion
        fields = ['code']
        widget = {
            'code': forms.NumberInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese su código'
                }
            )
        }

class GincanaForm(forms.ModelForm):
    titulo = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': "input-box",
                'placeholder': "Título de la Gincana"
            }
        )
    )
    titulo.label=""

    class Meta:
        model = Gincana
        fields = ['titulo']

class GincanaConfiguracionForm(forms.ModelForm):
    titulo = forms.CharField(label = 'Título:', max_length=128, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese el título de la Gincana',
            'id': 'titulo'
        }
    ))

    descripcion = forms.CharField(label = 'Descripción de la Gincana:', max_length=1000, widget = forms.Textarea(
        attrs = {
            'class': 'input-des',
            'placeholder': 'Ingrese una descripcion',
            'id': 'descripcion'
        }
    ))

    duracion = forms.TimeField(label='Duración de la Gincana', widget=TimePickerInput(
        options={
            "format": "HH:mm",  
            "stepping": 1,       
        },
        attrs={
            'class': 'input-reloj',
            'placeholder': 'Ingrese la duración',
            'id': 'duracion'
        }
    ))
    duracion.label=""

    class Meta:
        model = Gincana
        fields = ['titulo', 'descripcion', 'visibilidad', 'duracion']
        widget = {
            'titulo': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Nombre'
                }
            ),
            'descripcion': forms.Textarea(
                attrs = {
                    'class': 'input-des',
                    'placeholder': 'Ingrese una descripción '
                }
            ),
            'duracion': forms.TimeInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese la duración '
                }
            )
        }

class ProfesorForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(label = 'Fecha de nacimiento', widget = forms.DateInput(
        attrs = {
            'class': 'input-box',
            'type': 'date',
            'id': 'fecha_nacimiento',
            'required': 'required'
        }
    ))

    password1 = forms.CharField(label = 'Contraseña', max_length=128, widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required'
        }
    ))

    password2 = forms.CharField(label = 'Confirme su Contraseña', max_length=128, widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required'
        }
    ))

    email = forms.EmailField(label = 'Correo Electrónico', max_length=254, widget = forms.EmailInput(        
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Correo Electrónico',
            'id': 'email',
            'required': 'required'
        }
    ))

    nombre = forms.CharField(label = 'Nombre', max_length=50, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Nombre',
            'id': 'nombre',
            'required': 'required'
        }
    ))

    apellidos = forms.CharField(label = 'Apellidos', max_length=100, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Apellidos',
            'id': 'apellidos',
            'required': 'required'
        }
    ))

    ciudad = forms.CharField(label = 'Ciudad', max_length=50, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Ciudad',
            'id': 'ciudad',
            'required': 'required'
        }
    ))

    organizacion = forms.CharField(label = 'Organización', max_length=50, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Organización',
            'id': 'ciudad',
            'required': 'required'
        }
    ))

    email.label=""
    nombre.label=""
    apellidos.label=""
    nombre.label=""
    ciudad.label=""
    organizacion.label=""
    fecha_nacimiento.label=""
    password1.label=""
    password2.label=""

    class Meta:
        model = Profesor
        fields = ['email', 'nombre', 'apellidos', 'genero', 'pais', 'ciudad', 'organizacion']
        labels = {
            'genero': "",
            'pais': ""
        }
        widget = {
            'email': forms.EmailInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Correo Electrónico'
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese su nombre'
                }
            ),
            'apellidos': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese sus apellidos'
                }
            ),
            'genero': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese su género'
                }
            ),
            'pais': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese su pais'
                }
            ),
            'ciudad': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese su ciudad'
                }
            ),
            'organizacion': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Ingrese la organización a la que pertenece'
                }
            )
        }

class EditarProfesorForm(forms.ModelForm):
    imagen = forms.ImageField(label = 'Imagen de Perfil', widget = forms.FileInput(
        attrs = {
            'placeholder': 'Ingrese una imagen de perfil',
            'id': 'imagen',
        }
    ))

    fecha_nacimiento = forms.DateField(label = 'Fecha de nacimiento', widget = forms.DateInput(
        attrs = {
            'class': 'input-box',
            'type': 'date',
            'id': 'fecha_nacimiento',
            'required': 'required'
        }
    ))

    nombre = forms.CharField(label = 'Nombre', max_length=50, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Nombre',
            'id': 'nombre',
            'required': 'required'
        }
    ))

    apellidos = forms.CharField(label = 'Apellidos', max_length=100, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Apellidos',
            'id': 'apellidos',
            'required': 'required'
        }
    ))

    ciudad = forms.CharField(label = 'Ciudad', max_length=50, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Ciudad',
            'id': 'ciudad',
            'required': 'required'
        }
    ))

    organizacion = forms.CharField(label = 'Organización', max_length=50, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Organización',
            'id': 'ciudad',
            'required': 'required'
        }
    ))

    nombre.label=""
    apellidos.label=""
    nombre.label=""
    ciudad.label=""
    organizacion.label=""
    fecha_nacimiento.label=""
    
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellidos', 'genero', 'pais', 'ciudad', 'organizacion']
        labels = {
            'genero': "",
            'pais': ""
        }
        widget = {
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

class PasswordForm(forms.ModelForm):
    email = forms.EmailField(label = 'Correo Electrónico', max_length=254, widget = forms.EmailInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Correo Electrónico',
            'id': 'email',
            'required': 'required'
        }
    ))

    email.label=""

    class Meta:
        model = Profesor
        fields = ['email']
        widget = {
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Correo Electrónico'
                }
            )
        }

class PasswordCambioForm(forms.Form):
    password1 = forms.CharField(label = 'Contraseña', max_length=128, widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required'
        }
    ))

    password2 = forms.CharField(label = 'Confirme su Contraseña', max_length=128, widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required'
        }
    ))

    password1.label=""
    password2.label=""

class ParadaForm(forms.ModelForm):
    nombre = forms.CharField(label = 'Nombre de la Parada', max_length=50, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Nombre de la Parada'
        }
    ))

    nombre.label=""

    class Meta:
        model = Parada
        fields = ['nombre']
        widget = {
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Nombre'
                }
            )
        }

class PreguntaForm(forms.ModelForm):
    enunciado = forms.CharField(max_length=254, widget = forms.Textarea(
        attrs = {
            'class': 'input-des',
            'placeholder': 'Enunciado de la Pregunta'
        }
    ))

    num_respuestas = forms.ChoiceField(
        choices=Pregunta.NUM,
        widget=forms.Select(
            attrs={
                'class': 'input-box'
            }
        )
    )

    enunciado.label=""
    num_respuestas.label="Número de Respuestas"

    class Meta:
        model = Pregunta
        fields = ['enunciado', 'num_respuestas']
        widget = {
            'enunciado': forms.Textarea(
                attrs = {
                    'class': 'input-des',
                    'placeholder': 'Enunciado de la Pregunta'
                }
            ),
            'num_respuestas': forms.TextInput(
                attrs = {
                    'class': 'input-box'
                }
            )
        }

class RespuestaForm(forms.ModelForm):
    respuesta = forms.CharField(label = 'Respuesta', max_length=128, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Respuesta'
        }
    ))

    puntos = forms.IntegerField(label = 'Puntos', widget = forms.NumberInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Puntos'
        }
    ))

    respuesta.label=""
    puntos.label=""

    class Meta:
        model = Respuesta
        fields = ['respuesta', 'puntos', 'es_correcta']
        widget = {
            'respuesta': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Respuesta'
                }
            ),
            'puntos': forms.NumberInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Puntos'
                }
            )
        }

class ContactForm(forms.Form):
    asunto = forms.CharField(max_length=100, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese el asunto'
        }
    ))
    descripcion = forms.CharField(label = 'Descripción de la Gincana:', max_length=10000, widget = forms.Textarea(
        attrs = {
            'class': 'input-des',
            'placeholder': 'Ingrese una descripcion'
        }
    ))
    asunto.label=""

class InvitadosForm(forms.Form):
    usuarios = forms.ChoiceField(
        choices=[(1, '1 Invitado'), (5, '5 Invitados'), (10, '10 Invitados'), (15, '15 Invitados'), (20, '20 Invitados'), (25, '25 Invitados')],
        widget=forms.Select(
            attrs={
                'class': 'input-box'
            }
        ),
        label='Número de Invitados'
    )

class AuthenticationInvitadosForm(forms.Form):
    usuario = forms.CharField(max_length=254, widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su usuario'
        }
    ))
    usuario.label=""
