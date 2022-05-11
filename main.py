import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas import DataFrame
import requests
from time import sleep
from data import data
import os
from scraper_vak import Scraper
from random import randint
from typing import List
from scraper_conf import Conf_Scraper

def get_session(data):
    s = requests.Session()
    s.post(data.login_url, data=data.auth, headers=data.headers)
    sleep(randint(7,25))
    return s

def get_page(s, data, url):
    r = s.get(url, headers=data.headers)
    sleep(randint(7,25))
    soup = BeautifulSoup(r.content, 'lxml')
    main_table = soup.find('div', {'style' : 'width:580px; margin:0; border:0; padding:0; '})
    return main_table


def get_author_pub(author_id, data, s, name, pagenum):
    post = {
        'authorid' : author_id,
        'pagenum' : str(pagenum),
        'show_refs' : '0',
        'hide_doubles' : '1',
        'did' : '1',
        'urlnum' : '1',
        'rubric_order': '0',
        'title_order' : '0',
        'org_order' : '0',
        'author_order' : '0',
        'year_order' : '1',
        'years_2021' : 'on',
        'years_2020' : 'on',
        'years_2019' : 'on',
        'years_2018' : 'on',
        'years_2017' : 'on',
        'type_order' : '0',
        'role_order' : '0',
        'keyword_order' : '0',
        'show_option' : '5',
        'show_hash' : '0',
        'check_hide_doubles' : 'on',
        'sortorder' : '0',
        'order' : '1',}
    soup = BeautifulSoup(s.post('https://www.elibrary.ru/author_items.asp', data = post, headers = data.headers).content, 'lxml')
    with open(f'./vak/{name}{pagenum}.txt','w', encoding='utf-8') as infile:
        infile.write(str(soup))
        
def get_authors_pub(data, s):        
    sleep(5)
    with open('author_.txt', 'r', encoding='utf-8') as f:
            for line in f:
                name=line.split(':')[0]
                author_id=line.split(':')[1]
                #if name == 'Юша Владимир Леонидович1':
                #    get_author_pub(author_id, data, s, name, 3)
                #    get_author_pub(author_id, data, s, name, 4)
                #    sleep(14)
                with open(f"./vak/{name}3.txt", "r", encoding="utf-8") as f:
                    text = f.read()
                    df1 = Scraper(text).start()
                #    with open(f"./vak/{name}4.txt", "r", encoding="utf-8") as f1:
                #          text1 = f1.read()
                #          df = Scraper(text1).start()
                pd.concat([df1], axis=0).to_excel(f"./vak_xlsx/{name}.xlsx")

def update_pubs():
    files = os.listdir('./vak_xlsx')
    for file in files:
        if file.endswith(".xlsx"):
            db = pd.read_excel(f'./vak_xlsx/{file}')
            db = db.drop('Unnamed: 0',axis=1)
            tomes, names, biblio = [], [], []
            for i, row in db.iterrows():
                tome = ''
                for i in range(len(row['Том'])):
                    if row['Том'][i] == '.' and (row['Том'][i-1].isnumeric() or row['Том'][i-1] == ')') and i != len(row['Том'])-1:
                        tome += '. –'
                    else:
                        tome += row['Том'][i]
                tome = tome.replace('  ', ' ')
                b = row['Название'].capitalize() + ' / ' + row['Авторы'] + ' // ' + row['Журнал'] + '. –' + tome
                biblio.append(b)
                tomes.append(tome)
                names.append(row['Название'].capitalize())
            db['Полное библиографическое описание'] = biblio
            db['Название'] = names
            db['Том'] = tomes
            db.to_excel(f"./vak_xlsx/{file}")

def get_author_conf(author_id, data, s, name, pagenum):
    post = {
        'authorid' : author_id,
        'pagenum' : str(pagenum),
        'show_refs' : '0',
        'hide_doubles' : '1',
        'did' : '1',
        'urlnum' : '1',
        'rubric_order': '0',
        'title_order' : '0',
        'org_order' : '0',
        'author_order' : '0',
        'year_order' : '1',
        'years_2021' : 'on',
        'years_2020' : 'on',
        'years_2019' : 'on',
        'years_2018' : 'on',
        'years_2017' : 'on',
        'type_order' : '0',
        'types_6' : 'on',        
        'role_order' : '0',
        'keyword_order' : '0',
        'show_option' : '0',        
        'show_hash' : '0',
        'check_hide_doubles' : 'on',
        'sortorder' : '0',
        'order' : '1',
        'itemboxid' : '0'}
    soup = BeautifulSoup(s.post('https://www.elibrary.ru/author_items.asp', data = post, headers = data.headers).content, 'lxml')
    with open(f'./conf/{name}{pagenum}.txt','w', encoding='utf-8') as infile:
        infile.write(str(soup))


def get_authors_conf(d, s):
    sleep(5)
    with open('author_.txt', 'r', encoding='utf-8') as f:
        for line in f:
            name=line.split(':')[0]
            author_id=line.split(':')[1]
            #get_author_conf(author_id, data, s, name, 4)
           # sleep(12)
            #get_author_conf(author_id, data, s, name, 5)
            #sleep(14)
            #get_author_conf(author_id, data, s, name, 3)
            #sleep(13)          
            with open(f"./conf/{name}4.txt", "r", encoding="utf-8") as f:
                text = f.read()
                df1 = Conf_Scraper(text).start()
            #    with open(f"./conf/{name}5.txt", "r", encoding="utf-8") as f1:
            #          text1 = f1.read()
            #            df = Conf_Scraper(text1).start()
            #         with open(f"./conf/{name}3.txt", "r", encoding="utf-8") as f2:
            #             text2 = f2.read()
            #             df2 = Conf_Scraper(text2).start()
            pd.concat([df1], axis=0).to_excel(f"./conf_xlsx/{name}_conf.xlsx")

def update_conf(d, s):
    files = os.listdir('./conf_xlsx')
    for file in files:
        if file.endswith(".xlsx"):
            db = pd.read_excel(f'./conf_xlsx/{file}')
            db = db.drop('Unnamed: 0',axis=1)
            db = db.drop('Том',axis=1)
            db = db.drop('Журнал',axis=1)
            theme, names, years, biblio= [], [], [], []
            for i, row in db.iterrows():
                r = s.get(row['Ссылка'], headers=d.headers)
                soup = BeautifulSoup(r.content, 'lxml')
                try:
                    conf_data = soup.find(text='КОНФЕРЕНЦИЯ:').parent.parent.parent.parent.find_all('tr')[1].find_all('font')
                    conf = conf_data[0].text + '\n' + conf_data[1].text
                    year = conf[-9:-5]
                except:
                    conf = '-'
                    year = '-'
                sleep(randint(7,25))
                b = row['Название'].capitalize() + ' / ' + row['Авторы'] + ' // ' + row['Год'].replace('В сборнике: ', '')
                biblio.append(b)
                theme.append(row['Название'].capitalize())
                names.append(conf)
                years.append(year)
            db['Полное библиографическое описание'] = biblio
            db['Наименование конференции'] = names
            db['Год'] = years
            db['Тема'] = theme
            db.to_excel(f"./conf_xlsx/{file}")
def get_core():
    df = pd.read_excel('Publications.xlsx')     
    df = df.loc[df['Year'] != 2016]
    dictionary = pd.read_excel('dictionary.xlsx')
    wos_df = pd.read_excel('wos 2017-2021.xlsx')
    print(df)
    with open('author_.txt', 'r', encoding='utf-8') as f:
        for line in f:
            name=line.split(':')[0]
            scopus_id=line.split(':')[2].replace('\n', '')
            print(name, scopus_id)
            years = []
            authors_original = []
            authors_eng = []
            name_orig = []
            name_eng = []
            izd = []
            out_data = []
            doi = []
            impact = []
            biblio  = []
            db1 = []
            db2 = []
            for idx,row in df.iterrows():
                if scopus_id in str(row['Scopus Author Ids']):
                    years.append(row['Year'])
                    authors_original.append(row['Authors'].replace('|', ','))
                    authors_eng.append(row['Authors'].replace('|', ','))
                    name_orig.append(row['Title'])
                    name_eng.append(row['Title'])
                    izd.append(row['Scopus Source title'])
                    issue = ''
                    db1.append('Scopus')
                    if ((row['DOI'] in wos_df['DOI'].unique()) or
                    (row['Title'].lower() in wos_df['Article Title'].str.lower().unique())):
                        db2.append('WoS')
                    else:
                        db2.append('-')
                    if row['Issue'] != '-':
                        issue = f'– №{row["Issue"]}. '
                    volume = ''
                    if row['Volume'] != '-':
                        volume = f'– Т.{row["Volume"]}. '
                    pages = ''
                    if row['Pages'] != '-':
                        pages = f'– С. {row["Pages"]}'
                    out_d = str(row['Year']) + '. ' + volume + issue + pages
                    out_data.append(out_d)
                    doi.append(row['DOI'])
                    impact.append(row['CiteScore (publication year)'])
                    biblio.append(row['Title'] + ' / ' + row['Authors'].replace('|', ',') + ' // ' + row['Scopus Source title'] + '.– ' + out_d)
            names = dictionary.loc[dictionary['Сотрудник'] == name]
            try:
                names = names['names'].values[0][:-1].split(';')
                print(names)
                for index, value in enumerate(wos_df['Authors'].str.lower().values):
                    for n in names:
                        if n in value:
                            wos_string = wos_df.iloc[index]
                            if wos_string['DOI'] not in doi and wos_string['Article Title'].lower() not in [t.lower() for t in name_orig]:
                                years.append(wos_string['Publication Year'])
                                authors_original.append(wos_string['Authors'])
                                authors_eng.append(wos_string['Authors'])
                                name_orig.append(wos_string['Article Title'])
                                name_eng.append(wos_string['Article Title'])
                                izd.append(wos_string['Source Title'])
                                issue = ''
                                if wos_string['Issue'] != '':
                                    issue = f'– №{row["Issue"]}. '
                                volume = ''
                                if wos_string['Volume'] != '':
                                    volume = f'– Т.{row["Volume"]}. '
                                pages = ''
                                if wos_string['Start Page'] != '' and wos_string['End Page'] != '':
                                    pages = f'– С. {wos_string["Start Page"]}–{wos_string["End Page"]}'
                                out_d = str(int(wos_string['Publication Year'])) + '. ' + volume + issue + pages
                                out_data.append(out_d)
                                doi.append(wos_string['DOI'])
                                impact.append('-')
                                db1.append('-')
                                db2.append('WoS')
                                biblio.append(wos_string['Article Title'] + ' / ' + wos_string['Authors'].replace('|', ',') + ' // ' + wos_string['Source Title'] + '.– ' + out_d)
                                print(wos_string['Article Title'])
                            break
            except:
                print('-')           
            author_df = pd.DataFrame()
            author_df['Год'] = years
            author_df['Авторы на языке оригинала'] = authors_original
            author_df['Авторы на английском языке'] = authors_eng
            author_df['Название статьи на оригинальном языке'] = name_orig
            author_df['Название статьи на английском языке'] = name_eng
            author_df['Наименование издания'] = izd
            author_df['Выходные данные'] = out_data
            author_df['DOI'] = doi
            author_df['Импакт-фактор'] = impact
            author_df['Библиографическое описание'] = biblio
            author_df['Библиографическая БД1'] = db1
            author_df['Библиографическaя БД2'] = db2
            author_df.to_excel(f'./core_xlsx/{name}.xlsx', sheet_name='Международные базы')

def merge():
    with open('author_.txt', 'r', encoding='utf-8') as f:
        for line in f:
            name=line.split(':')[0]
            df_vak = pd.read_excel(f'./vak_xlsx/{name}.xlsx')
            df_vak = df_vak.drop('Unnamed: 0',axis=1)
            df_conf = pd.read_excel(f'./conf_xlsx/{name}_conf.xlsx')
            df_conf = df_conf.drop('Unnamed: 0',axis=1)
            df_conf = df_conf.drop('Название', axis=1)
            df_conf = df_conf.reindex(columns = ['Год', 'Тема', 'Наименование конференции', 'Полное библиографическое описание', 'Авторы', 'Ссылка'])
            df_core = pd.read_excel(f'./core_xlsx/{name}.xlsx')
            df_core = df_core.drop('Unnamed: 0',axis=1)
            df_vak.index += 1
            df_conf.index += 1
            df_core.index += 1
            writer = pd.ExcelWriter(f'./final/{name}.xlsx')
            df_core.to_excel(writer, 'Статьи международных изданий')
            df_vak.to_excel(writer, 'Статьи рецензируемых изданий')
            df_conf.to_excel(writer, 'Доклады')
            writer.save()

data = data()
s = get_session(data)
get_authors_pub(data, s)
update_pubs()
#get_authors_conf(data, s)
#update_conf(data, s)
#get_core()
#merge()
