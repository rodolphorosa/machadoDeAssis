# Carrega os dados #

import re

class Mapeador:
	machado 		= "CONTENTS"
	regex_livro 	= re.compile("^(\w+)/(\w+).txt: .*")
	regex_titulo 	= re.compile("\s+.*")
	regex_caminho	= re.compile("(\w+)/(\w+).txt")
	regex_anos 		= re.compile("\([0-9]{4}.*\)")

	def __init__(self):
		self.data = []

	""" Idenfica o ano da obra, quem vem inserida no titulo. """
	def encontrarAno(self, texto):
		anos = re.findall(self.regex_anos, texto)
		ano = re.findall(r'[0-9]{4}', anos[0])[0]
		return int(ano)

	""" Retorna um dicionario com todas as informacoes das obras do Machado de Assis. """
	def carregarDados(self):
		indice = 0
		""" Arquivo contendo todas as informacoes das obras. """
		informacoes = open(self.machado, encoding="utf-8")

		""" 
			Dicionario contendo todas as obras dividas em campos. 
			'titulo': Titulo da obra.
			'subtitulos': Subtitulos da obra.
			'ano': Data(s) da obra.
			'genero': Genero da obra.
			'caminho': Caminho da obra no servidor.
		"""
		dados = {}

		for linha in informacoes:

			if (re.match(self.regex_livro, linha)):
				""" Dicionario contendo os campos de uma obra. """
				campos = {}

				titulo = re.search(self.regex_titulo, linha)

				""" Separa o titulo e os subtitulos da obra. """
				if titulo:
					titulos = [ token.strip() for token in re.split("[;]", titulo.group(0)) ]
					campos['titulo'] = titulos[0]
					campos['subtitulos'] = titulos[1:]
					campos['ano'] = self.encontrarAno(titulo.group(0))

				caminho = re.search(self.regex_caminho, linha)

				""" Separa o caminho da obra no servidor e a informacao do genero. """
				if caminho:
					tokens = re.split("[/]", caminho.group(0))
					campos['genero'] = tokens[0]
					campos['caminho'] = "obras/" + caminho.group(0)

				dados[indice] = campos
				indice += 1

		return dados 