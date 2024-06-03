from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils.datastructures import MultiValueDictKeyError
from .forms import GincanaForm, ProfesorForm, GincanaConfiguracionForm, EditarProfesorForm, VerificacionForm, PasswordForm, PasswordCambioForm, AuthenticationForm, PreguntaForm, RespuestaForm, ContactForm, InvitadosForm, AuthenticationInvitadosForm
from .models import Gincana, Profesor, Verificacion, Parada, Pregunta, Respuesta, Invitado, Puntuacion, GincanaJugada
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import datetime, random, json, folium, os, shutil, uuid, pdfkit, base64
from datetime import date, datetime, timezone, time
import time as t
from selenium import webdriver
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from collections import defaultdict

# Create your views here.

@login_required
def update_dark_mode(request):
    if request.method == 'POST':
        dark_mode_enabled = request.POST.get('darkModeEnabled', False)
        request.session['darkModeEnabled'] = dark_mode_enabled
        response = JsonResponse({'success': True})

        response.set_cookie('darkModeEnabled', dark_mode_enabled)

        return response
    else:
        return JsonResponse({'success': False}, status=405) 

@login_required
def home(request):
    mis_gincanas = Gincana.objects.filter(email_profesor=request.user)
    gincanas_publicas = Gincana.objects.filter(visibilidad=True).order_by('-edicion')
    profesores = Profesor.objects.filter(email=request.user.email)

    dark_mode_cookie = request.COOKIES.get('darkModeEnabled')
    dark_mode_enabled = dark_mode_cookie if dark_mode_cookie is not None else 'false'

    return render(request, 'home.html', {'mis_gincanas': mis_gincanas, 'gincanas_publicas': gincanas_publicas, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled})

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
                    d = datetime.strptime(request.POST['fecha_nacimiento'], '%Y-%m-%d').date()
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
    if request.user.is_authenticated:
        return redirect('home')
    else:
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
    if request.user.is_authenticated:
        return redirect('home')
    else:
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
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

    return render(request, 'mis_gincanas.html',{'gincanas': gincanas, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled})

@login_required
def gincanas_publicas(request):
    gincanas = Gincana.objects.filter(visibilidad=True).order_by('-edicion')
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

    return render(request, 'gincanas_publicas.html',{'gincanas': gincanas, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled})

@login_required
def crear_gincana(request):
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if request.method == 'GET':
        return render(request, 'crear_gincana.html',{
            'form': GincanaForm, 
            'profesores': profesores,
            'darkModeEnabled': dark_mode_enabled
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
                'profesores': profesores,
                'darkModeEnabled': dark_mode_enabled
            })

@login_required
def gincana(request, gincana_id):  
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
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
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'darkModeEnabled': dark_mode_enabled})
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
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'darkModeEnabled': dark_mode_enabled})
        except ValueError:
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 
                'darkModeEnabled': dark_mode_enabled, 'error': "Error actualizando la Gincana"})

@login_required        
def editar_gincana(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    paradas = Parada.objects.filter(gincana=gincana)
    contador = paradas.count()
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

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

    return render(request, 'editar_gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'db': paradas, 'darkModeEnabled': dark_mode_enabled})

@login_required        
def configuracion_gincana(request, gincana_id):  
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
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
        return render(request, 'configuracion_gincana.html', {'gincana': gincana,'form': form, 'profesores': profesores, 'paradas': paradas_data, 'darkModeEnabled': dark_mode_enabled})
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
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'darkModeEnabled': dark_mode_enabled})
        except ValueError:
            return render(request, 'configuracion_gincana.html', {'gincana': gincana, 'form': form,
                'darkModeEnabled': dark_mode_enabled, 'profesores': profesores, 'error': "Error actualizando la Gincana"})

@login_required        
def puntuacion_gincana(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

    ediciones_distintas = GincanaJugada.objects.filter(gincana_id=gincana.id).values_list('edicion', flat=True).distinct()
    ediciones = list(ediciones_distintas)
    return render(request, 'puntuacion_gincana.html', {'gincana': gincana, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled, 'ediciones': ediciones})

@login_required        
def puntuacion_total(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

    gincanaJugadas = GincanaJugada.objects.filter(gincana=gincana)
    invitados_puntuaciones = []
    for gincanaJugada in gincanaJugadas:
        invitado = gincanaJugada.invitado
        puntos = Puntuacion.objects.filter(invitado_id=invitado.usuario)
        puntuacion = 0
        for punto in puntos:
            puntuacion+=punto.puntuacion
        invitados_puntuaciones.append((invitado, puntuacion))
    return render(request, 'puntuacion_total.html', {'gincana': gincana, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled, 
        'invitados_puntuaciones': invitados_puntuaciones})

@login_required        
def puntuacion_informe(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)

    gincanaJugadas = GincanaJugada.objects.filter(gincana=gincana)
    invitados_puntuaciones = []
    for gincanaJugada in gincanaJugadas:
        invitado = gincanaJugada.invitado
        puntos = Puntuacion.objects.filter(invitado_id=invitado.usuario)
        puntuacion = 0
        for punto in puntos:
            puntuacion+=punto.puntuacion
        invitados_puntuaciones.append((invitado, puntuacion))

    html_string = render_to_string('informe_total.html', {'invitados_puntuaciones': invitados_puntuaciones})

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None
    }

    pdf = pdfkit.from_string(html_string, False, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="puntuacion_total.pdf"'

    return response

@login_required        
def puntuacion_edicion(request, gincana_id, edicion):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

    gincanaJugadas = GincanaJugada.objects.filter(gincana=gincana, edicion=edicion)
    invitados_puntuaciones = []
    for gincanaJugada in gincanaJugadas:
        invitado = gincanaJugada.invitado
        puntos = Puntuacion.objects.filter(invitado_id=invitado.usuario)
        puntuacion = 0
        for punto in puntos:
            puntuacion+=punto.puntuacion
        invitados_puntuaciones.append((invitado, puntuacion))
    return render(request, 'puntuacion_edicion.html', {'gincana': gincana, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled, 
        'invitados_puntuaciones': invitados_puntuaciones, 'edicion': edicion})  

@login_required        
def puntuacion_edicion_informe(request, gincana_id, edicion):
    gincana = get_object_or_404(Gincana, pk=gincana_id)

    gincanaJugadas = GincanaJugada.objects.filter(gincana=gincana, edicion=edicion)
    invitados_puntuaciones = []
    for gincanaJugada in gincanaJugadas:
        invitado = gincanaJugada.invitado
        puntos = Puntuacion.objects.filter(invitado_id=invitado.usuario)
        puntuacion = 0
        for punto in puntos:
            puntuacion+=punto.puntuacion
        invitados_puntuaciones.append((invitado, puntuacion))

    html_string = render_to_string('informe_edicion.html', {'invitados_puntuaciones': invitados_puntuaciones, 'edicion': edicion})

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None
    }

    pdf = pdfkit.from_string(html_string, False, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="puntuacion_edicion.pdf"'

    return response

@login_required        
def gincana_publica(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
    paradas_data = []
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
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
    return render(request, 'gincana_publica.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'darkModeEnabled': dark_mode_enabled})

@login_required
def gincana_iniciar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    profesores = Profesor.objects.filter(email=request.user.email)
    paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
    paradas_data = []
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
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

    paradas_gincana = Parada.objects.filter(gincana=gincana)
    ids_paradas = paradas_gincana.values_list('id', flat=True)
    todas_con_pregunta = all(Pregunta.objects.filter(parada_id=parada_id).exists() for parada_id in ids_paradas)
    
    if request.method == "POST" and gincana.activa == False and gincana.duracion is not None and todas_con_pregunta:
        gincana.activa = True
        gincana.edicion = datetime.now(timezone.utc)
        gincana.save()
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data})
    elif request.method == "POST" and gincana.activa == True and gincana.duracion is not None and todas_con_pregunta:
        gincana.activa = False
        gincana.save()

        invitados = Invitado.objects.filter(gincana_id=gincana.id)
        for invitado in invitados:
            if GincanaJugada.objects.filter(gincana=gincana, invitado=invitado).exists():
                continue 

            puntos = Puntuacion.objects.filter(invitado_id=invitado.usuario)
            puntuacion = 0
            for punto in puntos:
                puntuacion+=punto.puntuacion

            duracion = datetime.now(timezone.utc) - gincana.edicion

            total = int(duracion.total_seconds())
            horas, resto = divmod(total, 3600)
            minutos, segundos = divmod(resto, 60)

            duracion = time(horas, minutos, segundos)

            gincanaJugada = GincanaJugada.objects.create(
                duracion=duracion,
                total_puntos=puntuacion,
                edicion=gincana.edicion,
                gincana_id=gincana.id,
                invitado_id=invitado.usuario
            )
            gincanaJugada.save()
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'darkModeEnabled': dark_mode_enabled})
    else:
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'darkModeEnabled': dark_mode_enabled, 
            'error': "Se necesita primero configurar la hora de finalización de la Gincana y añadir a todas las Paradas sus Preguntas y Respuestas."})

@login_required
def gincana_copiar(request, gincana_id):
    gincanas = Gincana.objects.filter(email_profesor=request.user)
    profesores = Profesor.objects.filter(email=request.user.email)
    nueva_Gincana = Gincana.objects.get(pk=gincana_id)
    paradas = Parada.objects.filter(gincana=gincana_id).order_by('orden')
    paradas_gincana = list(paradas.values('latitud', 'longitud'))
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if nueva_Gincana.email_profesor == request.user:
        return render(request, 'gincana_publica.html', {'gincana': nueva_Gincana, 'gincanas': gincanas, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled,
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
        return render(request, 'mis_gincanas.html', {'gincana': nueva_Gincana, 'gincanas': gincanas, 'profesores': profesores, 'paradas': paradas_gincana, 'darkModeEnabled': dark_mode_enabled})

@login_required    
def gincana_eliminar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    if request.method == "POST":
        if gincana.imagen and os.path.isfile(gincana.imagen.path) and gincana.imagen != 'mapa.png':
            os.remove(gincana.imagen.path)
            os.remove(gincana.imagen_oscura.path)
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
    dark_mode_cookie = request.COOKIES.get('darkModeEnabled')
    dark_mode_enabled = dark_mode_cookie if dark_mode_cookie is not None else False
    if request.method == 'GET':
        profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
        return render(request, 'profesor.html', {'profesor': profesor, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled})
    else:
        try:
            profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
            return redirect('verificacion_password', email_id=request.user.email)
        except ValueError:
            return render(request, 'profesor.html', {'profesor': profesor, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled, 
                'error': "Error actualizando el Perfil"})

@login_required     
def verificacion_password(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if request.method == 'GET':
        return render(request, 'verificacion_password.html', {
            'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores,
            'darkModeEnabled': dark_mode_enabled
        })
    else:
        profesor = get_object_or_404(Profesor, pk=email_id)
        if profesor.email == request.POST['username']:
            user = authenticate(request, username=request.POST['username'], 
                        password=request.POST['password'])
            if user is None:
                return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'La contraseña no es correcta',
                    'profesor': profesor,'profesores': profesores, 
                    'darkModeEnabled': dark_mode_enabled
                })
            else:
                return redirect('editar_profesor', email_id=email_id)
        else:
            return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'Introduzca su Correo Electrónico',
                    'profesor': profesor,'profesores': profesores, 'darkModeEnabled': dark_mode_enabled
                })
        
@login_required     
def verificacion_password2(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if request.method == 'GET':
        return render(request, 'verificacion_password.html', {
            'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores, 
            'darkModeEnabled': dark_mode_enabled
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
                        'profesor': profesor,'profesores': profesores, 'darkModeEnabled': dark_mode_enabled
                    })
                else:
                    return redirect('profesor_password', email_id=email_id)
            else:
                return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'Introduzca su Correo Electrónico',
                    'profesor': profesor,'profesores': profesores, 'darkModeEnabled': dark_mode_enabled
                })
        except MultiValueDictKeyError:
            return render(request, 'verificacion_password.html', {
                'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores, 
            'darkModeEnabled': dark_mode_enabled
            })

@login_required     
def profesor_eliminar(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if request.method == 'GET':
        return render(request, 'verificacion_password.html', {
            'form': AuthenticationForm, 'email_id': email_id, 
            'profesor': profesor, 'profesores': profesores, 
            'darkModeEnabled': dark_mode_enabled
        })
    else:
        try:
            profesor = get_object_or_404(Profesor, pk=email_id)
            user = authenticate(request, username=request.POST['username'], 
                        password=request.POST['password'])
            if user is None:
                return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'La contraseña no es correcta',
                    'profesor': profesor,'profesores': profesores, 'darkModeEnabled': dark_mode_enabled
                })
            else:
                profesor.delete()
                return redirect('signin')
        except MultiValueDictKeyError:
            return render(request, 'verificacion_password.html', {
                'form': AuthenticationForm, 'email_id': email_id, 
                'profesor': profesor, 'profesores': profesores, 
                'darkModeEnabled': dark_mode_enabled
            })

@login_required 
def editar_profesor(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if request.method == 'GET':
        profesor = get_object_or_404(Profesor, pk = email_id, email = request.user.email)
        form = EditarProfesorForm(instance=profesor)
        return render(request, 'editar_profesor.html', {'profesor': profesor, 'form': form, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled})
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
                    'error': 'Para registrarse necesita tener 18 años mínimo.', 
                    'darkModeEnabled': dark_mode_enabled
                })
        except MultiValueDictKeyError:
            return render(request, 'editar_profesor.html', {'profesor': profesor, 'form': form,
                'profesores': profesores, 'error': "Error actualizando el Perfil", 'darkModeEnabled': dark_mode_enabled})
    
@login_required
def profesor_password(request, email_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if request.method == 'GET':
        return render(request, 'profesor_password.html', {
            'form': PasswordCambioForm,
            'profesor': profesor, 'profesores': profesores, 
            'darkModeEnabled': dark_mode_enabled
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
                        'profesor': profesor, 'profesores': profesores, 
                        'darkModeEnabled': dark_mode_enabled
                    })
            else:
                return render(request, 'profesor_password.html', {
                    'form': PasswordCambioForm,
                    'error': 'Las contraseñas no coinciden',
                    'profesor': profesor, 'profesores': profesores, 
                    'darkModeEnabled': dark_mode_enabled
                })
        except MultiValueDictKeyError:
            return render(request, 'profesor_password.html', {
                'form': PasswordCambioForm,
                'profesor': profesor, 'profesores': profesores, 
                'darkModeEnabled': dark_mode_enabled
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
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

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
    map.save(f'mapa_gincana_{gincana_id}_oscuro.html')

    mapa_oscuro_file = f'mapa_gincana_{gincana_id}_oscuro.html'
    with open(mapa_oscuro_file, 'r') as file:
        mapa_oscuro_content = file.read()

    pos_head_cierre = mapa_oscuro_content.find('</head>')

    estilo_css = '<style>body { filter: invert(1) hue-rotate(180deg); }</style>'
    mapa_oscuro_content = mapa_oscuro_content[:pos_head_cierre] + estilo_css + mapa_oscuro_content[pos_head_cierre:]

    with open(mapa_oscuro_file, 'w') as file:
        file.write(mapa_oscuro_content)
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') 
    
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('--headless')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver2 = webdriver.Chrome(options=chrome_options)
    except:
        try:
            driver = webdriver.Firefox(options=firefox_options)
            driver2 = webdriver.Firefox(options=firefox_options)
        except:
            try:
                driver = webdriver.Edge(options=edge_options)
                driver2 = webdriver.Edge(options=edge_options)
            except:
                driver = None
                driver2 = None

    user_agent = request.META['HTTP_USER_AGENT']
    if 'Chrome' in user_agent:
        driver = webdriver.Chrome(options=chrome_options)
        driver2 = webdriver.Chrome(options=chrome_options)
    elif 'Firefox' in user_agent:
        driver = webdriver.Firefox()
        driver2 = webdriver.Firefox()
    elif 'Edg' in user_agent:  
        driver = webdriver.Edge()
        driver2 = webdriver.Edge()
    else:
        driver = None
        driver2 = None

    if driver and driver2:
        driver.get('file://' + os.path.abspath(f'mapa_gincana_{gincana_id}.html'))
        driver2.get('file://' + os.path.abspath(f'mapa_gincana_{gincana_id}_oscuro.html'))
        t.sleep(2)
        driver.save_screenshot(f'mapa_gincana_{gincana_id}.png')
        driver2.save_screenshot(f'mapa_gincana_{gincana_id}_oscuro.png')
        driver.quit()
        driver2.quit()

    os.remove(f'mapa_gincana_{gincana_id}.html')
    os.remove(f'mapa_gincana_{gincana_id}_oscuro.html')
    
    nombre_archivo = f"mapa_{gincana.id}.png"
    nombre_archivo2 = f"mapa_{gincana.id}_oscuro.png"
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
    ruta_imagen2 = os.path.join(settings.MEDIA_ROOT, nombre_archivo2)
    shutil.move(f'mapa_gincana_{gincana_id}.png', ruta_imagen)
    shutil.move(f'mapa_gincana_{gincana_id}_oscuro.png', ruta_imagen2)
    gincana.imagen = nombre_archivo
    gincana.imagen_oscura = nombre_archivo2
    gincana.save()

    return render(request, 'editar_gincana.html', {'gincana': gincana, 'darkModeEnabled': dark_mode_enabled})

@login_required
def guardar_cambios_gincana(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    ordered_ids = request.POST.getlist('ordered_ids[]')

    ordered_ids = [int(id) for id in ordered_ids]

    for index, parada_id in enumerate(ordered_ids, start=1):
        Parada.objects.filter(id=parada_id, gincana=gincana).update(orden=index)
    
    paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
    map = folium.Map(location=[51.505, -0.09], zoom_start=13)

    for parada in paradas:
        folium.Marker([parada.latitud, parada.longitud], popup=f'Parada {parada.orden}').add_to(map)

    for i in range(len(paradas) - 1):
        parada_actual = paradas[i]
        parada_siguiente = paradas[i + 1]
        folium.PolyLine([(parada_actual.latitud, parada_actual.longitud), (parada_siguiente.latitud, parada_siguiente.longitud)]).add_to(map)

    map.save(f'mapa_gincana_{gincana_id}.html')
    map.save(f'mapa_gincana_{gincana_id}_oscuro.html')

    mapa_oscuro_file = f'mapa_gincana_{gincana_id}_oscuro.html'
    with open(mapa_oscuro_file, 'r') as file:
        mapa_oscuro_content = file.read()

    pos_head_cierre = mapa_oscuro_content.find('</head>')

    estilo_css = '<style>body { filter: invert(1) hue-rotate(180deg); }</style>'
    mapa_oscuro_content = mapa_oscuro_content[:pos_head_cierre] + estilo_css + mapa_oscuro_content[pos_head_cierre:]

    with open(mapa_oscuro_file, 'w') as file:
        file.write(mapa_oscuro_content)
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') 
    
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('--headless')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver2 = webdriver.Chrome(options=chrome_options)
    except:
        try:
            driver = webdriver.Firefox(options=firefox_options)
            driver2 = webdriver.Firefox(options=firefox_options)
        except:
            try:
                driver = webdriver.Edge(options=edge_options)
                driver2 = webdriver.Edge(options=edge_options)
            except:
                driver = None
                driver2 = None

    user_agent = request.META['HTTP_USER_AGENT']
    if 'Chrome' in user_agent:
        driver = webdriver.Chrome(options=chrome_options)
        driver2 = webdriver.Chrome(options=chrome_options)
    elif 'Firefox' in user_agent:
        driver = webdriver.Firefox()
        driver2 = webdriver.Firefox()
    elif 'Edg' in user_agent:  
        driver = webdriver.Edge()
        driver2 = webdriver.Edge()
    else:
        driver = None
        driver2 = None

    if driver and driver2:
        driver.get('file://' + os.path.abspath(f'mapa_gincana_{gincana_id}.html'))
        driver2.get('file://' + os.path.abspath(f'mapa_gincana_{gincana_id}_oscuro.html'))
        t.sleep(2)
        driver.save_screenshot(f'mapa_gincana_{gincana_id}.png')
        driver2.save_screenshot(f'mapa_gincana_{gincana_id}_oscuro.png')
        driver.quit()
        driver2.quit()

    os.remove(f'mapa_gincana_{gincana_id}.html')
    os.remove(f'mapa_gincana_{gincana_id}_oscuro.html')
    
    nombre_archivo = f"mapa_{gincana.id}.png"
    nombre_archivo2 = f"mapa_{gincana.id}_oscuro.png"
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
    ruta_imagen2 = os.path.join(settings.MEDIA_ROOT, nombre_archivo2)
    shutil.move(f'mapa_gincana_{gincana_id}.png', ruta_imagen)
    shutil.move(f'mapa_gincana_{gincana_id}_oscuro.png', ruta_imagen2)
    gincana.imagen = nombre_archivo
    gincana.imagen_oscura = nombre_archivo2
    gincana.save()

    return render(request, 'editar_gincana.html', {'gincana': gincana, 'darkModeEnabled': dark_mode_enabled})

@login_required
def borrar_parada(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    parada_id = request.POST.get('parada_id')

    parada = Parada.objects.get(id=parada_id)

    parada.delete()

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
        t.sleep(2)
        driver.save_screenshot(f'mapa_gincana_{gincana_id}.png')
        driver.quit()

    os.remove(f'mapa_gincana_{gincana_id}.html')
    
    nombre_archivo = f"mapa_{gincana.id}.png"
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
    shutil.move(f'mapa_gincana_{gincana_id}.png', ruta_imagen)
    gincana.imagen = nombre_archivo
    gincana.save()
    
    return render(request, 'editar_gincana.html', {'gincana': gincana, 'darkModeEnabled': dark_mode_enabled})

@login_required
def editar_parada(request, gincana_id, parada_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    parada = get_object_or_404(Parada, pk=parada_id)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)

    if Pregunta.objects.filter(parada_id=parada_id).exists():
        pregunta = Pregunta.objects.get(parada_id=parada_id)
        preguntaForm = PreguntaForm(instance=pregunta)
        respuestas = Respuesta.objects.filter(pregunta_id=pregunta.id)
        respuestasForms = [RespuestaForm(instance=respuesta) for respuesta in respuestas]
    else:
        preguntaForm = PreguntaForm()
        respuestasForms = [RespuestaForm() for _ in range(10)]

    return render(request, 'pregunta.html', {'gincana': gincana, 'preguntaForm': preguntaForm, 'respuestaForm': respuestasForms, 'parada': parada, 'darkModeEnabled': dark_mode_enabled})

@login_required
def editar_guardar(request, gincana_id, parada_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
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

    if request.method == 'POST':
        pregunta_form = PreguntaForm(request.POST)

        if pregunta_form.is_valid():
            pregunta, created = Pregunta.objects.get_or_create(parada_id=parada_id)
            pregunta.enunciado = pregunta_form.cleaned_data['enunciado']
            pregunta.save()

            Respuesta.objects.filter(pregunta=pregunta).delete()

            num_respuestas = int(request.POST.get('num_respuestas', 0))

            cont_true=0
            lista_false = []
            for i in range(num_respuestas):
                if request.POST.get(f'respuesta_{i}_es_correcta') != None:
                    cont_true+=1
                    true = request.POST.get(f'respuesta_{i}_puntos')
                else:
                    lista_false.append(request.POST.get(f'respuesta_{i}_puntos'))
            if cont_true != 1:
                return render(request, 'editar_gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'db': paradas, 'darkModeEnabled': dark_mode_enabled,
                    'error': 'Tiene que haber solo una respuesta correcta.'})
            for i in range(len(lista_false)):
                if lista_false[i] > true:
                    return render(request, 'editar_gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'db': paradas, 'darkModeEnabled': dark_mode_enabled,
                        'error': 'La respuesta correcta tiene que tener mayor puntuación.'})

            for i in range(num_respuestas):
                respuesta_texto = request.POST.get(f'respuesta_{i}_respuesta')
                if request.POST.get(f'respuesta_{i}_puntos').isnumeric():
                    puntos = request.POST.get(f'respuesta_{i}_puntos')
                else:
                    return render(request, 'editar_gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_data, 'db': paradas, 'darkModeEnabled': dark_mode_enabled,
                        'error': 'La puntuación solo pueden ser numeros enteros.'})
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

    return render(request, 'editar_gincana.html', {'gincana': gincana, 'darkModeEnabled': dark_mode_enabled})

@login_required
def buscar_gincanas(request):
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    if request.method == 'GET':
        query = request.GET.get('q')
        mis_gincanas = Gincana.objects.filter(titulo__icontains=query, email_profesor=request.user)
        gincanas_publicas = Gincana.objects.filter(titulo__icontains=query).exclude(email_profesor=request.user)
        return render(request, 'resultados_busqueda.html', {'mis_gincanas': mis_gincanas, 'gincanas_publicas': gincanas_publicas, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled})
    else:
        return render(request, 'resultados_busqueda.html', {'profesores': profesores, 'darkModeEnabled': dark_mode_enabled})

@login_required
def centro_de_ayuda(request):
    profesores = Profesor.objects.filter(email=request.user.email)

    dark_mode_cookie = request.COOKIES.get('darkModeEnabled')
    dark_mode_enabled = dark_mode_cookie if dark_mode_cookie is not None else False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            asunto = form.cleaned_data['asunto'] + " - " + request.user.email
            descripcion = form.cleaned_data['descripcion']
            send_mail(
                asunto,
                descripcion,
                from_email='herstorygincanas@gmail.com',
                recipient_list=['herstorygincanas@gmail.com']
            )
            return render(request, 'centro_de_ayuda.html', {'profesores': profesores, 'form': form, 'darkModeEnabled': dark_mode_enabled, 'confirmacion': 'Se ha enviado el mensaje.'})    
    else:
        form = ContactForm()

    return render(request, 'centro_de_ayuda.html', {'profesores': profesores, 'form': form, 'darkModeEnabled': dark_mode_enabled})

@login_required
def usuarios_invitados(request, gincana_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    form = InvitadosForm()
    total = Invitado.objects.filter(gincana=gincana).count()
    invitados = Invitado.objects.filter(gincana=gincana)
    invitados_ordenados = defaultdict(list)
    
    for invitado in invitados:
        jugadas = GincanaJugada.objects.filter(gincana=gincana, invitado=invitado)
        if jugadas.exists():
            for jugada in jugadas:
                invitados_ordenados[jugada.edicion].append(invitado)
        else:
            invitados_ordenados["Nuevos"].append(invitado)

    return render(request, 'usuarios_invitados.html', {'gincana': gincana, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled, 
        'invitados_ordenados': dict(invitados_ordenados), 'form': form, 'total': total})

@login_required
def documento_qrs(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    invitados = Invitado.objects.filter(gincana=gincana)
    invitados_nuevos = []
    for invitado in invitados:
        jugadas = GincanaJugada.objects.filter(gincana=gincana, invitado=invitado)
        if not jugadas.exists():
            invitados_nuevos.append(invitado)

    for invitado in invitados_nuevos:
        if invitado.qr_code and hasattr(invitado.qr_code, 'file'):
            qr_code_image = invitado.qr_code.file.read()
            qr_code_base64 = base64.b64encode(qr_code_image).decode('utf-8')
            invitado.qr_code_base64 = qr_code_base64

    html_string = render_to_string('documento_qrs.html', {'invitados': invitados_nuevos})

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None
    }

    pdf = pdfkit.from_string(html_string, False, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="documento_qrs.pdf"'

    return response

@login_required
def crear_usuarios_invitados(request, gincana_id):
    profesores = Profesor.objects.filter(email=request.user.email)
    dark_mode_enabled = request.session.get('darkModeEnabled', False)
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    invitados = Invitado.objects.filter(gincana=gincana)
    count = Invitado.objects.filter(gincana=gincana).count()

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

    paradas_gincana = Parada.objects.filter(gincana=gincana)
    ids_paradas = paradas_gincana.values_list('id', flat=True)
    todas_con_pregunta = all(Pregunta.objects.filter(parada_id=parada_id).exists() for parada_id in ids_paradas)

    if request.method == "POST" and gincana.duracion is not None and todas_con_pregunta:
        form = InvitadosForm(request.POST)
        if form.is_valid():
            numero_invitados = int(form.cleaned_data['usuarios'])
            for i in range(numero_invitados):
                unique_id = uuid.uuid4().hex
                usuario = f'invitado_{gincana_id}_{count + i + 1}_{unique_id}'
                invitado = Invitado(usuario=usuario, gincana=gincana)
                invitado.save()
            return redirect('usuarios_invitados', gincana_id = gincana_id)
    else:
        form = InvitadosForm()

    return render(request, 'usuarios_invitados.html', {'gincana': gincana, 'profesores': profesores, 'darkModeEnabled': dark_mode_enabled, 'invitados': invitados, 'form': form, 'num': count,
        'error': "Se necesita primero configurar la hora de finalización de la Gincana y añadir a todas las Paradas sus Preguntas y Respuestas."})

@login_required
def borrar_usuarios_invitados(request, gincana_id, usuario):
    invitado = get_object_or_404(Invitado, usuario=usuario, gincana_id=gincana_id)
    invitado.delete()
    return redirect('usuarios_invitados', gincana_id = gincana_id)

def selector(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'selector.html')

def signin_invitado(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'GET':
                return render(request, 'signin_invitado.html',{
                    'form': AuthenticationInvitadosForm
                })
        else:
            if Invitado.objects.filter(usuario=request.POST['usuario']).exists():
                invitado = get_object_or_404(Invitado,pk=request.POST['usuario'])
                return redirect('invitado_gincana', gincana_id = invitado.gincana_id, invitado=invitado.usuario)
            else:
                return render(request, 'signin_invitado.html',{
                    'form': AuthenticationInvitadosForm,
                    'error': 'El usuario invitado introducido no existe.'
                })

def invitado_gincana(request, gincana_id, invitado):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        gincana = get_object_or_404(Gincana, pk=gincana_id)
        invitado_gincana = get_object_or_404(Invitado, pk=invitado)
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
        return render(request, 'invitado_gincana.html', {'gincana': gincana, 'invitado': invitado_gincana, 'paradas': paradas_data})
    
def invitado_gincana_iniciar(request, gincana_id, invitado):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        gincana = get_object_or_404(Gincana, pk=gincana_id)
        invitado_gincana = get_object_or_404(Invitado, pk=invitado)
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
        if request.method == "POST" and gincana.activa == True:
            return redirect ('invitado_responder', gincana_id = gincana_id, invitado = invitado, parada = (invitado_gincana.respondidas+1))
        else:
            return render(request, 'invitado_gincana.html', {'gincana': gincana, 'invitado': invitado_gincana, 'paradas': paradas_data, 'parada': (invitado_gincana.respondidas+1), 
                'error': "La Gincana todavía no ha empezado."})
    
def invitado_responder(request, gincana_id, invitado, parada):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        gincana = get_object_or_404(Gincana, pk=gincana_id)
        invitado_gincana = get_object_or_404(Invitado, pk=invitado)
        paradas = Parada.objects.filter(gincana=gincana).order_by('orden')
        paradas_data = []
        for par in paradas:
            if par.orden == parada:
                preg = get_object_or_404(Pregunta, parada_id=par.id)
                res = list(preg.respuesta_set.all()) if preg else []
            pregunta = par.pregunta_set.first()
            respuestas = list(pregunta.respuesta_set.all()) if pregunta else []
            parada_data = {
                'latitud': par.latitud,
                'longitud': par.longitud,
                'pregunta': pregunta.enunciado if pregunta else None,
                'respuestas': [{'respuesta': respuesta.respuesta, 'puntos': respuesta.puntos, 'es_correcta': respuesta.es_correcta} for respuesta in respuestas]
            }
            paradas_data.append(parada_data)
        if Parada.objects.filter(gincana=gincana).order_by('orden').last().orden < parada:
            return redirect('invitado_fin', gincana_id=gincana_id, invitado=invitado)
        else:
            return render(request, 'invitado_gincana_responder.html', {'gincana': gincana, 'invitado': invitado_gincana, 'paradas': paradas_data, 
                'parada': parada, 'pregunta': preg.enunciado, 'respuestas': res})

def invitado_registrar(request, gincana_id, invitado, parada, respuesta_id):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        invitado_gincana = get_object_or_404(Invitado, pk=invitado)
        res = get_object_or_404(Respuesta, pk=respuesta_id)
        preg = get_object_or_404(Pregunta, pk=res.pregunta.id)
        par = get_object_or_404(Parada, pk=preg.parada.id)

        if par.orden == invitado_gincana.respondidas:
            gincana = get_object_or_404(Gincana, pk=gincana_id)
            if Parada.objects.filter(gincana=gincana).order_by('orden').last().orden < parada:
                return redirect('invitado_fin', gincana_id=gincana_id, invitado=invitado)
            else:
                parada+=1
                return redirect('invitado_responder', gincana_id=gincana_id, invitado=invitado, parada=parada)

        parada+=1
        gincana = get_object_or_404(Gincana, pk=gincana_id)
        
        invitado_gincana.respondidas+=1
        invitado_gincana.update()

        respondida = Puntuacion.objects.create(
            puntuacion=res.puntos,
            invitado=get_object_or_404(Invitado, pk=invitado),
            respuesta_id=res.id,
        )
        respondida.save()

        if Parada.objects.filter(gincana=gincana).order_by('orden').last().orden < parada:
            puntos = Puntuacion.objects.filter(invitado_id=invitado_gincana.usuario)
            puntuacion = 0
            for punto in puntos:
                puntuacion+=punto.puntuacion

            duracion = datetime.now(timezone.utc) - gincana.edicion

            total = int(duracion.total_seconds())
            horas, resto = divmod(total, 3600)
            minutos, segundos = divmod(resto, 60)

            duracion = time(horas, minutos, segundos)

            gincanaJugada = GincanaJugada.objects.create(
                duracion=duracion,
                total_puntos=puntuacion,
                edicion=gincana.edicion,
                gincana_id=gincana.id,
                invitado_id=invitado_gincana.usuario
            )
            gincanaJugada.save()
            return redirect('invitado_fin', gincana_id=gincana_id, invitado=invitado)
        else:
            return redirect('invitado_responder', gincana_id=gincana_id, invitado=invitado, parada=parada)
        
def invitado_fin(request, gincana_id, invitado):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        gincana = get_object_or_404(Gincana, pk=gincana_id)
        invitado_gincana = get_object_or_404(Invitado, pk=invitado)
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

        puntos = Puntuacion.objects.filter(invitado_id=invitado_gincana.usuario)
        puntuacion = 0
        for punto in puntos:
            puntuacion+=punto.puntuacion
        return render(request, 'invitado_fin.html', {'gincana': gincana, 'invitado': invitado_gincana, 'paradas': paradas_data, 'puntuacion': puntuacion})

@login_required
def gincana_confirmacion_eliminar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    return render(request, 'confirmacion_eliminar.html', {'gincana': gincana}) 

@login_required
def gincana_confirmacion_iniciar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    return render(request, 'confirmacion_iniciar.html', {'gincana': gincana}) 

@login_required
def gincana_confirmacion_terminar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    return render(request, 'confirmacion_terminar.html', {'gincana': gincana}) 

@login_required
def profesor_confirmacion_cuenta(request, email_id):
    profesor = get_object_or_404(Profesor, pk=email_id, email=request.user.email)
    return render(request, 'confirmacion_cuenta.html', {'email_id': email_id, 'profesor': profesor}) 
