# Motor de busca #

import re, os.path
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter, StandardAnalyzer
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser, OrGroup, AndGroup
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.index import create_in, open_dir

from mapper import load

data = load() # Carrega um dicionario com a descrição das obras

index_path = "whoosh_index"	# Indice dos documentos
analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang="pt") 
schema = Schema(title=TEXT(analyzer=analyzer, stored=True), 
	subtitles=TEXT(analyzer=analyzer, stored=True), 
	content=TEXT(analyzer=analyzer, stored=True), 
	genre=TEXT(stored=True), 
	date=TEXT(stored=True), 
	path=TEXT(stored=False)) 

if not os.path.exists(index_path):
	os.mkdir(index_path)
	index = create_in(index_path, schema)

	writer = index.writer()

	try:
		for i in data.keys():
			fields = data[i]
			content = open(data[i]['path']).read()
			writer.add_document(title=fields['title'], subtitles=fields['subtitles'], genre=fields['genre'], content=content, date=fields['date'], path=fields['path'])
		writer.commit()
	finally:
		index.close()
else:
	index = open_dir(index_path)

searcher = index.searcher()

queries = {'subtitles' : 'a mulher de preto é de que livro'}

# Retorna uma query (string) dados o nome de um campo e um valor
def fieldQuery(field, value):
	parser 	= QueryParser(field, schema, group=OrGroup)
	query 	= parser.parse(value)
	return str(query)

def searchFields(userqueries): 
	queries 	= [fieldQuery(fieldname, userqueries[fieldname]) for fieldname in userqueries.keys()]
	querystring = " AND ".join(queries)
	parser 		= MultifieldParser([fieldname for fieldname in userqueries.keys()], schema)
	query 		= parser.parse(querystring)
	# print(query)
	try:
		results = searcher.search(query, terms=True)
		for result in results:
			print(result['title'])
	finally:
		searcher.close()
		index.close()

searchFields(queries)