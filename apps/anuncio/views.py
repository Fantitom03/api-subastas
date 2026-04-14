from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Anuncio, Categoria
from .serializers import AnuncioSerializer, CategoriaSerializer
from apps.usuario.models import Usuario



#Vistas APIView Categoría 
class CategoriaListaAPIView(APIView):
    def get(self, request, format=None):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoriaDetalleAPIView(APIView):
    
    def get(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    

#Vistas APIView Anuncio 
class AnuncioListaAPIView(APIView):
    def get(self,request, format=None):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AnuncioSerializer(data=request.data)
        if serializer.is_valid():
            # TEMPORAL: Forzamos la asignación del primer usuario
            usuario_prueba = Usuario.objects.first() 
            
            serializer.save(publicado_por=usuario_prueba) 
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AnuncioDetalleAPIView(APIView):
    def get(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#Vistas Anuncio GenericAPIView
class AnuncioListaGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def perform_create(self, serializer):
        # TEMPORAL: Forzamos la asignación del primer usuario
        usuario_prueba = Usuario.objects.first()
        serializer.save(publicado_por=usuario_prueba)

class AnuncioDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer