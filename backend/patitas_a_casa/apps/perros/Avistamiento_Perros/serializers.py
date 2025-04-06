from rest_framework import serializers
from .models import AvistamientoPerro

class AvistamientoPerroSerializer(serializers.ModelSerializer):
    tipo_usuario = serializers.SerializerMethodField()
    nombre_reportante = serializers.SerializerMethodField()
    
    class Meta:
        model = AvistamientoPerro
        fields = [
            'id', 'fecha_hora_avistamiento', 'fecha_reporte',
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal',
            'colonia', 'calle', 'numero_exterior',
            'foto', 'raza', 'sexo', 'tamaño', 'color_dominante',
            'señas_particulares', 'identificador', 'estado_perro',
            'descripcion', 'es_anonimo', 'tipo_usuario', 'nombre_reportante',
            'puede_albergar'
        ]
        read_only_fields = ['id', 'fecha_reporte']
    
    def get_tipo_usuario(self, obj):
        if obj.es_anonimo:
            return "Anónimo"
        elif obj.reportado_por_usuario:
            return "Persona"
        elif obj.reportado_por_albergue:
            return "Albergue"
        return "Desconocido"
    
    def get_nombre_reportante(self, obj):
        if obj.es_anonimo:
            return "Anónimo"
        elif obj.reportado_por_usuario:
            return f"{obj.reportado_por_usuario.nombre} {obj.reportado_por_usuario.apellido}"
        elif obj.reportado_por_albergue:
            return obj.reportado_por_albergue.nombre
        return "Desconocido"

class AvistamientoAnonimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvistamientoPerro
        fields = [
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal',
            'colonia', 'calle', 'numero_exterior', 'fecha_hora_avistamiento',
            'foto', 'raza', 'sexo', 'tamaño', 'color_dominante',
            'señas_particulares', 'identificador', 'estado_perro', 'descripcion'
        ]
    
    def create(self, validated_data):
        validated_data['es_anonimo'] = True
        return super().create(validated_data)

class AvistamientoPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvistamientoPerro
        fields = [
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal',
            'colonia', 'calle', 'numero_exterior', 'fecha_hora_avistamiento',
            'foto', 'raza', 'sexo', 'tamaño', 'color_dominante',
            'señas_particulares', 'identificador', 'estado_perro',
            'puede_albergar', 'descripcion'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        try:
            usuario = user.usuario_persona
            validated_data['reportado_por_usuario'] = usuario
            validated_data['es_anonimo'] = False
            return super().create(validated_data)
        except:
            raise serializers.ValidationError("El usuario no tiene un perfil de persona registrado")

class AvistamientoAlbergueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvistamientoPerro
        fields = [
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal',
            'colonia', 'calle', 'numero_exterior', 'fecha_hora_avistamiento',
            'foto', 'raza', 'sexo', 'tamaño', 'color_dominante',
            'señas_particulares', 'identificador', 'estado_perro', 'descripcion'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        try:
            albergue = user.albergue
            validated_data['reportado_por_albergue'] = albergue
            validated_data['es_anonimo'] = False
            return super().create(validated_data)
        except:
            raise serializers.ValidationError("El usuario no tiene un perfil de albergue registrado")