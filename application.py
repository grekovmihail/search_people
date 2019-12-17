import sqlite3
import re
import wptools
import wikipedia
from bs4 import BeautifulSoup

if __name__ == '__main__':
    conn = sqlite3.connect('./wikipedia_spb_smart_people.db')
    cursor = conn.cursor()
    wikipedia.set_lang("ru")
    result = wikipedia.search(
        "\"Учёная степень доктор\" OR \"Учёная степень кандидат\"    incategory:\"Родившиеся в Санкт-Петербурге\" ",
        results=5000)  # limit for bot
    i = 0
    for current_man in result:

        try:

            html_article = wikipedia.page(current_man)
            tree = BeautifulSoup(html_article.html())

            if ("mbox" in str(html_article.html())):
                 problem_with_article = tree.find('td', {'class': 'mbox-text'}).find('div').text + tree.find('div', {
                    'class': 'mbox-textsmall-div hide-when-compact'}).text
            else:
                problem_with_article = ''


            i += 1
            print(current_man + str(i))


            info_from_wiki_current_man = wptools.page(current_man, lang='ru')
            info_from_wiki_current_man.get()
            try:
                img = info_from_wiki_current_man.data['image'][0]['url']
            except:
                img = "No image"
            try:
                graduate = re.sub(r'\([^()]*\)', '',
                                  str(info_from_wiki_current_man.data['wikidata']['учёная степень (P512)']))
            except:
                graduate = 'No data'



            '''
            if ("infobox-image" in str(html_article.html())):
                img = tree.find('td', {'class': 'infobox-image'}).find('a').get("href")
            else:
                img = "No image"


            dict_info_about_man = tree.find_all('table', {'class': 'infobox vcard'}.find('a'))
            graduate = 'No data'
            for key in dict_info_about_man:
                    if ("доктор" in str(key)) or ("кандидат" in str(key)):
                        graduate = key['title']
                        print(graduate)
                        break
            '''


            cursor.execute("INSERT INTO people (name, img, graduation, problem_with_article) VALUES(?, ?, ?, ?)",
                           (re.sub(r'\([^()]*\)', '', current_man), img, graduate, problem_with_article))
        except:
            cursor.execute("INSERT INTO people (name, img, graduation, problem_with_article) VALUES(?, ?, ?, ?)",
                           (re.sub(r'\([^()]*\)', '', current_man), 'fail', 'fail', ''))

    conn.commit()
    conn.close()
