from scrape_new import *
import pandas as pd
from bs4 import BeautifulSoup

df = pd.DataFrame()
list_address="http://www.goodreads.com/genres/new_releases/romance"

while list_address:

    list_response = requests.get(list_address)

    if list_response.status_code == 200:
        print("")
        print("ok",list_address)
        soup = BeautifulSoup(list_response.text,"lxml")
        book_links = ["http://www.goodreads.com" + book.find("a")["href"] for book in soup.find_all("div",class_="coverWrapper")]


        try:
            list_address = "http://www.goodreads.com"+ soup.find('a',class_='next_page')['href']
        except:
            list_address = ""
    else:
        print("website not found")

    for num, link in enumerate(book_links):

        book_results = parse_page(link)
        print(link)

        df=df.append(pd.DataFrame(book_results),ignore_index=True)
        df.to_pickle("modern_romance.pkl")
