from rest_framework import serializers
from apps.anuncio.models import Anuncio, Categoria
from apps.usuario.models import Usuario
from django.utils import timezone

class CategoriaSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Categoria
        fields= [
            'id',
            'nombre',
            'activa'
        ]



# Heredamos de Serializer (no ModelSerializer). 
# Solo definimos los campos que esperamos recibir. Es decir, no hay validación de DB, ni de duplicados, ni nada. Solo validación de tipos y formatos.
class CategoriaAnidadaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=100)
    activa = serializers.BooleanField(default=True, required=False)



class AnuncioSerializer(serializers.ModelSerializer):
    # Usamos el serializador "puro"
    categorias = CategoriaAnidadaSerializer(many=True, required=False)
    
    class Meta:
        model= Anuncio
        fields = [
            'id', 'titulo', 'descripcion', 'precio_inicial', 'imagen',
            'fecha_inicio', 'fecha_fin', 'activo', 'categorias',
            'publicado_por', 'oferta_ganadora'
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']


    def validate_precio_inicial(self, data):
        request = self.context.get('request') #permite tener contexto de la view en el serializador, si no existe devuelve None
        if request.version == '2':
            if data < 50:
                raise serializers.ValidationError("El precio inicial debe ser mayor o igual a $50")
        elif data <= 0:
            raise serializers.ValidationError("El precio inicial debe ser mayor a $0")

        return data
    
    def validate_fecha_inicio(self, data):
        current_date = timezone.localtime(timezone.now())

        if data < current_date:
            raise serializers.ValidationError(f"La fecha ingresada debe ser superior que la actual - Fecha Actual {current_date}")
        return data
    
    def validate(self, data):
        if data['fecha_fin'] < data['fecha_inicio']:
            raise serializers.ValidationError("La fecha de fin debe ser superior a la fecha inicio")
        return data

    # Usamos to_representation para modificar la respuesta que se le da al cliente. En este caso, queremos devolver el objeto completo de las categorías, no solo su id.
    def to_representation(self, instance):
        #Usamos super() para mantener la funcionalidad original del método y luego modificamos la representación según nuestras necesidades.
        representation = super().to_representation(instance)
        # Devolvemos el objeto completo con todas las categorías asociadas al anuncio, usando el serializador de categoría para cada una de ellas.
        representation['categorias'] = CategoriaSerializer(instance.categorias.all(), many=True).data
        return representation