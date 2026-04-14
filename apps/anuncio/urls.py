from django.urls import include, path
from .views import AnuncioDetalleAPIView, AnuncioListaAPIView, CategoriaDetalleAPIView, CategoriaListaAPIView, AnuncioListaGenericView, AnuncioDetalleGenericView

app_name = 'anuncio'

urlpatterns = [
    #api view categoria
    path('api-view/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),

    #api view anuncio
    path('api-view/anuncio/', AnuncioListaAPIView.as_view()),
    path('api-view/anuncio/<pk>/', AnuncioDetalleAPIView.as_view()),

    #generic view
    path('generic-view/anuncio/', AnuncioListaGenericView.as_view()),
    path('generic-view/anuncio/<pk>/', AnuncioDetalleGenericView.as_view()),

    #router
    path('view-set/', include('apps.anuncio.router'))
]
    

