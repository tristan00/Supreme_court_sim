import requests
from bs4 import BeautifulSoup
import nltk
import sqlite3
import time
import traceback

num_of_volumes = 557
base_search_url = 'http://caselaw.findlaw.com/court/us-supreme-court/volume/{0}'

def prep_db():
    with sqlite3.connect('scotus.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS info_table (name text, link text, date text, docket text)')
        conn.commit()

def get_opinion_links():
    with sqlite3.connect('scotus.db') as conn:
        for i in range(1, num_of_volumes):
            s = requests.Session()

            time.sleep(10)
            r = s.get(base_search_url.format(i))
            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                #print(soup)
                table = soup.find('table', {'id':'srpcaselaw'})
                tr_tags = table.find_all('tr')
                for j in tr_tags[2:-1]:
                    columns = j.find_all('td')
                    name = columns[0].text
                    link = columns[0].find('a')['href']
                    date = columns[1].text
                    docket = columns[2].text
                    print(name, link, date, docket)
                    try:
                        conn.execute('insert into info_table values (?, ?, ?, ?)', (name, link, date, docket,))
                    except:
                        pass
                conn.commit()
            except:
                traceback.print_exc()
                time.sleep(10)

def read_cases(row):
    pass

def main():
    get_opinion_links()

if __name__ == '__main__':
    main()
