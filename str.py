import streamlit as st
from function import *
import pandas as pd


if __name__=='__main__':

	# Insert words
	user_input = st.text_input("Enter the word or words you need a database with examples for ANKI:")

	if len(user_input) != 0:

		# Order word by frecuency
		words = contar_palabras(user_input)

		# Scrapy
		df = scrapy( words['word'].values )
		# df = scrapy()


		st.write("Words sorted by frequency ", words['word'].values )
		st.write("Database with words that you are learning ", df )


		# Agrega un botón de descarga
		st.download_button(
			label='Descargar CSV',
			data=df[['english_phrase','spanish_phrase']].to_csv(index=False, header=False).encode('utf-8'),
			file_name='datos.csv',
			mime='text/csv'
			)