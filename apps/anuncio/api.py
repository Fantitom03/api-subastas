from rest_framework import viewsets
from .models import Anuncio
from apps.usuario.models import Usuario
from .serializers import AnuncioSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404

class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def perform_create(self, serializer):
        usuario_a_asignar = Usuario.objects.first()

        serializer.save(publicado_por=usuario_a_asignar)

    @action(detail=True, methods=['get'])
    def get_remaining_time(self, request, pk=None):
        anuncio = get_object_or_404(Anuncio, pk=pk)

        last_date = anuncio.fecha_fin
        current_date = timezone.localtime(timezone.now())
        
        remaining_time = last_date - current_date

        if request.version == '2': 
            return Response(
                {
                    'status': 'Pronto a finalizar' if remaining_time.days < 2 else 'Lejos de finalizar',
                    'message': f'Quedan {remaining_time.days} Dias {remaining_time.seconds // 3600} Horas {(remaining_time.seconds // 60) % 60} Minutos',
                }  
            )

        return Response(
            {
                'dias': remaining_time.days,
                'horas': remaining_time.seconds // 3600,
                'minutos': (remaining_time.seconds // 60) % 60,
            } 
        ) 


