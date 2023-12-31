#!/usr/bin/env python
# coding: utf-8

# # Import

# ## Library

# In[2]:


import pandas as pd
import xlwt
import requests
import lxml.html as html
import time
import warnings
warnings.filterwarnings('ignore')


# ## Dataset

# In[73]:


selection_word = ['great']
selection_word = pd.DataFrame( selection_word, columns=['word'] )
selection_word


# # Scrapy

# ## Functions

# ### Scrapy Promt

# In[92]:


def scrapy_promr( uniqueword ):
    
    url = f'https://www.online-translator.com/contexts/english-spanish/{uniqueword}'
    df = pd.DataFrame(columns=['server','search_word','english_word','english_phrase','spanish_word','spanish_phrase','link'])

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie' : 'ForeignLang=ES; footer-overlay=b1; cookie=3721bdab-5475-7e7f-2ec2-0d2dbf8a3590:8'
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': site
    }
    
    
#     print(uniqueword,url)

    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200 :
            response2 = response.content.decode('utf-8')
            response3 = html.fromstring(response2)   
            for i in range(1,6):
                body_english = response3.xpath(f'//div[@class="allSamples"]/div[{i}]/span[@class="samSource"]//text()')
                word_english = response3.xpath(f'//div[@class="allSamples"]/div[{i}]/span[@class="samSource"]/span//text()')
                word_english = word_english[0].lower()
#                 print(word_english)
                body_english = ''.join(body_english).replace( f'{word_english}',f'[ {word_english} ]')
                body_english = f'[ {word_english} ]  ' + body_english
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


# ### Linguee

# In[93]:


def scrapy_linguee( uniqueword ):

    session = requests.Session()

    url = f'https://www.linguee.com/english-spanish/search?source=auto&query={uniqueword}'

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7",
        "Cookie": "ForeignLang=ES; cookie=3722f56a-5f4c-51f4-847d-90472033cf16:1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Referer": url
    }

    session.headers.update(headers)
    
    df = pd.DataFrame(columns=['server','search_word','english_word','english_phrase','spanish_word','spanish_phrase','link'])
    
#     print(uniqueword,url)

    try:
        response = session.get(url)
        if response.status_code == 200 :

            response2 = response.content.decode('latin-1')
            response3 = html.fromstring(response2) 
            
            for i in range( 20) :  
                #spanish phase                 
                spanish_phrase = response3.xpath( f'//div[@class="exact"]/child::node()[1]//div[@class="translation_lines"]/child::node()[{i}]//div[@class="example_lines"]/child::node()[1]//span[@class="tag_t"]/text()' )
                spanish_word   = response3.xpath( f'//div[@class="exact"]/child::node()[1]//div[@class="translation_lines"]/child::node()[{i}]//span[@class="tag_trans"]//text()' )
                
                english_phrase = response3.xpath( f'//div[@class="exact"]/child::node()[1]//div[@class="translation_lines"]/child::node()[{i}]//div[@class="example_lines"]/child::node()[1]//span[@class="tag_s"]/text()')
                

                if (len(english_phrase) and len(spanish_word))  != 0 :  
#                         english_phrase = f'[{uniqueword}]' + english_phrase[0]

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


# ## Main

# In[94]:


selection_word = ['run']
selection_word = pd.DataFrame( selection_word, columns=['word'] )


if __name__=='__main__':
    
    df_mother = pd.DataFrame(columns=['server','search_word','english_word','english_phrase','spanish_word','spanish_phrase','link'])

    for i in range(1):
        # PROMT.One
        df_aux_promr = scrapy_promr( selection_word['word'][i]  )
        df_mother = pd.concat([df_mother, df_aux_promr],axis=0)
        
#         word reference         
        df_aux_linguee = scrapy_linguee( selection_word['word'][i]  )
        df_mother = pd.concat([df_mother, df_aux_linguee],axis=0)
        
        #Reset index         
        df_mother = df_mother.reset_index(drop=True)

df_mother

