from rest_framework import serializers
from .models import oferta, Usuario, aplicantes, area, ciudad




class usuarioSerial(serializers.ModelSerializer):
    queryset = Usuario.objects.all()

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model=Usuario
        fields=['is_empresa','username','nombre','dni','email','contacto','imagen','hdv','password']

class LoginSerial(serializers.ModelSerializer):

    class Meta:
        model=Usuario
        fields=['id']



class AreaSerial(serializers.ModelSerializer):
    class Meta:
        model=area
        fields = ['nombre']

class CiudadSerial(serializers.ModelSerializer):
    class Meta:
        model=ciudad
        fields = ['nombre']



class ofertaSerial(serializers.ModelSerializer):

    class Meta:
        model=oferta
        fields = ['id','titulo', 'contenido', 'salario', 'horario', 'logoempresa', 'nombreempresa', 'nombrearea', 'nombreciudad']


class aplicantesSerial(serializers.ModelSerializer):
    class Meta:
        model=aplicantes
        fields = ['ofertaaplicada','titulooferta','aplicante','nombreaplicante']

