from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Usuario, Albergue, ServicioAlbergue

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']

class ServicioAlbergueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioAlbergue
        fields = ['id', 'nombre', 'descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    usuario_info = UserSerializer(source='usuario', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'usuario', 'usuario_info', 'nombre', 'apellido', 'telefono', 'fecha_registro']
        read_only_fields = ['id', 'fecha_registro']

class AlbergueSerializer(serializers.ModelSerializer):
    usuario_info = UserSerializer(source='usuario', read_only=True)
    servicios_info = ServicioAlbergueSerializer(source='servicios', many=True, read_only=True)
    
    class Meta:
        model = Albergue
        fields = [
            'id', 'usuario', 'usuario_info', 'nombre', 'telefono',
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal',
            'calle', 'numero_exterior', 'referencias',
            'nombre_responsable', 'apellido_responsable', 'correo_responsable',
            'capacidad_actual', 'capacidad_maxima', 'servicios', 'servicios_info',
            'facebook', 'instagram', 'twitter', 'sitio_web',
            'imagen1', 'imagen2', 'imagen3', 'imagen4',
            'fecha_registro', 'activo'
        ]
        read_only_fields = ['id', 'fecha_registro']

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class RegistroPersonaSerializer(serializers.Serializer):
    # Datos de autenticación
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    # Datos de perfil
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    telefono = serializers.CharField(max_length=15)
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso")
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado")
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        # Crear usuario
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Crear perfil de persona
        usuario = Usuario.objects.create(
            usuario=user,
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            telefono=validated_data['telefono']
        )
        
        return usuario

class RegistroAlbergueSerializer(serializers.Serializer):
    # Datos de autenticación
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharFiel