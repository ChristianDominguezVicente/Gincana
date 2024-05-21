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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('password/', views.password, name='password'),
    path('password/<str:email>/', views.password_cambio, name='password_cambio'),
    path('verificacion/<str:email>/', views.verificacion, name='verificacion'),
    path('verificacion/<str:email>/reenviar/', views.verificacion_reenviar, name='verificacion_reenviar'),
    path('mis_gincanas/', views.gincanas, name='mis_gincanas'),
    path('gincanas_publicas/', views.gincanas_publicas, name='gincanas_publicas'),
    path('mis_gincanas/crear/', views.crear_gincana, name='crear_gincana'),
    path('mis_gincanas/<int:gincana_id>/', views.gincana, name='gincana'),
    path('gincanas_publicas/<int:gincana_id>/', views.gincana_publica, name='gincana_publica'),
    path('gincanas_publicas/<int:gincana_id>/gincana_copiar/', views.gincana_copiar, name='gincana_copiar'),
    path('mis_gincanas/<int:gincana_id>/iniciar/', views.gincana_iniciar, name='gincana_iniciar'),
    path('mis_gincanas/<int:gincana_id>/editar/', views.editar_gincana, name='editar_gincana'),
    path('mis_gincanas/<int:gincana_id>/configuracion/', views.configuracion_gincana, name='configuracion_gincana'),
    path('mis_gincanas/<int:gincana_id>/puntuacion/', views.puntuacion_gincana, name='puntuacion_gincana'),
    path('mis_gincanas/<int:gincana_id>/eliminar/', views.gincana_eliminar, name='gincana_eliminar'),
    path('mis_gincanas/<int:gincana_id>/usuarios_invitados/', views.usuarios_invitados, name='usuarios_invitados'),
    path('mis_gincanas/<int:gincana_id>/usuarios_invitados/crear/', views.crear_usuarios_invitados, name='crear_usuarios_invitados'),
    path('mis_gincanas/<int:gincana_id>/usuarios_invitados/borrar/<str:usuario>/', views.borrar_usuarios_invitados, name='borrar_usuarios_invitados'),
    path('logout/', views.signout, name='logout'),
    path('informacion/', views.informacion, name='informacion'),
    path('profesor/<str:email_id>/', views.profesor, name='profesor'),
    path('profesor/<str:email_id>/password/', views.profesor_password, name='profesor_password'),
    path('profesor/<str:email_id>/verificacion/', views.verificacion_password, name='verificacion_password'),
    path('profesor/<str:email_id>/verificacion2/', views.verificacion_password2, name='verificacion_password2'),
    path('profesor/<str:email_id>/eliminar/', views.profesor_eliminar, name='profesor_eliminar'),
    path('profesor/<str:email_id>/editar/', views.editar_profesor, name='editar_profesor'),
    path('mis_gincanas/<int:gincana_id>/editar/parada/', views.parada, name='parada'),
    path('mis_gincanas/<int:gincana_id>/editar/parada/guardar/', views.parada_guardar, name='parada_guardar'),
    path('mis_gincanas/<int:gincana_id>/editar/guardar_cambios_gincana/', views.guardar_cambios_gincana, name='guardar_cambios_gincana'),
    path('mis_gincanas/<int:gincana_id>/editar/borrar_parada/', views.borrar_parada, name='borrar_parada'),
    path('mis_gincanas/<int:gincana_id>/editar/<int:parada_id>/', views.editar_parada, name='editar_parada'),
    path('mis_gincanas/<int:gincana_id>/editar/<int:parada_id>/guardar/', views.editar_guardar, name='editar_guardar'),
    path('buscar/', views.buscar_gincanas, name='buscar_gincanas'),
    path('update_dark_mode/', views.update_dark_mode, name='update_dark_mode'),
    path('centro_de_ayuda/', views.centro_de_ayuda, name='centro_de_ayuda'),
    path('signin_profesor/', views.signin, name='signin'),
    path('', views.selector, name='selector'),
    path('signin_invitado/', views.signin_invitado, name='signin_invitado'),
    path('invitado_gincana/<int:gincana_id>/<str:invitado>/', views.invitado_gincana, name='invitado_gincana'),
    path('invitado_gincana/<int:gincana_id>/<str:invitado>/responder/', views.invitado_gincana_iniciar, name='invitado_gincana_iniciar'),
    path('invitado_gincana/<int:gincana_id>/<str:invitado>/responder/<int:parada>/', views.invitado_responder, name='invitado_responder'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)