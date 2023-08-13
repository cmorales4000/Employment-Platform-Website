"""aplicativopractica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import urls, routers
from practiapp.views import usuarioAPI, ofertaAPI, aplicantesAPI, CityAPI, AreaAPI, LoginAPI
from rest_framework.authtoken import views
#from django.contrib.auth.views import LoginView



apiurl = routers.SimpleRouter()
apiurl.register('usuarios', usuarioAPI)
apiurl.register('oferta', ofertaAPI)
apiurl.register('aplicantes', aplicantesAPI)
apiurl.register('ciudad', CityAPI)
apiurl.register('area', AreaAPI)
apiurl.register('loguser', LoginAPI)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apiurl.urls)),
    path('', include('practiapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('pwa.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    #path('login/', LoginView.as_view(), name='login')
] 


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Practiapp"
admin.site.index_title = "Administración de Modulos"
admin.site.site_title = "Practiapp"



