from scrape_new import *
import pandas as pd
import pickle
from bs4 import BeautifulSoup

#this can be replaced with whatever starting point is desired.
#In case below, the first pages of Best_Book_Boyfriends had already been scraped
list_address="https://www.goodreads.com/list/show/10762.Best_Book_Boyfriends?page=40"

#Initialize page number at the page above (in list address +1)
page_num=41

#use the list of already screabed books to make sure that you are not scraping the same data twice
with open("merged_links.txt", "rb") as fp:   # Unpickling
    link_list= pickle.load(fp)

#You can set the limit for the while loop to whatver you like, or pick the last page
#Sometimes the last few pages of books will have very few reviews
while page_num<81:
    df=pd.DataFrame()
    print(page_num)
    list_response = requests.get(list_address)
   
     #if the server successfully answered the http request, print ok message with list_address, then start looking for links to individual books 
    if list_response.status_code == 200:
        print("")
        print("ok",list_address)
        soup = BeautifulSoup(list_response.text,"lxml")
        book_links = ["http://www.goodreads.com" + book["href"] for book in soup.find_all("a",class_="bookTitle")]
        #see if there is a link to the next page 
        try:
            list_address = "https://www.goodreads.com/list/show/10762.Best_Book_Boyfriends?page="+ str(page_num)
        except:
            list_address = ""
    else:
        print("website not found")

    #for each book, follow links to its individaul page, use the parse_page function (from scrape_new.py) to scrape need information
    #put all the data together in a pickle to save for future analysis
    for num, link in enumerate(book_links):
        if link not in link_list:
            book_results = parse_page(link)
            print(link)

            df=df.append(pd.DataFrame(book_results),ignore_index=True)
            df.to_pickle("bf_romance"+str(page_num)+".pkl")
    page_num=page_num+1
