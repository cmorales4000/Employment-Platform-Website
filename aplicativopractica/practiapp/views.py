from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import oferta, Usuario, aplicantes, ciudad, area
from .forms import formoferta, formperfil, formusuario, formaplicar
from .filters import filtoferta
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
from django.views.generic import View, CreateView, ListView, DetailView, TemplateView, UpdateView
from django.urls import reverse_lazy
from rest_framework import serializers, viewsets
from .serializers import usuarioSerial, ofertaSerial, aplicantesSerial, CiudadSerial, AreaSerial, LoginSerial
from django_filters import rest_framework as filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password


############################################### APIS SERIALIZERS #########################################################

class usuarioAPI(viewsets.ModelViewSet):
    queryset=Usuario.objects.all()
    serializer_class=usuarioSerial



class LoginFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='iexact', label='username')
    password = filters.CharFilter(field_name='password', lookup_expr='iexact', label='password')
    

    class Meta:
        model=Usuario
        fields = ('username','password')


class LoginAPI(viewsets.ModelViewSet):
    queryset=Usuario.objects.all()
    serializer_class=LoginSerial
    filterset_class = LoginFilter



class OfertaFilter(filters.FilterSet):
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains', label='Titulo')
    salario = filters.CharFilter(field_name='salario', lookup_expr='gte', label='Salario Esperado')

    class Meta:
        model=oferta
        fields = ('titulo', 'area', 'ciudad', 'salario')

class ofertaAPI(viewsets.ModelViewSet):
    queryset=oferta.objects.all()
    serializer_class=ofertaSerial
    filterset_class = OfertaFilter
    authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    

class aplicantesAPI(viewsets.ModelViewSet):
    queryset=aplicantes.objects.all()
    serializer_class=aplicantesSerial

class CityAPI(viewsets.ModelViewSet):
    queryset=ciudad.objects.all()
    serializer_class=CiudadSerial

class AreaAPI(viewsets.ModelViewSet):
    queryset=area.objects.all()
    serializer_class=AreaSerial


#################################################### VIEWS PRACTIAPP #####################################################

class Home(TemplateView):
    template_name='practiapp/home.html'


class Buscar(ListView):
    model = oferta
    template_name = 'practiapp/buscar.html'

    def get(self, request):
        varofertas = oferta.objects.all()

        myfilter = filtoferta(request.GET, queryset=varofertas)
        varofertas = myfilter.qs
        
        data = {'ofertas':varofertas, 'myfilter':myfilter}
        return render(request, self.template_name, data)



class Aplicadas(ListView):
    model = aplicantes
    template_name = 'practiapp/aplicadas.html'

    def get(self, request, *args, **kwargs):
        variableid = request.user
        varaplicadas = aplicantes.objects.filter(aplicante=variableid)
        return render(request, self.template_name,{'aplicadas':varaplicadas})
        



class Ver(ListView):
    model = oferta
    template_name = 'practiapp/ver.html'

    def get(self, request, id, **kwargs):
        
        varoferta = oferta.objects.filter(id=id)
        return render(request, self.template_name,{'oferta':varoferta})


@login_required
def aplicar(request, id):
    
    try:
        form=formaplicar(data=request.POST, files=request.FILES)
        formulario = form.save(commit=False)
        formulario.ofertaaplicada = oferta.objects.get(id=id)
        formulario.aplicante = request.user
        formulario.save()
                
        mensaje="Aplicación Exitosa"
        return render(request,'practiapp/ver.html',{'oferta':oferta.objects.filter(id=id),'mensaje':mensaje})
        
    except:
        
        mensaje="Ya has aplicado"
        return render(request,'practiapp/ver.html',{'oferta':oferta.objects.filter(id=id),'mensaje':mensaje})
        


            




#################################################### VIEWS EMPRESA #####################################################


class Listar(ListView):
    model = oferta
    template_name = 'empresa/listar.html'

    def get(self, request, *args, **kwargs):
        variableid = request.user
        varofertas = oferta.objects.filter(empresa=variableid)
        return render(request, self.template_name,{'ofertas':varofertas}) 


class Aplicantes(ListView):
    model = aplicantes
    template_name = 'empresa/aplicantes.html'

    def get(self, request, id, **kwargs):
        ofertaid = oferta.objects.get(id=id)
        varaplicante = aplicantes.objects.filter(ofertaaplicada=ofertaid)
        return render(request, self.template_name,{'aplicantes':varaplicante}) 


@login_required
def agregar(request):
    data = {}

    if request.method == 'POST':
        form = formoferta(request.POST, request.FILES)
            
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.empresa = request.user
            formulario.save()
                
            return redirect('/')
    else:
        form = formoferta()
            
    data['form'] = form
        
    return render(request,'empresa/oferta.html', data)

@login_required
def modificar(request, id):
    varoferta = oferta.objects.get(id=id)
    form = formoferta(instance=varoferta)
    
    if request.method=='POST':
        formulario=formoferta(data=request.POST, files=request.FILES, instance=varoferta)

        if formulario.is_valid():
            formulario.save()
            return redirect('listar')
            # data['form'] = formoferta(instance=oferta.objects.get(id=id))

    data = {'form':form}
    return render(request, 'empresa/oferta.html', data)


@login_required
def eliminar(request, id):
    varoferta = oferta.objects.get(id=id)
    varoferta.delete()
    return redirect(to="listar")



#################################################### VIEWS REGISTRATION #####################################################

def registro(request):
    data = {'form':formusuario()}
    
    if request.method == 'POST':
        formulario = formusuario(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return redirect(to='home')
        
        else:
            data['mensaje']="No se ha podido crear el usuario, verifique los campos"

            
    return render(request, 'registration/registro.html', data)


@login_required
def perfil(request):
    varusuario = request.user
    data={'form':formperfil(instance=varusuario),'mensaje':"Favor confirmar su contraseña para guardar cambios" }
    
    if request.method=='POST':
        formulario=formperfil(data=request.POST, files=request.FILES, instance=varusuario)
        
        if formulario.is_valid():
            
            formulario.save()

            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            data['mensaje']="Perfil Modificado Correctamente"
            data['form'] = formperfil(instance=varusuario)
        
        else:
            data['mensaje']="No se han podido modificar sus datos, revise nuevamente"
            

    return render(request, 'registration/perfil.html', data)






#################################################### PRUEBAS #####################################################


def ver_oferta(request, id):
    
    varoferta = oferta.objects.get(id=id)
    data={
        'form':formoferta(instance=varoferta)
    }
    if request.method=='POST':
        formulario=formoferta(data=request.POST, instance=varoferta, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            data['mensaje']="Haz Aplicado Correctamente"
            
            data['form'] = formoferta(instance=oferta.objects.get(id=id))

    return render(request, 'practiapp/ver_oferta.html', data)




def listado_aplicantes(request, id):
    
    ofertaid = oferta.objects.get(id=id)
    varaplicante = aplicantes.objects.filter(ofertaaplicada=ofertaid)

    data = {
        'aplicantes':varaplicante
    }
    return render(request, 'practiapp/listado_aplicantes.html', data)



def ver_aplicantes(request, id):
    varoferta = oferta.objects.get(id=id)
    data={
        'form':formaplicar(instance=varoferta)
    }
    if request.method=='POST':
        formulario=formaplicar(data=request.POST, instance=varoferta, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            data['mensaje']="Publicación Modificada Correctamente"
            #data['form'] = formulario
            data['form'] = formaplicar(instance=oferta.objects.get(id=id))

    return render(request, 'practiapp/ver_aplicantes.html', data)


def buscar(request):

    varofertas = oferta.objects.all()
    data = {
        'ofertas':varofertas
    }
    return render(request, 'practiapp/buscar.html', data)


class Aplicadas2(ListView):
    model = oferta
    template_name = 'practiapp/aplicadas.html'

    def get(self, request, *args, **kwargs):
        variableid = request.user
        varaplicadas = oferta.objects.filter(apply=variableid)
        return render(request, self.template_name,{'aplicadas':varaplicadas.all()})



