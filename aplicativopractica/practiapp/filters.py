import django_filters
from django_filters import CharFilter

from .models import *

class filtoferta(django_filters.FilterSet):
    titulo = CharFilter(field_name='titulo', lookup_expr='icontains', label='Titulo')
    salario = CharFilter(field_name='salario', lookup_expr='gte', label='Salario Esperado')

    class Meta:
        model = oferta
        fields = ['titulo', 'area','ciudad','salario']