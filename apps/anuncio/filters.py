from django_filters import rest_framework as filters
from .models import Anuncio, Categoria

class AnuncioFilter(filters.FilterSet):
    # Filtro de búsqueda parcial para el título
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains')
    # Filtro por rango de precio inicial
    precio_min = filters.NumberFilter(field_name='precio_inicial', lookup_expr='gte')
    precio_max = filters.NumberFilter(field_name='precio_inicial', lookup_expr='lte')

    class Meta:
        model = Anuncio
        fields = ['activo', 'categorias', 'publicado_por']

class CategoriaFilter(filters.FilterSet):
    # Coincidencia parcial en el nombre de la categoría
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        model = Categoria
        fields = ['nombre', 'activa']