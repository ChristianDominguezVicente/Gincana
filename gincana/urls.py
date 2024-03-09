"""
URL configuration for gincana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('mis_gincanas/', views.gincanas, name='mis_gincanas'),
    path('gincanas_publicas/', views.gincanas_publicas, name='gincanas_publicas'),
    path('mis_gincanas/crear/', views.crear_gincana, name='crear_gincana'),
    path('mis_gincanas/<int:gincana_id>/', views.gincana, name='gincana'),
    path('gincanas_publicas/<int:gincana_id>/', views.gincana_publica, name='gincana_publica'),
    path('mis_gincanas/<int:gincana_id>/completada', views.gincana_completada, name='gincana_completada'),
    path('mis_gincanas/<int:gincana_id>/eliminar', views.gincana_eliminar, name='gincana_eliminar'),
    path('logout/', views.signout, name='logout'),
    path('informacion/', views.informacion, name='informacion'),
    path('', views.signin, name='signin')
]
