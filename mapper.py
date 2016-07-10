# Carrega os dados #

import re

machado 	= "CONTENTS"	# Obra completa 
book_regex 	= re.compile("^(\w+)/(\w+).txt: .*")	# Regex das descrições das obras 
title_regex = re.compile("\s+.*")	# Regex do título da obra (sem o caminho do arquivo) 
path_regex	= re.compile("(\w+)/(\w+).txt")	# Regex do caminho da obra 
date_regex 	= re.compile("[0-9]{4}|[0-9]{2}")	# Regex do ano 

# Retorna um dicionário com os campos que compõem as obras
def load():	
	index = 0
	contents = open(machado, encoding="utf-8")	# Carrega os dados 
	data = {}	# Recebe os dados separados por campos

	for line in contents:
		if (re.match(book_regex, line)):
			fields = {}	# Recebe os campos que compõe a descrição da obra 

			title = re.search(title_regex, line)
			if(title):
				titles = [token.strip() for token in re.split("[;]", title.group(0))]
				fields['title'] = titles[0]					# Titulo da obra 
				fields['subtitles'] = ", ".join(titles[1:])	# Subtitulos da obra (titulo dos contos) 
				fields['date'] = findDate(title.group(0))	# Data da obra 

			path = re.search(path_regex, line)
			if(path):
				tokens = re.split("[/]", path.group(0))
				fields['genre'] = tokens[0]					# Gênero da obra 
				fields['path'] = "dataset/" + path.group(0)	# Caminho (no servidor) da obra 
			
			data[index] = fields
			index = index + 1
	return data

# Retorna a data da obra
def findDate(text):
	date = re.findall(date_regex, text)
	try:
		if len(date[1]) < 4:	# Se uma das datas for composta por menos de quatro dígitos 
			aux = date[0][:2]	# Copia os dois primeiros dígitos da data completa 
			date[1] = aux + date[1]	# Adiciona os primeiros dígitos na segunda data 
	except:
		pass 
	return date 