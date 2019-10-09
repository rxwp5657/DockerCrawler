import bs4 as bs
import requests as rq
from enum import Enum
import sys

# Base link for dunde

LINK = 'https://www.duden.de'


# Get next link on the list

def get_next_link(page):
    try:
        html = bs.BeautifulSoup(page.text,'html.parser')
        # Find the next link on the list
        next_link = html.find_all('ul',{"class" : "hookup__list"})[1].find('a').get('href')
        return LINK + next_link
    except:
        # Print finish when there isn't a next link to process
        print("UNABLE TO GET NEXT LINK, END OF SEARCH")
        return ''

# Check if word is sustantive 

def is_sustantive(page):
    html = bs.BeautifulSoup(page.text,'html.parser')
    try:
        stv = html.select_one('dd.tuple__val').text
        if "Substantiv" in stv:
            return True
        else:
            return False
    except:
        return False
        print("NONE")

# if has table, get the nominativ plural
def get_table(grammatik):
    try:
        table = grammatik.find_all("td")[1].text
        return table
    except:
        return False


# Get plural either on the table or sentence 

def get_plural(page):
    html = bs.BeautifulSoup(page.text,'html.parser')
    try:
        grammatik = html.find(id="grammatik")
        has_value = get_table(grammatik)
        if(has_value):
            return has_value
        else:
            return grammatik.text
    except:
        return ""
        

# Get the etimology, plural and name 

def process_content(page):

    html = bs.BeautifulSoup(page.text,'html.parser')

    try:
        word = html.select_one('span.lemma__main').text
        log = open("./results/words.txt", "a")
        log.write(word + "\n")

        # if it isn't a sustantive, do nothing
        if not is_sustantive(page):
            return ""

        etymology = html.find(id="herkunft").p.text
        plural = get_plural(page)

        if "englisch" in etymology:
            f = open("./results/english_words.csv", "a")
            f.write('{},"{}","{}"\n'.format(word,plural,etymology))
    except:
        return ""
    
def process_page(url,to):
    page = rq.get(url)
    if page.status_code == 200:
        process_content(page)
        new_link = get_next_link(page)
        if not new_link == '' and not new_link == to:
            process_page(new_link,to)
    else:
        process_page(url,to)

def main():
    try:
        seed = sys.argv[1]
        to   = sys.argv[2]
        process_page(seed,to)
    except:
        print("No seed provided")
    
main()
# Seed
#process_page("https://www.duden.de/rechtschreibung/Aa_Kot")
