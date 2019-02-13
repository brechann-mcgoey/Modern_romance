from scrape_new import *
import pandas as pd
from bs4 import BeautifulSoup


#make an empty dataframe to later fill up with book information
df = pd.DataFrame()

#list_address will be refered to later and will point to the page on Goodreads where scraping will begin
list_address="http://www.goodreads.com/genres/new_releases/romance"

#while there are still new pages, keep scraping and then moving on the next page
while list_address:

    list_response = requests.get(list_address)

    #if the server successfully answered the http request, print ok message with list_address, then start looking for links to individual books
    if list_response.status_code == 200:
        print("")
        print("ok",list_address)
        soup = BeautifulSoup(list_response.text,"lxml")
        book_links = ["http://www.goodreads.com" + book.find("a")["href"] for book in soup.find_all("div",class_="coverWrapper")]

	#see if there is a link to the next page of new releases
        try:
            list_address = "http://www.goodreads.com"+ soup.find('a',class_='next_page')['href']
        except:
            list_address = ""
    else:
        print("website not found")

    #for each book, follow links to its individual page, use the parse_page function to scrape needed information
    #put all the data together in a pickle to save for future analysis
    for num, link in enumerate(book_links):

        book_results = parse_page(link)
        print(link)

        df=df.append(pd.DataFrame(book_results),ignore_index=True)
        df.to_pickle("modern_romance.pkl")
