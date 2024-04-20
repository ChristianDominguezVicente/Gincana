from django import forms
from .models import Gincana, Profesor, Verificacion, Pregunta, Respuesta

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
    titulo = forms.CharField(label = 'Titulo', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese el título de la Gincana',
            'id': 'titulo'
        }
    ))

    descripcion = forms.CharField(label = 'Descripción de la Gincana', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese una descripcion',
            'id': 'descripcion'
        }
    ))

    duracion = forms.CharField(label = 'Duración de la Gincana', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese la duración',
            'id': 'duracion'
        }
    ))
    duracion.label=""

    class Meta:
        model = Gincana
        fields = ['titulo', 'descripcion', 'visibilidad', 'duracion', 'imagen']
        widget = {
            'titulo': forms.TextInput(
                attrs = {
                    'class': 'input-box',
                    'placeholder': 'Nombre'
                }
            ),
            'descripcion': forms.TextInput(
                attrs = {
                    'class': 'input-box',
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

    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required'
        }
    ))

    password2 = forms.CharField(label = 'Confirme su Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required'
        }
    ))

    email = forms.EmailField(label = 'Correo Electrónico', widget = forms.EmailInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Correo Electrónico',
            'id': 'email',
            'required': 'required'
        }
    ))

    nombre = forms.CharField(label = 'Nombre', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Nombre',
            'id': 'nombre',
            'required': 'required'
        }
    ))

    apellidos = forms.CharField(label = 'Apellidos', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Apellidos',
            'id': 'apellidos',
            'required': 'required'
        }
    ))

    ciudad = forms.CharField(label = 'Ciudad', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Ciudad',
            'id': 'ciudad',
            'required': 'required'
        }
    ))

    organizacion = forms.CharField(label = 'Organización', widget = forms.TextInput(
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

    nombre = forms.CharField(label = 'Nombre', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Nombre',
            'id': 'nombre',
            'required': 'required'
        }
    ))

    apellidos = forms.CharField(label = 'Apellidos', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Apellidos',
            'id': 'apellidos',
            'required': 'required'
        }
    ))

    ciudad = forms.CharField(label = 'Ciudad', widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su Ciudad',
            'id': 'ciudad',
            'required': 'required'
        }
    ))

    organizacion = forms.CharField(label = 'Organización', widget = forms.TextInput(
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
    email = forms.EmailField(label = 'Correo Electrónico', widget = forms.EmailInput(
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
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required'
        }
    ))

    password2 = forms.CharField(label = 'Confirme su Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'input-box',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required'
        }
    ))

    password1.label=""
    password2.label=""

class PreguntaForm(forms.ModelForm):
    enunciado = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class': 'input-box',
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
            'enunciado': forms.TextInput(
                attrs = {
                    'class': 'input-box',
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
    respuesta = forms.CharField(label = 'Respuesta', widget = forms.TextInput(
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