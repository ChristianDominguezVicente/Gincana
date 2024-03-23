from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from .forms import GincanaForm, ProfesorForm, GincanaConfiguracionForm, EditarProfesorForm, VerificacionForm
from .models import Gincana, Profesor, Verificacion
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime, random

from django.core.mail import send_mail

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
                        
                        return redirect('verificacion')
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
                
def verificacion(request):
    if request.method == 'GET':
            return render(request, 'verificacion.html', {
                'form': VerificacionForm
            })
    else:
        form = VerificacionForm(request.POST)
        if Verificacion.objects.filter(code=request.POST['code'],email=request.POST['email']):
            user = get_object_or_404(Profesor, pk=request.POST['email'])
            user.usuario_verificado=True
            user.save()
            code = get_object_or_404(Verificacion, email=user.email)
            code.delete()
            login(request, user)
            return redirect('home')
        else:
            form = VerificacionForm()
            return render(request, 'verificacion.html',{'form': form, 'error': 'No es el código de verificación.'})

def verificacion_reenviar(request):
    if request.method == "POST":
        if request.POST['email'] is None:
            form = VerificacionForm()
            return render(request, 'verificacion.html',{'form': form, 'error': 'Escriba su email en la caja de texto antes de pulsar en reenviar.'})
        else:
            num=random.randint(0,9999)
            user = Verificacion.objects.get(email=request.POST['email'])
            user.code = num
            user.save()
            send_mail(
                subject='Código de Verificación',
                message=str(num),
                from_email='herstorygincanas@gmail.com',
                recipient_list=[request.POST['email']]
            )
            return redirect('verificacion')

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
    return render(request, 'editar_gincana.html', {'gincana': gincana, 'profesores': profesores})

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
                """
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'El usuario no esta verificado.'
                })
                """
                return redirect('verificacion')
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
            return redirect('profesor')
        except ValueError:
            return render(request, 'profesor.html', {'profesor': profesor, 'profesores': profesores, 
                'error': "Error actualizando el Perfil"})

@login_required    
def profesor_eliminar(request, email_id):
    profesor = get_object_or_404(Profesor, pk = email_id, email = request.user.email)
    if request.method == "POST":
        profesor.delete()
        return redirect('signin')

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
            form = EditarProfesorForm(request.POST, instance=profesor)
            d = datetime.datetime.strptime(request.POST['fecha_nacimiento'], '%Y-%m-%d').date()
            edad = date.today().year - d.year -((date.today().month, date.today().day) <(d.month, d.day))
            if edad >= 18:
                form.save()
                return render(request, 'profesor.html', {'profesor': profesor, 'profesores': profesores})
            else:
                return render(request, 'editar_profesor.html', {
                    'profesor': profesor, 'profesores': profesores,
                    'form': EditarProfesorForm,
                    'error': 'Para registrarse necesita tener 18 años mínimo.'
                })
        except MultiValueDictKeyError:
            return render(request, 'editar_profesor.html', {'profesor': profesor, 'form': form,
                'profesores': profesores, 'error': "Error actualizando el Perfil"})