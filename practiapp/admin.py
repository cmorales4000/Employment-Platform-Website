from django.contrib import admin
from .models import oferta, area, ciudad, Usuario, aplicantes
from .forms import formoferta
from django.utils.html import format_html


# Register your models here.

class ofertaadmin(admin.ModelAdmin):
    readonly_fields=("created", "updated")
    list_display = ['titulo', 'area', 'ciudad', 'salario']
    search_fields = ['titulo']
    list_filter = ['area']
    list_per_page = 15


class usuarioadmin(admin.ModelAdmin):
    list_display = ('username', 'nombre', 'dni', 'imagen', 'hdv')

    def save_model(self, request, obj, form, change):
    
        if obj.pk:
            orig_obj = Usuario.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


class areaadmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')



admin.site.register(Usuario, usuarioadmin)
admin.site.register(area, areaadmin)
admin.site.register(ciudad)
admin.site.register(oferta, ofertaadmin)
admin.site.register(aplicantes)

