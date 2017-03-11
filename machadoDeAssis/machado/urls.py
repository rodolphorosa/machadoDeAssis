from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views
from .models import Genero

# app_name = 'machado'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^obra-completa/$', views.exibirObraCompleta, name='obraCompleta'),
	url(r'^obra-completa/filtro/$', views.filtrarObraCompleta, name="filtrarObraCompleta"),
	url(r'^resultados/filtro$', views.filtrarResultadosBusca, name="filtrarResultadosBusca"),
	url(r'^resultados/$', views.detalharResultadosBusca, name="resultadosBusca"),
	url(r'^genero=(?P<pk>[0-9]+)/$', views.detalharGenero, name="detalharGenero"),
	url(r'^obra=(?P<pk>[0-9]+)/$', views.detalharObra, name="descricao"),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

