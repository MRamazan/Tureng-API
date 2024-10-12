from bs4 import BeautifulSoup
import requests

languages = {"EN-TR":"turkce-ingilizce",
             "EN-DE":"almanca-ingilizce",
             "EN-ES":"ispanyolca-ingilizce",
             "EN-FR":"fransizca-ingilizce"}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}


class Tureng(object):
    def __init__(self, word, language_,closestWordCount=1):
        self.word = word
        self.MeaningList = None
        self.WordTypeList = None
        self.CategoryLisy = None
        self.closestWordCount = closestWordCount


        if language_ in languages:
            self.tureng_url = "https://tureng.com/tr/{}".format(languages[language_]) + "/" + self.word
        else:
            raise TypeError("The language parameter is not in the language list; make sure you haven't entered it incorrectly.")





    def request_html(self):
        return requests.get(self.tureng_url, headers=headers)




    def TranslateResults(self, counter=0):
        meaning = self.MeaningList[:self.closestWordCount]
        type = self.WordTypeList[:self.closestWordCount]
        translated = self.CategoryLisy[:self.closestWordCount]

        return meaning, type, translated




    def translate_en_to_other(self):
        response = self.request_html()
        if response.status_code == 200:
            word_url = BeautifulSoup(response.text, 'html.parser')
            table_word = word_url.find('table', id='englishResultsTable')
            if table_word:

                wordTypes = table_word.find_all('td', class_='en tm')
                meanings = table_word.find_all('td', class_='tr ts')
                usages = table_word.find_all('td', class_='hidden-xs')



                wordTypeList = [td.get_text(strip=True)[-2] for td in wordTypes]
                meaning_list = [td.get_text(strip=True) for td in meanings]
                category_list = [td.get_text(strip=True) for td in usages]

                self.WordTypeList = wordTypeList
                self.MeaningList  = meaning_list
                cleaned_usage_list = []
                for i in range(1, len(category_list), 3):
                    cleaned_usage_list.append(category_list[i])
                self.CategoryLisy = cleaned_usage_list





    def translate_other_to_en(self):
        try:
            kelime_url_r = BeautifulSoup(self.request_html(), 'html.parser')
            table_kelime_r = kelime_url_r.find_all('table', id='englishResultsTable')
            self.anlam = table_kelime_r[0].find_all('td', class_='en tm')
            self.kategori = table_kelime_r[0].find_all('td', class_='hidden-xs')

        except IndexError:
            print("Kelime bulunamadı.")







#selected_language = input(" EN-TR \n EN-DE \n EN-ES \n EN-FR \n\n Choose one of the language pairs above: ")
#word = input("Enter word to translate: ")
#sinif = Tureng(word,selected_language,3)
#sinif.translate_en_to_other()
#meanings, word_types, category = sinif.TranslateResults()
