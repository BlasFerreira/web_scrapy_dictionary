import pandas as pd
import xlwt
import requests
import lxml.html as html
import warnings
warnings.filterwarnings('ignore')


def contar_palabras(texto):

	text_cleaned = clear_data(texto)
	palabras = text_cleaned.split()  # separar el texto en una lista de palabras

	frecuencia = {}
	for palabra in palabras:
		if palabra in frecuencia:
		    frecuencia[palabra] += 1  # incrementar la frecuencia de una palabra ya vista
		else:
		    frecuencia[palabra] = 1  # registrar la aparición de una nueva palabra
	    
	# ordenar el diccionario por valores en orden descendente
	frecuencia_ordenada = {k: v for k, v in sorted(frecuencia.items(), key=lambda item: item[1], reverse=True)}

	list_tuples = [(i, n) for i, n in frecuencia_ordenada.items()]
	df = pd.DataFrame(list_tuples, columns=['word', 'frecuency'])
	return df

    
def clear_data(texto_dirty): 

	texto = texto_dirty
	texto = texto.replace('(',' ')
	texto = texto.replace(')',' ')
	texto = texto.replace('.',' ')
	texto = texto.replace('1',' ')
	texto = texto.replace('2',' ')
	texto = texto.replace('3',' ')
	texto = texto.replace('4',' ')
	texto = texto.replace('5',' ')
	texto = texto.replace('6',' ')
	texto = texto.replace('7',' ')
	texto = texto.replace('8',' ')
	texto = texto.replace('9',' ')
	texto = texto.replace('0',' ')
	texto = texto.replace('\n',' ')
	texto = texto.replace(',',' ')
	texto = texto.replace('[',' ')
	texto = texto.replace(']','')
	texto = texto.replace('—',' ')
	texto = texto.replace('–',' ')
	texto = texto.replace('-',' ')	
	texto = texto.replace('"',' ')
	texto = texto.replace(';',' ')
	texto = texto.replace(':',' ')
	texto = texto.replace('/',' ')
	texto = texto.lower()
	
	return texto


def scrapy_promr( uniqueword ):

	url = f'https://www.online-translator.com/contexts/english-spanish/{uniqueword}'
	df = pd.DataFrame(columns=['server','search_word','english_word','english_phrase','spanish_word','spanish_phrase','link'])

	print(url)
	try:

		response = requests.get(url)
		print(response.status_code)

		if response.status_code == 200 :
			response2 = response.content.decode('utf-8')
			response3 = html.fromstring(response2)   

			for i in range(1,6):
			
					body_english = response3.xpath(f'//div[@class="allSamples"]/div[{i}]/span[@class="samSource"]//text()')
					word_english = response3.xpath(f'//div[@class="allSamples"]/div[{i}]/span[@class="samSource"]/span//text()')
					print(body_english)
					print(word_english)

					if len(word_english) != 0 :
						word_english = word_english[0].lower()
						body_english = ''.join(body_english).replace( f'{word_english}',f'[{word_english}]')
						body_english = f'[{word_english}]  ' + body_english
						body_english = body_english.lower()
						body_spanish = response3.xpath(f'//div[@class="allSamples"]/div[{i}]/span[@class="samTranslation"]//text()')
						body_spanish = ''.join(body_spanish)
						body_spanish = body_spanish.lower()
						word_spanish = response3.xpath(f'//div[@class="allSamples"]/div[{i}]/span[@class="samTranslation"]/a//text()')
						word_spanish = ''.join(word_spanish).lower()
						body_spanish = body_spanish.lower().replace( f'{word_spanish}',f'[{word_spanish}]')

						df = df.append({'server' : 'Promt',
						'search_word' : uniqueword,
						'english_word': word_english,
						'english_phrase':body_english,
						'spanish_word':word_spanish ,
						'spanish_phrase':f'[ {word_spanish} ]  ' + body_spanish,
						'link':url},
						ignore_index=True)




		else:
			raise ValueError(f'Error : {response.status_code}')
			print('NO GOOD')

	except ValueError as ve:
		print(ve)
	
	return df 



def scrapy_linguee( uniqueword ):

	url = f'https://www.linguee.com/english-spanish/search?source=auto&query={uniqueword}'
	df = pd.DataFrame(columns=['server','search_word','english_word','english_phrase','spanish_word','spanish_phrase','link'])


	try:
		response = requests.get(url)
		if response.status_code == 200 :

			response2 = response.content.decode('latin-1')
			response3 = html.fromstring(response2) 

			for i in range( 20) :  

				#spanish phase                 
				spanish_phrase = response3.xpath( f'//div[@class="exact"]/child::node()[1]//div[@class="translation_lines"]/child::node()[{i}]//div[@class="example_lines"]/child::node()[1]//span[@class="tag_t"]/text()' )
				spanish_word   = response3.xpath( f'//div[@class="exact"]/child::node()[1]//div[@class="translation_lines"]/child::node()[{i}]//span[@class="tag_trans"]//text()' )

				english_phrase = response3.xpath( f'//div[@class="exact"]/child::node()[1]//div[@class="translation_lines"]/child::node()[{i}]//div[@class="example_lines"]/child::node()[1]//span[@class="tag_s"]/text()')

				if (len(english_phrase) and len(spanish_word))  != 0 :  

					df = df.append({'server' : 'linguee',
					'search_word':uniqueword,
					'english_word':uniqueword,
					'english_phrase':f'[ {uniqueword} ]  ' + english_phrase[0].replace( f'{uniqueword}',f'[ {uniqueword} ]').lower(),
					'spanish_word' : spanish_word[0] ,
					'spanish_phrase': f'[ {spanish_word[0]} ]  ' + spanish_phrase[0].replace( f'{spanish_word[0]}',f'[ {spanish_word[0]} ]').lower(),                    
					'link':url }, ignore_index=True)


		else:
			raise ValueError(f'Error : {response.status_code}')
			print('NO GOOD')

	except ValueError as ve:
		print(ve)

	return df 


def scrapy( list_words ) :

	selection_word = list_words
	selection_word = pd.DataFrame( selection_word, columns=['word'] )

	df_mother = pd.DataFrame(columns=['server','search_word','english_word','english_phrase','spanish_word','spanish_phrase','link'])

	for i in range( len(selection_word)):
		# PROMT.One
		df_aux_promr = scrapy_promr( selection_word['word'][i]  )
		df_mother = pd.concat([df_mother, df_aux_promr],axis=0)

		#         word reference         
		df_aux_linguee = scrapy_linguee( selection_word['word'][i]  )
		df_mother = pd.concat([df_mother, df_aux_linguee],axis=0)

		#Reset index         
		df_mother = df_mother.reset_index(drop=True)

	return df_mother
