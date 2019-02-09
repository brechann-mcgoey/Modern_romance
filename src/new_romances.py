from scrape_new import *
import pandas as pd
import pickle
from bs4 import BeautifulSoup


list_address="https://www.goodreads.com/list/show/10762.Best_Book_Boyfriends?page=40"

page_num=41

with open("merged_links.txt", "rb") as fp:   # Unpickling
    link_list= pickle.load(fp)

while page_num<81:
    df=pd.DataFrame()
    print(page_num)
    list_response = requests.get(list_address)

    if list_response.status_code == 200:
        print("")
        print("ok",list_address)
        soup = BeautifulSoup(list_response.text,"lxml")
        book_links = ["http://www.goodreads.com" + book["href"] for book in soup.find_all("a",class_="bookTitle")]

        try:
            list_address = "https://www.goodreads.com/list/show/10762.Best_Book_Boyfriends?page="+ str(page_num)
        except:
            list_address = ""
    else:
        print("website not found")

    for num, link in enumerate(book_links):
        if link not in link_list:
            book_results = parse_page(link)
            print(link)

            df=df.append(pd.DataFrame(book_results),ignore_index=True)
            df.to_pickle("bf_romance"+str(page_num)+".pkl")
    page_num=page_num+1
