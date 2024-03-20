from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import GincanaForm, ProfesorForm, GincanaConfiguracionForm, EditarProfesorForm
from .models import Gincana, Profesor
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime

# Create your views here.

@login_required
def home(request):
    mis_gincanas = Gincana.objects.filter(email_profesor=request.user)
    gincanas_publicas = Gincana.objects.filter(visibilidad=True).order_by('-edicion')
    return render(request, 'home.html',{'mis_gincanas': mis_gincanas, 'gincanas_publicas': gincanas_publicas})


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
                        login(request, user)
                        return redirect('home')
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

@login_required
def gincanas(request):
    gincanas = Gincana.objects.filter(email_profesor=request.user)
    return render(request, 'mis_gincanas.html',{'gincanas': gincanas})

@login_required
def gincanas_publicas(request):
    gincanas = Gincana.objects.filter(visibilidad=True).order_by('-edicion')
    return render(request, 'gincanas_publicas.html',{'gincanas': gincanas})

@login_required
def crear_gincana(request):

    if request.method == 'GET':
        return render(request, 'crear_gincana.html',{
            'form': GincanaForm
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
                'error': 'Los datos no son válidos'
            })

@login_required
def gincana(request, gincana_id):  
    if request.method == 'GET':
        gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
        return render(request, 'gincana.html', {'gincana': gincana  })
    else:
        try:
            gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
            return redirect('gincana')
        except ValueError:
            return render(request, 'gincana.html', {'gincana': gincana, 
                'error': "Error actualizando la Gincana"})

@login_required        
def editar_gincana(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    return render(request, 'editar_gincana.html', {'gincana': gincana})

@login_required        
def configuracion_gincana(request, gincana_id):  
    if request.method == 'GET':
        gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
        form = GincanaConfiguracionForm(instance=gincana)
        return render(request, 'configuracion_gincana.html', {'gincana': gincana,'form': form})
    else:
        try:
            gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
            form = GincanaConfiguracionForm(request.POST, instance=gincana)
            form.save()
            return render(request, 'gincana.html', {'gincana': gincana})
        except ValueError:
            return render(request, 'configuracion_gincana.html', {'gincana': gincana, 'form': form,
                'error': "Error actualizando la Gincana"})

@login_required        
def puntuacion_gincana(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    return render(request, 'puntuacion_gincana.html', {'gincana': gincana})

@login_required        
def gincana_publica(request, gincana_id):  
    gincana = get_object_or_404(Gincana, pk=gincana_id)
    return render(request, 'gincana_publica.html', {'gincana': gincana})

@login_required
def gincana_iniciar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    if request.method == "POST" and gincana.activa == False and gincana.duracion is not None :
        gincana.activa = True
        gincana.save()
        return render(request, 'gincana.html', {'gincana': gincana})
    elif request.method == "POST" and gincana.activa == True and gincana.duracion is not None :
        gincana.activa = False
        gincana.edicion = timezone.now()
        gincana.save()
        return render(request, 'gincana.html', {'gincana': gincana})
    else:
        return render(request, 'gincana.html', {'gincana': gincana, 
            'error': "Se necesita primero establecer una duración a la gincana."})

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
def profesor(request):
    profesor = get_object_or_404(Profesor, pk = request.user.email)
    return render(request, 'profesor.html', {'profesor': profesor})

@login_required
def editar_profesor(request, email):
    if request.method == 'GET':
        profesor = get_object_or_404(Profesor, pk=email)
        form = EditarProfesorForm(instance=profesor)
        return render(request, 'editar_profesor.html', {'profesor': profesor,'form': form})
    else:
        try:
            profesor = get_object_or_404(Profesor, pk=email)
            form = EditarProfesorForm(request.POST, instance=profesor)
            form.save()
            return render(request, 'profesor.html', {'profesor': profesor})
        except ValueError:
            return render(request, 'editar_profesor.html', {'profesor': profesor, 'form': form,
                'error': "Error actualizando Perfil"})
    

