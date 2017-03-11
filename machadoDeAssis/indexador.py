import re, os.path

from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser, OrGroup, AndGroup
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.index import create_in, open_dir

import dbManager

class Indexador:
	
	obras = dbManager.recuperarObras()

	index_path = "whoosh_index"	
	analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang="pt")
	
	schema = Schema(
		pk = NUMERIC(int, stored=True),
		titulo = TEXT(analyzer=analyzer, stored=True), 
		subtitulos = TEXT(analyzer=analyzer, stored=True), 
		conteudo = TEXT(analyzer=analyzer, stored=True)
	)

	if not os.path.exists(index_path):
		os.mkdir(index_path)
		index = create_in(index_path, schema)

		writer = index.writer()

		try:
			for obra in obras:
				subtitulos 	= [subtitulo.subtitulo for subtitulo in obra.subtitulo_set.all()]
				subtitulos 	= " ".join(subtitulos)
				conteudo 	= open(obra.caminho).read()
				
				writer.add_document(
					pk = obra.id,
					titulo = obra.titulo,
					subtitulos = subtitulos,
					conteudo = conteudo
				)

			writer.commit()
		finally:
			index.close()
	else:
		index = open_dir(index_path)

if __name__ == "__main__":
	indexador = Indexador()