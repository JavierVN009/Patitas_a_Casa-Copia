from rest_framework import serializers
from .models import PerroPerdido, FotoPerroPerdido

class FotoPerroPerdidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoPerroPerdido
        fields = ['id', 'foto', 'es_principal', 'fecha_subida']


class PerroPerdidoListSerializer(serializers.ModelSerializer):
    foto_principal = serializers.SerializerMethodField()
    edad_formateada = serializers.CharField(source='get_edad_formateada', read_only=True)
    tiempo_perdido = serializers.CharField(source='get_tiempo_perdido', read_only=True)
    sexo_display = serializers.CharField(source='get_sexo_display', read_only=True)
    tamaño_display = serializers.CharField(source='get_tamaño_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = PerroPerdido
        fields = [
            'id', 'nombre', 'raza', 'sexo', 'sexo_display', 'tamaño', 'tamaño_display',
            'entidad_federativa', 'municipio_alcaldia', 'fecha_hora_perdida', 
            'fecha_registro', 'estado', 'estado_display', 'edad_formateada', 
            'tiempo_perdido', 'foto_principal'
        ]
    
    def get_foto_principal(self, obj):
        foto_principal = obj.fotos.filter(es_principal=True).first()
        if not foto_principal:
            foto_principal = obj.fotos.first()
        
        if foto_principal:
            return self.context['request'].build_absolute_uri(foto_principal.foto.url)
        return None


class PerroPerdidoDetailSerializer(serializers.ModelSerializer):
    fotos = FotoPerroPerdidoSerializer(many=True, read_only=True)
    colores_list = serializers.SerializerMethodField()
    edad_formateada = serializers.CharField(source='get_edad_formateada', read_only=True)
    tiempo_perdido = serializers.CharField(source='get_tiempo_perdido', read_only=True)
    sexo_display = serializers.CharField(source='get_sexo_display', read_only=True)
    tamaño_display = serializers.CharField(source='get_tamaño_display', read_only=True)
    patron_pelaje_display = serializers.CharField(source='get_patron_pelaje_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    propietario_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = PerroPerdido
        fields = [
            'id', 'nombre', 'sexo', 'sexo_display', 'edad_años', 'edad_meses', 
            'edad_formateada', 'tamaño', 'tamaño_display', 'raza', 'esterilizado', 
            'colores', 'colores_list', 'patron_pelaje', 'patron_pelaje_display', 
            'señas_particulares', 'tiene_collar', 'color_collar', 'identificador',
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal', 'colonia', 
            'calle', 'numero_exterior', 'fecha_hora_perdida', 'fecha_registro',
            'propietario', 'propietario_nombre', 'estado', 'estado_display', 
            'fecha_actualizacion', 'tiempo_perdido', 'fotos'
        ]
    
    def get_colores_list(self, obj):
        if obj.colores:
            return obj.colores.split(',')
        return []
    
    def get_propietario_nombre(self, obj):
        if obj.propietario:
            return f"{obj.propietario.nombre} {obj.propietario.apellido}"
        return None


class PerroPerdidoCreateUpdateSerializer(serializers.ModelSerializer):
    colores_list = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    
    class Meta:
        model = PerroPerdido
        exclude = ['propietario', 'fecha_registro', 'estado', 'fecha_actualizacion', 'colores']
    
    def validate(self, data):
        colores_list = data.pop('colores_list', [])