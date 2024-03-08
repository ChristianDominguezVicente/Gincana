from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import GincanaForm, ProfesorForm
from .models import Gincana, Profesor
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': ProfesorForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registro de usuario
                user = Profesor.objects.create_user(username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    nombre=request.POST['nombre'])
                user.save()
                login(request, user)
                return redirect('gincanas')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': ProfesorForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': ProfesorForm,
            'error': 'Las contraseñas no coinciden'
        })

@login_required
def gincanas(request):
    gincanas = Gincana.objects.filter(email_profesor=request.user, edicion__isnull=True)
    return render(request, 'gincanas.html',{'gincanas': gincanas})

@login_required
def gincanas_completadas(request):
    gincanas = Gincana.objects.filter(email_profesor=request.user, edicion__isnull=False).order_by('-edicion')
    return render(request, 'gincanas.html',{'gincanas': gincanas})

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
            return redirect('gincanas')
        except ValueError:
            return render(request, 'crear_gincana.html',{
                'form': GincanaForm,
                'error': 'Los datos no son válidos'
            })

@login_required
def gincana(request, gincana_id):  
    if request.method == 'GET':
        gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
        form = GincanaForm(instance=gincana)
        return render(request, 'gincana.html', {'gincana': gincana, 'form': form})
    else:
        try:
            gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
            form = GincanaForm(request.POST, instance=gincana)
            form.save()
            return redirect('gincanas')
        except ValueError:
            return render(request, 'gincana.html', {'gincana': gincana, 'form': form,
                'error': "Error actualizando la Gincana"})

@login_required
def gincana_completada(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    if request.method == "POST":
        gincana.edicion = timezone.now()
        gincana.save()
        return redirect('gincanas')

@login_required    
def gincana_eliminar(request, gincana_id):
    gincana = get_object_or_404(Gincana, pk=gincana_id, email_profesor=request.user)
    if request.method == "POST":
        gincana.delete()
        return redirect('gincanas')

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
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
    return render(request, 'informacion.html')
