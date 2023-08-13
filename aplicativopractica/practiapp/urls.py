from django.urls import path

from practiapp import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    
    path('', views.Home.as_view(), name="home"),
    path('registro', views.registro, name="registro"),
    path('perfil',views.perfil,name="perfil"),
    
    path('buscar', views.Buscar.as_view(), name="buscar"),
    path('ver/<id>/', views.Ver.as_view(), name="ver"),
    path('aplicar/<id>/', views.aplicar, name="aplicar"),
    path('aplicadas', views.Aplicadas.as_view(), name="aplicadas"),

    path('agregar',views.agregar,name="agregar"),
    path('modificar/<id>/', views.modificar, name="modificar"),
    path('eliminar/<id>/', views.eliminar, name="eliminar"),
    path('listar', views.Listar.as_view(), name="listar"),
    path('aplicantes/<id>/',views.Aplicantes.as_view(),name="aplicantes"),
    
]

