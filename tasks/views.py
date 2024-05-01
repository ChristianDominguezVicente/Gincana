from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils.datastructures import MultiValueDictKeyError
from .forms import GincanaForm, ProfesorForm, GincanaConfiguracionForm, EditarProfesorForm, VerificacionForm, PasswordForm, PasswordCambioForm, AuthenticationForm, PreguntaForm, RespuestaForm
from .models import Gincana, Profesor, Verificacion, Parada, Pregunta, Respuesta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import datetime, random, json, folium, time, os
from selenium import webdriver
from django.conf import settings
import shutil

# Create your views here.

@login_required
def home(request):
    mis_gincanas = Gincana.objects.filter(email_profesor=request.user)
    gincanas_publicas = Gincana.objects.filter(visibilidad=True).order_by('-edicion')
    profesores = Profesor.objects.filter(email=request.user.email)
    return render(request, 'home.html',{'mis_gincanas': mis_gincanas, 'gincanas_publicas': gincanas_publicas, 'profesores': profesores})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request, 'signup.html', {
                'form': ProfesorForm
            })
        else:
            if Profesor.objects.filter(email=request.POST['email']):
                return render(request, 'signup.html', {
                    'form': ProfesorForm,
                    'error': 'El usuario ya existe.'
                })
            else:
                if request.POST['password1'] == request.POST['password2']:
                    d = datetime.datetime.strptime(request.POST['fecha_nacimiento'], '%Y-%m-%d').date()
                    edad = date.today().year - d.year -((date.today().month, date.today().day) <(d.month, d.day))
                    if edad >= 18:
                        try:
                            temp = Profesor.objects.create_temp_user(email=request.POST['email'],
                                nombre=request.POST['nombre'],
                                apellidos=request.POST['apellidos'],
                                fecha_nacimiento=request.POST['fecha_nacimiento'],
                                genero=request.POST['genero'],
                                pais=request.POST['pais'],
                                ciudad=request.POST['ciudad'],
                                organizacion=request.POST['organizacion'],
                                password=request.POST['password1'])

                            if validate_password(request.POST['password1'], temp) is None:

                                user = Profesor.objects.create_user(email=request.POST['email'],
                                    nombre=request.POST['nombre'],
                                    apellidos=request.POST['apellidos'],
                                    fecha_nacimiento=request.POST['fecha_nacimiento'],
                                    genero=request.POST['genero'],
                                    pais=request.POST['pais'],
                                    ciudad=request.POST['ciudad'],
                                    organizacion=request.POST['organizacion'],
                                    password=request.POST['password1'])

                                user.save()
                                num=random.randint(0,9999)
                                Verificacion.objects.create(code=num, email=user.email)

                                send_mail(
                                    subject='Código de Verificación',
                                    message=str(num),
                                    from_email='herstorygincanas@gmail.com',
                                    recipient_list=[user.email]
                                )
                                
                                return redirect('verificacion', email=user.email)
                        except ValidationError as e:
                            return render(request, 'signup.html', {
                                'form': ProfesorForm,
                                'error': e
                            })
                    else:
                        return render(request, 'signup.html', {
                            'form': ProfesorForm,
                            'error': 'Para registrarse necesita tener 18 años mínimo.'
                        })
                else:
                    return render(request, 'signup.html', {
                        'form': ProfesorForm,
                        'error': 'Las contraseñas no coinciden'
                    })
                
def verificacion(request, email):
    if request.method == 'GET':
            return render(request, 'verificacion.html', {
                'form': VerificacionForm,
                'email': email
            })
    else:
        form = VerificacionForm(request.POST)
        if Verificacion.objects.filter(code=request.POST['code'],email=email):
            user = get_object_or_404(Profesor, pk=email)
            user.usuario_verificado=True
            user.save()
            code = get_object_or_404(Verificacion, email=user.email)
            code.delete()
            login(request, user)
            return redirect('home')
        else:
            form = VerificacionForm()
            return render(request, 'verificacion.html',{'form': form, 'error': 'No es el código de verificación.', 'email': email})

def verificacion_reenviar(request, email):
    if request.method == "POST":
        num=random.randint(0,9999)
        user = Verificacion.objects.get(email=email)
        user.code = num
        user.save()
        send_mail(
            subject='Código de Verificación',
            message=str(num),
            from_email='herstorygincanas@gmail.com',
            recipient_list=[email]
        )
        return redirect('verificacion', email=email)
    
def password(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request, 'password.html', {
                'form': PasswordForm
            })
        else:
            profesor = get_object_or_404(Profesor, pk=request.POST['email'])
            if not Profesor.objects.filter(email=request.POST['email']):
                return render(request, 'password.html', {
                    'form': PasswordForm,
                    'error': 'El usuario no existe.'
                })
            elif profesor.usuario_verificado == False:
                return redirect('verificacion', email=request.POST['email'])
            else:
                send_mail(
                    subject='Cambio de Contraseña',
                    message='http://127.0.0.1:8000/password/' + request.POST['email'] + '/',
                    from_email='herstorygincanas@gmail.com',
                    recipient_list=[request.POST['email']]
                )
                
                return redirect('password')
        
def password_cambio(request, email):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request, 'password_cambiar.html', {
                'form': PasswordCambioForm
            })
        else:
            if not Profesor.objects.filter(email=email):
                return render(request, 'password.html', {
                    'form': PasswordForm,
                    'error': 'El usuario no existe.'
                })
            else:
                if request.POST['password1'] == request.POST['password2']:
                    profesor = get_object_or_404(Profesor, pk=email)
                    try:
                        temp = Profesor.objects.create_temp_user(email=profesor.email,
                                nombre=profesor.nombre,
                                apellidos=profesor.apellidos,
                                fecha_nacimiento=profesor.fecha_nacimiento,
                                genero=profesor.genero,
                                pais=profesor.pais,
                                ciudad=profesor.ciudad,
                                organizacion=profesor.organizacion,
                                password=request.POST['password1'])

                        if validate_password(request.POST['password1'], temp) is None:
                            user = Profesor.objects.create_user(email=profesor.email,
                                    nombre=profesor.nombre,
                                    apellidos=profesor.apellidos,
                                    fecha_nacimiento=profesor.fecha_nacimiento,
                                    genero=profesor.genero,
                                    pais=profesor.pais,
                                    ciudad=profesor.ciudad,
                                    organizacion=profesor.organizacion,
                                    password=request.POST['password1'])
                            user.usuario_verificado=True
                            user.save()
                            return redirect('signin')
                    except ValidationError as e:
                        return render(request, 'password_cambiar.html', {
                            'form': PasswordCambioForm,
                            'error': e
                        })
                else:
                    return render(request, 'password_cambiar.html', {
                        'form': PasswordCambioForm,
                        'error': 'Las contraseñas no coinciden'
                    })

@login_required
def gincanas(request):
    gincanas = Gincana.objects.filter(email_profesor=request.user)
    profesores = Profesor.objects.filter(email=request.user.email)
    return render(request, 'mis_gincanas.html',{'gincanas': gincanas, 'profesores': profesores})

@login_required
def gincanas_publicas(request):
    gincanas = Gincana.objects.filter(visibilidad=True).order_by('-edicion')
    profesores = Profesor.objects.filter(email=request.user.email)
    return render(request, 'gincanas_publicas.html',{'gincanas': gincanas, 'profesores': profesores})

@login_required
def crear_gincana(request):
    profesores = Profesor.objects.filter(email=request.user.email)
    if request.method == 'GET':
        return render(request, 'crear_gincana.html',{
            'form': GincanaForm, 
            'profesores': profesores
        })
    else:
        try:
            form = GincanaForm(request.POST)
            nueva_Gincana = form.save(commit=False)
            nueva_Gincana.email_profesor = request.user
            nueva_Gincana.save()
            return redirect('mis_gincanas')
        except ValueError:
            return render(request, 'crear_gincana.html',{
                'form': GincanaForm,
                'error': 'Los datos no son válidos',
                'profesores': profesores
            })

@login_required
def gincana(request, gincana_id):  
    profesores = Profesor.objects.filter(email=request.user.email)
    if request.method == 'GET':
        gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
        paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
        paradas_data = []
        for parada in paradas:
            pregunta = parada.pregunta_set.first()
            respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
            parada_data = {
                'latitud': parada.latitud,
                'longitud': parada.longitud,
                'pregunta': pregunta.enunciado if pregunta else None,
                'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
            }
            paradas_data.append(parada_data)
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data})
    else:
        try:
            gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
            paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
            paradas_data = []
            for parada in paradas:
                pregunta = parada.pregunta_set.first()
                respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
                parada_data = {
                    'latitud': parada.latitud,
                    'longitud': parada.longitud,
                    'pregunta': pregunta.enunciado if pregunta else None,
                    'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
                }
                paradas_data.append(parada_data)
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data})
        except ValueError:
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 
                'error': "Error actualizando la Gincana"})

@login_required        
def editar_gincana(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    paradas = Parada.objects.filter(gincana=gincana)
    contador = paradas.count()

    if contador > 0 and contador != paradas.last().orden:
        for index, parada in enumerate(paradas, start=1):
            Parada.objects.filter(pk=parada.pk).update(orden=index)
    
    paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
    paradas_data = []
    for parada in paradas:
        pregunta = parada.pregunta_set.first()
        respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
        parada_data = {
            'latitud': parada.latitud,
            'longitud': parada.longitud,
            'pregunta': pregunta.enunciado if pregunta else None,
            'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
        }
        paradas_data.append(parada_data)

    for parada in paradas:
        pregunta = parada.pregunta_set.first()
        respuestas = pregunta.respuesta_set.all() if pregunta else []

        parada.pregunta = pregunta
        parada.respuestas = respuestas

    return render(request, 'editar_gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'db': paradas})

@login_required        
def configuracion_gincana(request, gincana_id):  
    profesores = Profesor.objects.filter(email=request.user.email)
    if request.method == 'GET':
        gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
        paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
        paradas_data = []
        for parada in paradas:
            pregunta = parada.pregunta_set.first()
            respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
            parada_data = {
                'latitud': parada.latitud,
                'longitud': parada.longitud,
                'pregunta': pregunta.enunciado if pregunta else None,
                'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
            }
            paradas_data.append(parada_data)
        form = GincanaConfiguracionForm(instance=gincana)
        return render(request, 'configuracion_gincana.html', {'gincana': gincana,'form': form, 'profesores': profesores, 'paradas': paradas_data})
    else:
        try:
            gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
            paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
            paradas_data = []
            for parada in paradas:
                pregunta = parada.pregunta_set.first()
                respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
                parada_data = {
                    'latitud': parada.latitud,
                    'longitud': parada.longitud,
                    'pregunta': pregunta.enunciado if pregunta else None,
                    'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
                }
                paradas_data.append(parada_data)
            form = GincanaConfiguracionForm(request.POST, instance=gincana)
            form.save()
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data})
        except ValueError:
            return render(request, 'configuracion_gincana.html', {'gincana': gincana, 'form': form,
                'profesores': profesores, 'error': "Error actualizando la Gincana"})

@login_required        
def puntuacion_gincana(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    return render(request, 'puntuacion_gincana.html', {'gincana': gincana, 'profesores': profesores})

@login_required        
def gincana_publica(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
    paradas_data = []
    for parada in paradas:
        pregunta = parada.pregunta_set.first()
        respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
        parada_data = {
            'latitud': parada.latitud,
            'longitud': parada.longitud,
            'pregunta': pregunta.enunciado if pregunta else None,
            'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
        }
        paradas_data.append(parada_data)
    return render(request, 'gincana_publica.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data})

@login_required
def gincana_iniciar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    profesores = Profesor.objects.filter(email=request.user.email)
    if request.method == "POST" and gincana.activa == False and gincana.duracion is not None :
        gincana.activa = True
        gincana.save()
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores})
    elif request.method == "POST" and gincana.activa == True and gincana.duracion is not None :
        gincana.activa = False
        gincana.edicion = timezone.now()
        gincana.save()
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores})
    else:
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 
            'error': "Se necesita primero establecer una duración a la gincana."})

@login_required
def gincana_copiar(request, gincana_id):
    gincanas = Gincana.objects.filter(email_profesor=request.user)
    profesores = Profesor.objects.filter(email=request.user.email)
    nueva_Gincana = Gincana.objects.get(pk=gincana_id)
    paradas = Parada.objects.filter(gincana=gincana_id).order_by('orden')
    paradas_gincana = list(paradas.values('latitud', 'longitud'))
    if nueva_Gincana.email_profesor == request.user:
        return render(request, 'gincana_publica.html', {'gincana': nueva_Gincana, 'gincanas': gincanas, 'profesores': profesores,
            'paradas': paradas_gincana, 'error': "Esta Gincana ya te pernetece."})
    else:
        nueva_Gincana.pk = None
        nueva_Gincana.email_profesor = request.user
        nueva_Gincana.save()
        for parada in paradas:
            nueva_parada = Parada.objects.create(
                orden=parada.orden,
                latitud=parada.latitud,
                longitud=parada.longitud,
                gincana=nueva_Gincana
            )
            nueva_parada.save()

            if Pregunta.objects.filter(parada_id=parada.id).exists():
                pregunta = Pregunta.objects.get(parada_id=parada.id)
                nueva_pregunta = Pregunta.objects.create(
                    enunciado=pregunta.enunciado,
                    parada_id=nueva_parada.id,
                    num_respuestas=pregunta.num_respuestas
                )
                nueva_pregunta.save()

                respuestas = Respuesta.objects.filter(pregunta_id=pregunta.id)
                for respuesta in respuestas:
                    nueva_respuesta = Respuesta.objects.create(
                        respuesta=respuesta.respuesta,
                        puntos=respuesta.puntos,
                        pregunta_id=nueva_pregunta.id,
                        es_correcta=respuesta.es_correcta
                    )
                    nueva_respuesta.save()
        return render(request, 'mis_gincanas.html', {'gincana': nueva_Gincana, 'gincanas': gincanas, 'profesores': profesores, 'paradas': paradas_gincana})

@login_required    
def gincana_eliminar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    if request.method == "POST":
        gincana.delete()
        return redirect('mis_gincanas')

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'GET':
            return render(request, 'signin.html',{
                'form': AuthenticationForm
            })
        else:
            profesor = get_object_or_404(Profesor,pk=request.POST['username'])
            if profesor.usuario_verificado == False:
                return redirect('verificacion', email=request.POST['username'])
            else:
                user = authenticate(request, username=request.POST['username'], 
                    password=request.POST['password'])

                if user is None:
                    return render(request, 'signin.html',{
                        'form': AuthenticationForm,
                        'error': 'El usuario o la contraseña es incorrecto'
                    })
                else:
                    login(request, user)
                    return redirect('home')
        
def informacion(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'informacion.html')

@login_required
def profesor(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    if request.method == 'GET':
        profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
        return render(request, 'profesor.html', {'profesor': profesor, 'profesores': profesores})
    else:
        try:
            profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
            return redirect('verificacion_password', email_id=request.user.email)
        except ValueError:
            return render(request, 'profesor.html', {'profesor': profesor, 'profesores': profesores, 
                'error': "Error actualizando el Perfil"})

@login_required     
def verificacion_password(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    if request.method == 'GET':
        return render(request, 'verificacion_password.html', {
            'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores
        })
    else:
        profesor = get_object_or_404(Profesor, pk=email_id)
        if profesor.email == request.POST['username']:
            user = authenticate(request, username=request.POST['username'], 
                        password=request.POST['password'])
            if user is None:
                return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'La contraseña no es correcta',
                    'profesor': profesor,'profesores': profesores
                })
            else:
                return redirect('editar_profesor', email_id=email_id)
        else:
            return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'Introduzca su Correo Electrónico',
                    'profesor': profesor,'profesores': profesores
                })
        
@login_required     
def verificacion_password2(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    if request.method == 'GET':
        return render(request, 'verificacion_password.html', {
            'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores
        })
    else:
        try:
            profesor = get_object_or_404(Profesor, pk=email_id)
            if profesor.email == request.POST['username']:
                user = authenticate(request, username=request.POST['username'], 
                            password=request.POST['password'])
                if user is None:
                    return render(request, 'verificacion_password.html', {
                        'form': AuthenticationForm, 'email_id': email_id, 'error': 'La contraseña no es correcta',
                        'profesor': profesor,'profesores': profesores
                    })
                else:
                    return redirect('profesor_password', email_id=email_id)
            else:
                return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'Introduzca su Correo Electrónico',
                    'profesor': profesor,'profesores': profesores
                })
        except MultiValueDictKeyError:
            return render(request, 'verificacion_password.html', {
                'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores
            })

@login_required     
def profesor_eliminar(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    if request.method == 'GET':
        return render(request, 'verificacion_password.html', {
            'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores
        })
    else:
        try:
            profesor = get_object_or_404(Profesor, pk=email_id)
            user = authenticate(request, username=request.POST['username'], 
                        password=request.POST['password'])
            if user is None:
                return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'La contraseña no es correcta',
                    'profesor': profesor,'profesores': profesores
                })
            else:
                profesor.delete()
                return redirect('signin')
        except MultiValueDictKeyError:
            return render(request, 'verificacion_password.html', {
                'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores
            })

@login_required 
def editar_profesor(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    if request.method == 'GET':
        profesor = get_object_or_404(Profesor, pk = email_id, email = request.user.email)
        form = EditarProfesorForm(instance=profesor)
        return render(request, 'editar_profesor.html', {'profesor': profesor, 'form': form, 'profesores': profesores})
    else:
        try:
            profesor = get_object_or_404(Profesor, pk = email_id, email = request.user.email)
            form = EditarProfesorForm(request.POST, request.FILES, instance=profesor)
            d = datetime.datetime.strptime(request.POST['fecha_nacimiento'], '%Y-%m-%d').date()
            edad = date.today().year - d.year -((date.today().month, date.today().day) <(d.month, d.day))
            if edad >= 18:
                profesor.fecha_nacimiento=request.POST['fecha_nacimiento']
                profesor.imagen=request.FILES['imagen']
                form.save()
                return redirect('profesor', email_id=request.user.email)
            else:
                return render(request, 'editar_profesor.html', {
                    'profesor': profesor, 'profesores': profesores,
                    'form': EditarProfesorForm,
                    'error': 'Para registrarse necesita tener 18 años mínimo.'
                })
        except MultiValueDictKeyError:
            return render(request, 'editar_profesor.html', {'profesor': profesor, 'form': form,
                'profesores': profesores, 'error': "Error actualizando el Perfil"})
    
@login_required
def profesor_password(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    if request.method == 'GET':
        return render(request, 'profesor_password.html', {
            'form': PasswordCambioForm,
            'profesor': profesor, 'profesores': profesores
        })
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                profesor = get_object_or_404(Profesor, pk=email_id)
                try:
                    temp = Profesor.objects.create_temp_user(email=profesor.email,
                            nombre=profesor.nombre,
                            apellidos=profesor.apellidos,
                            fecha_nacimiento=profesor.fecha_nacimiento,
                            genero=profesor.genero,
                            pais=profesor.pais,
                            ciudad=profesor.ciudad,
                            organizacion=profesor.organizacion,
                            password=request.POST['password1'])
                    if validate_password(request.POST['password1'], temp) is None:
                        logout(request)
                        user = Profesor.objects.create_user(email=profesor.email,
                                nombre=profesor.nombre,
                                apellidos=profesor.apellidos,
                                fecha_nacimiento=profesor.fecha_nacimiento,
                                genero=profesor.genero,
                                pais=profesor.pais,
                                ciudad=profesor.ciudad,
                                organizacion=profesor.organizacion,
                                password=request.POST['password1'])
                        user.usuario_verificado=True
                        user.save()
                        login(request, user)
                        return redirect('profesor', email_id=user.email)
                except ValidationError as e:
                    return render(request, 'profesor_password.html', {
                        'form': PasswordCambioForm,
                        'error': e,
                        'profesor': profesor, 'profesores': profesores
                    })
            else:
                return render(request, 'profesor_password.html', {
                    'form': PasswordCambioForm,
                    'error': 'Las contraseñas no coinciden',
                    'profesor': profesor, 'profesores': profesores
                })
        except MultiValueDictKeyError:
            return render(request, 'profesor_password.html', {
                'form': PasswordCambioForm,
                'profesor': profesor, 'profesores': profesores
            })
        
@login_required
def parada(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
    paradas_data = []
    for parada in paradas:
        pregunta = parada.pregunta_set.first()
        respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
        parada_data = {
            'latitud': parada.latitud,
            'longitud': parada.longitud,
            'pregunta': pregunta.enunciado if pregunta else None,
            'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
        }
        paradas_data.append(parada_data)
    return render(request, 'parada.html', {'gincana': gincana, 'paradas': paradas_data})

@login_required
def parada_guardar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    contador = Parada.objects.filter(gincana=gincana).count()
    paradas_data = json.loads(request.POST.get('parada'))

    for latitud, longitud in paradas_data.items():
        contador += 1
        if not Parada.objects.filter(latitud=latitud, longitud=longitud, gincana_id=gincana_id).exists():
            parada= Parada.objects.create(
                orden=contador,
                latitud=latitud,
                longitud=longitud,
                gincana_id=gincana_id
            )
            parada.save()

    paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
    map = folium.Map(location=[51.505, -0.09], zoom_start=13)

    for parada in paradas:
        folium.Marker([parada.latitud, parada.longitud], popup=f'Parada {parada.orden}').add_to(map)

    for i in range(len(paradas) - 1):
        parada_actual = paradas[i]
        parada_siguiente = paradas[i + 1]
        folium.PolyLine([(parada_actual.latitud, parada_actual.longitud), (parada_siguiente.latitud, parada_siguiente.longitud)]).add_to(map)

    map.save(f'mapa_gincana_{gincana_id}.html')
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') 
    
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('--headless')

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        try:
            driver = webdriver.Firefox(options=firefox_options)
        except:
            try:
                driver = webdriver.Edge(options=edge_options)
            except:
                driver = None

    user_agent = request.META['HTTP_USER_AGENT']
    if 'Chrome' in user_agent:
        driver = webdriver.Chrome(options=chrome_options)
    elif 'Firefox' in user_agent:
        driver = webdriver.Firefox()
    elif 'Edg' in user_agent:  
        driver = webdriver.Edge()
    else:
        driver = None

    if driver:
        driver.get('file://' + os.path.abspath(f'mapa_gincana_{gincana_id}.html'))
        time.sleep(2)
        driver.save_screenshot(f'mapa_gincana_{gincana_id}.png')
        driver.quit()

    os.remove(f'mapa_gincana_{gincana_id}.html')
    
    nombre_archivo = f"mapa_{gincana.id}.png"
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
    shutil.move(f'mapa_gincana_{gincana_id}.png', ruta_imagen)
    gincana.imagen = nombre_archivo
    gincana.save()

    return render(request, 'editar_gincana.html', {'gincana': gincana})

@login_required
def guardar_cambios_gincana(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    ordered_ids = request.POST.getlist('ordered_ids[]')

    ordered_ids = [int(id) for id in ordered_ids]

    for index, parada_id in enumerate(ordered_ids, start=1):
        Parada.objects.filter(id=parada_id, gincana=gincana).update(orden=index)
    
    return render(request, 'editar_gincana.html', {'gincana': gincana})

@login_required
def borrar_parada(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    parada_id = request.POST.get('parada_id')

    parada = Parada.objects.get(id=parada_id)

    parada.delete()
    
    return render(request, 'editar_gincana.html', {'gincana': gincana})

@login_required
def editar_parada(request, gincana_id, parada_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    parada = get_object_or_404(Parada, pk=parada_id)

    if Pregunta.objects.filter(parada_id=parada_id).exists():
        pregunta = Pregunta.objects.get(parada_id=parada_id)
        preguntaForm = PreguntaForm(instance=pregunta)
        respuestas = Respuesta.objects.filter(pregunta_id=pregunta.id)
        respuestasForms = [RespuestaForm(instance=respuesta) for respuesta in respuestas]
    else:
        preguntaForm = PreguntaForm()
        respuestasForms = [RespuestaForm() for _ in range(10)]

    return render(request, 'pregunta.html', {'gincana': gincana, 'preguntaForm': preguntaForm, 'respuestaForm': respuestasForms, 'parada': parada})

@login_required
def editar_guardar(request, gincana_id, parada_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)

    if request.method == 'POST':
        pregunta_form = PreguntaForm(request.POST)

        if pregunta_form.is_valid():
            pregunta, created = Pregunta.objects.get_or_create(parada_id=parada_id)
            pregunta.enunciado = pregunta_form.cleaned_data['enunciado']
            pregunta.save()

            Respuesta.objects.filter(pregunta=pregunta).delete()

            num_respuestas = int(request.POST.get('num_respuestas', 0))
            for i in range(num_respuestas):
                respuesta_texto = request.POST.get(f'respuesta_{i}_respuesta')
                puntos = request.POST.get(f'respuesta_{i}_puntos')
                es_correcta = request.POST.get(f'respuesta_{i}_es_correcta')

                respuesta = Respuesta(
                    respuesta=respuesta_texto,
                    puntos=int(puntos),
                    es_correcta=bool(es_correcta),
                    pregunta=pregunta
                )
                respuesta.save()


            return redirect('editar_gincana', gincana_id=gincana_id)
    else:
        pregunta_form = PreguntaForm()

    return render(request, 'editar_gincana.html', {'gincana': gincana})