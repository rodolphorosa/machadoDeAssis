from django.db import models

"""
Genero de uma obra.

"""
class Genero(models.Model):
	""" Texto do genero (vindo ao arquivo). """
	genero = models.CharField(max_length=30)

	""" Texto do genero com acentuacao. """
	nome_site = models.CharField(max_length=30)

	""" Retorna o texto do genero. """
	def __str__(self):
		return self.nome_site.title()

"""
Obra do Machado de Assis.

"""
class Obra(models.Model):
	""" Genero da obra. """
	genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

	""" Titulo da obra """
	titulo = models.CharField(max_length=200)

	""" Ano da obra. """
	ano = models.IntegerField()	
	
	""" Caminho do texto da obra no servidor. """
	caminho = models.CharField(max_length=200)

	""" Retorna o titulo da obra. """
	def __str__(self):
		return self.titulo

""" 
Substitulo de uma obra.

"""
class Subtitulo(models.Model):
	""" Obra a qual o subtitulo pertence. """
	obra = models.ForeignKey(Obra, on_delete=models.CASCADE)

	""" Texto do subtitulo. """
	subtitulo = models.CharField(max_length=200)

	""" Retorna o texto do subtitulo. """
	def __str__(self):
		return self.subtitulo
		