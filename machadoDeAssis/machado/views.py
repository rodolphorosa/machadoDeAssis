from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import *

from .buscador import Buscador

def index(request):
	request.session.flush()
	
	generos = Genero.objects.order_by('genero')
	context = {'generos':generos}
	
	return render(request, "machado/index.html", context)

def detalharGenero(request, pk):
	request.session.flush()
	
	generos = Genero.objects.order_by('genero')

	genero = Genero.objects.get(pk=pk)

	listaDeObras = genero.obra_set.all()
	
	paginator = Paginator(listaDeObras, 30)
	
	page = request.GET.get('page')

	try:
		obras = paginator.page(page)
	except PageNotAnInteger:
		obras = paginator.page(1)
	except EmptyPage:
		obras = paginator.page(paginator.num_pages)	
	
	context = {'obras': obras, 'generos': generos, 'genero_escolhido':genero}
	
	return render(request, "machado/obras.html", context)

def detalharObra(request, pk):
	request.session.flush()

	generos = Genero.objects.order_by('genero')
	
	obra = Obra.objects.get(pk=pk)
	context = {'obra':obra, 'generos':generos}
	
	return render(request, "machado/descricao.html", context)

def detalharResultadosBusca(request):
	request.session.flush()
	
	buscador 	= Buscador()
	entrada 	= request.GET.get('entrada')
	saida 		= buscador.obterResultadosBusca(entrada)
	resultados 	= saida['resultados']
	chaves 		= [ r['pk'] for r in resultados ]
	obras 		= Obra.objects.filter(pk__in=chaves)

	generos 		= Genero.objects.order_by('genero')
	generosFiltro 	= Genero.objects.filter(pk__in=obras.values_list('genero', flat=True))

	context = {'obras':obras, 'generos':generos, 'generosFiltro':generosFiltro}

	try:
		context['corrigido'] = saida['corrigido']
	except:
		pass

	request.session['resultados'] = chaves

	return render(request, "machado/resultados.html", context)

def exibirObraCompleta(request):
	request.session.flush()

	generos = Genero.objects.order_by('genero')	

	obraCompleta = Obra.objects.order_by('titulo')
	
	paginator = Paginator(obraCompleta, 30)
	
	page = request.GET.get('page')

	try:
		obras = paginator.page(page)
	except PageNotAnInteger:
		obras = paginator.page(1)
	except EmptyPage:
		obras = paginator.page(paginator.num_pages)	
	
	context = {'obras': obras, 'generos': generos}
	
	return render(request, "machado/obra_completa.html", context)

def filtrarObraCompleta(request):

	checked_generos = list(map(int, request.POST.getlist('genero')))
	checked_ordenar = request.POST.get('ordenar')

	obras = Obra.objects.all()

	if checked_generos:
		obras = obras.filter(genero__in=checked_generos)
	
	if checked_ordenar:
		obras = obras.order_by(checked_ordenar)

	paginator = Paginator(obras, 30)
	
	page = request.GET.get('page')

	try:
		obras = paginator.page(page)
	except PageNotAnInteger:
		obras = paginator.page(1)
	except EmptyPage:
		obras = paginator.page(paginator.num_pages)	
	
	context = {'obras':obras, 'generos':Genero.objects.order_by('genero')}
	
	request.session['checked_generos'] = checked_generos
	request.session['checked_ordenar'] = checked_ordenar

	return render(request, "machado/obra_completa.html", context)

def filtrarResultadosBusca(request):

	checked_generos = list(map(int, request.POST.getlist('genero')))
	checked_ordenar = request.POST.get('ordenar')

	chaves = request.session['resultados']
	obras = Obra.objects.filter(pk__in=chaves)
	generosFiltro = Genero.objects.filter(pk__in=obras.values_list('genero', flat=True))

	if checked_generos:
		obras = obras.filter(genero__in=checked_generos)
	
	if checked_ordenar:
		obras = obras.order_by(checked_ordenar)

	paginator = Paginator(obras, 30)
	
	page = request.GET.get('page')

	try:
		obras = paginator.page(page)
	except PageNotAnInteger:
		obras = paginator.page(1)
	except EmptyPage:
		obras = paginator.page(paginator.num_pages)	
	
	context = {'obras':obras, 'generos':Genero.objects.order_by('genero'), 'generosFiltro':generosFiltro}
	
	request.session['checked_generos'] = checked_generos
	request.session['checked_ordenar'] = checked_ordenar

	return render(request, "machado/resultados.html", context)