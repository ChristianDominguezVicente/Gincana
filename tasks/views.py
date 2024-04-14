from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils.datastructures import MultiValueDictKeyError
from .forms import GincanaForm, ProfesorForm, GincanaConfiguracionForm, EditarProfesorForm, VerificacionForm, PasswordForm, PasswordCambioForm, AuthenticationForm
from .models import Gincana, Profesor, Verificacion, Parada, Pregunta, Respuesta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import datetime, random, json

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
        return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores})
    else:
        try:
            gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
            return redirect('gincana')
        except ValueError:
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores, 
                'error': "Error actualizando la Gincana"})

@login_required        
def editar_gincana(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    profesores = Profesor.objects.filter(email=request.user.email)
    paradas = Parada.objects.filter(gincana=gincana)
    paradas_gincana = list(paradas.values('latitud', 'longitud'))
    return render(request, 'editar_gincana.html', {'gincana': gincana, 'profesores': profesores, 'paradas': paradas_gincana})

@login_required        
def configuracion_gincana(request, gincana_id):  
    profesores = Profesor.objects.filter(email=request.user.email)
    if request.method == 'GET':
        gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
        form = GincanaConfiguracionForm(instance=gincana)
        return render(request, 'configuracion_gincana.html', {'gincana': gincana,'form': form, 'profesores': profesores})
    else:
        try:
            gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
            form = GincanaConfiguracionForm(request.POST, instance=gincana)
            form.save()
            return render(request, 'gincana.html', {'gincana': gincana, 'profesores': profesores})
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
    return render(request, 'gincana_publica.html', {'gincana': gincana, 'profesores': profesores})

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
    if nueva_Gincana.email_profesor == request.user:
        return render(request, 'gincana_publica.html', {'gincana': nueva_Gincana, 'gincanas': gincanas, 'profesores': profesores,
            'error': "Esta Gincana ya te pernetece."})
    else:
        nueva_Gincana.pk = None
        nueva_Gincana.email_profesor = request.user
        nueva_Gincana.save()
        return render(request, 'mis_gincanas.html', {'gincana': nueva_Gincana, 'gincanas': gincanas, 'profesores': profesores})

@login_required    
def gincana_eliminar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    profesores = Profesor.objects.filter(email=request.user.email)
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
        user = authenticate(request, username=request.POST['username'], 
                    password=request.POST['password'])
        if user is None:
            return render(request, 'verificacion_password.html', {
                'form': AuthenticationForm, 'email_id': email_id, 'error': 'La contraseña no es correcta',
                'profesor': profesor,'profesores': profesores
            })
        else:
            return redirect('editar_profesor', email_id=email_id)
        
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
            user = authenticate(request, username=request.POST['username'], 
                        password=request.POST['password'])
            if user is None:
                return render(request, 'verificacion_password.html', {
                    'form': AuthenticationForm, 'email_id': email_id, 'error': 'La contraseña no es correcta',
                    'profesor': profesor,'profesores': profesores
                })
            else:
                return redirect('profesor_password', email_id=email_id)
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
    paradas = Parada.objects.filter(gincana=gincana)
    paradas_gincana = list(paradas.values('latitud', 'longitud'))
    return render(request, 'parada.html', {'gincana': gincana, 'paradas': paradas_gincana})

@login_required
def parada_guardar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id)

    paradas_data = json.loads(request.POST.get('parada'))
    for latitud, longitud in paradas_data.items():
        if not Parada.objects.filter(latitud=latitud, longitud=longitud, gincana_id=gincana_id).exists():
            parada= Parada.objects.create(
                latitud=latitud,
                longitud=longitud,
                gincana_id=gincana_id
            )
            parada.save()

    return render(request, 'editar_gincana.html', {'gincana': gincana})
