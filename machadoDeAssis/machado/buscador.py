import re, os.path

from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser, OrGroup, AndGroup
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.index import create_in, open_dir

class Buscador:

	index_path = "whoosh_index"
	analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang="pt")
	
	schema = Schema(
		pk = NUMERIC(int, stored=True),
		titulo = TEXT(analyzer=analyzer, stored=True), 
		subtitulos = TEXT(analyzer=analyzer, stored=True), 
		conteudo = TEXT(analyzer=analyzer, stored=True)
	)

	if not os.path.exists(index_path):
		print("Diretório não existe.")
	else:
		index = open_dir(index_path)
	
	buscador = index.searcher()

	def obterQueryCampo(self, nomeDoCampo, entradaDoUsuario):
		qp = QueryParser(nomeDoCampo, self.schema, group=OrGroup)

		try:
			query = qp.parse(entradaDoUsuario)
		except:
			query = ""
		return str(query)

	def obterQueryBuscaUsuario(self, entradaDoUsuario):
		campos 	= ['titulo', 'subtitulos', 'conteudo']		
		mp 		= MultifieldParser(campos, self.schema, group=OrGroup)
		query 	= mp.parse(entradaDoUsuario)
		
		return query

	def obterResultadosBusca(self, entradaDoUsuario):
		queryDoUsuario = self.obterQueryBuscaUsuario(entradaDoUsuario)
		
		try:
			resultados = self.buscador.search(queryDoUsuario, terms=True)

			saida = {'resultados':resultados}

			corrector = self.buscador.correct_query(queryDoUsuario, entradaDoUsuario)
			
			if corrector.query != queryDoUsuario:
				saida['corrigido'] = corrector.string

			return saida
		except:
			return 

	def fechar(self):
		self.buscador.close()
		self.index.close() 