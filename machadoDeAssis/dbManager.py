from machado.models import *
from mapeador import Mapeador

def recuperarGeneros():
	return Genero.objects.all()

def recuperarGeneroPorNome(genero):
	return Genero.objects.get(genero=genero)

def recuperarObras():
	return Obra.objects.all()

def recuperarObraPorNome(titulo):
	return Obra.objects.get(titulo=titulo)

def recuperarSubtitulos():
	return Subtitulo.objects.all()

def recuperarSubtituloPorNome(subtitulo):
	return Subtitulo.objects.get(subtitulo=subtitulo)

def persistirObras():
	mapeador = Mapeador()

	obras = mapeador.carregarDados()

	for chave in obras.keys():
		obra = obras[chave]

		genero = recuperarGeneroPorNome(obra['genero'])

		genero.obra_set.create(titulo=obra['titulo'], ano=obra['ano'], caminho=obra['caminho'])

		novaObra = recuperarObraPorNome(obra['titulo'])

		if len(obra['subtitulos']) > 0:
			for subtitulo in obra['subtitulos']:
				novaObra.subtitulo_set.create(subtitulo=subtitulo) 