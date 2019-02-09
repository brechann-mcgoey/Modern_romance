from bs4 import BeautifulSoup
import pandas as pd
import requests
import codecs

def review_parse(review):
    review_id=review['id']
    reviewer_name=review.find('a',class_='user').get_text()
    review_date=review.find('a',class_='reviewDate').get_text()
    score_dict={"it was amazing":5,"really liked it":4,"liked it":3,"it was ok":2,"did not like it":1}
    reviewer_rating=review.find('span',class_='staticStar',text=True).get_text()
    reviewer_score=score_dict[reviewer_rating]
    review_boxes=review.findAll('span', class_='readable')[0].findAll('span')
    review_text=[review_box.get_text() for review_box in review_boxes[min(1,len(review_boxes)-1):]]

    return ([review_id],[reviewer_name],[review_date],[reviewer_rating],[reviewer_score],[review_text])

def reviews_find(soupy,book_address):

    review_ids=[]
    reviewer_names=[]
    review_dates=[]
    reviewer_ratings=[]
    reviewer_scores=[]
    review_texts=[]

    book_address=book_address+"?sort=newest&text_only=true"
    while book_address:

        response = requests.get(book_address)

        if response.status_code == 200:
            #print("")
            #print("ok",book_address)
            soup = BeautifulSoup(codecs.getdecoder("unicode_escape")(response.text)[0],"lxml")

            for review in soup.findAll('div', class_="review"):
                if "rated it" in review.get_text():
                    result=review_parse(review)
                    review_ids=review_ids+result[0]
                    reviewer_names=reviewer_names+result[1]
                    review_dates=review_dates+result[2]
                    reviewer_ratings=reviewer_ratings+result[3]
                    reviewer_scores=reviewer_scores+result[4]
                    review_texts=review_texts+result[5]


            try:
                if book_address == "http://www.goodreads.com"+ soup.findAll('a',
                                class_="next_page")[0]['onclick'].split("'")[1]:
                    book_address = ""
                else:
                    book_address = "http://www.goodreads.com"+ soup.findAll('a',
                                class_="next_page")[0]['onclick'].split("'")[1]

            except:
                book_address = ""
        else:
            print("reviews not found")

    return [review_ids],[reviewer_names],[review_dates], [reviewer_ratings],[reviewer_scores],[review_texts]

def isbn_find (soupy):
    if soupy.findAll('div',class_="infoBoxRowTitle")[0].get_text()=='ISBN':
        isbn = soupy.findAll('div',class_="infoBoxRowItem")[0].get_text().split("\n")[1].strip()
    elif soupy.findAll('div',class_="infoBoxRowTitle")[1].get_text()=='ISBN':
        isbn = soupy.findAll('div',class_="infoBoxRowItem")[1].get_text().split("\n")[1].strip()
    else: isbn = 'NA'
    return isbn



def parse_page (link):
    """
    website_response in unicode text -> dictionary of attributes

    """
    webpage = requests.get(link)
    book = {}

    soup = BeautifulSoup(webpage.text, "lxml")

    try:
        book["title"] = [soup.find('h1',class_='bookTitle').get_text().strip()]
    except:
        book["title"] =[""]

    try:
        book["authors"] = [[author.get_text().strip()
                       for author in soup.findAll('a',class_="authorName")]]
    except:
        book["authors"] = [""]

    try:
        book["buy_link"]=[soup.findAll('a',class_='buttonBar')[1]['href']]

    except:
        book["buy_link"]=[""]

    try:
        book["rating"] = [soup.find('span',class_="value rating").get_text().strip()]
    except:
        book["rating"] = [""]

    try:
        book["isbn"] = [isbn_find(soup)]
    except:
        book["isbn"] = [""]

    try:
        book["date"] = [soup.findAll('div',class_="row")[1].get_text().split("\n")[2].strip()]
    except:
        book["date"] = [""]

    try:
        book["description"] = [soup.find('div',class_="readable stacked").findAll('span')[-1].get_text()]
    except:
        book["description"] = [""]

    try:
        book["awards"] = [[award.get_text() for award in soup.findAll('a',class_="award")]]
    except:
        book["awards"] = [""]

    try:
        result=reviews_find(soup,link)
        book["review_ids"]=result[0]
        book["reviewer_names"]=result[1]
        book["review_dates"]=result[2]
        book["reviewer_ratings"]=result[3]
        book["reviewer_scores"]=result[4]
        book["review_texts"]=result[5]
    except:
        book["review_ids"]=[""]
        book["reviewer_names"]=[""]
        book["review_dates"]=[""]
        book["reviewer_ratings"]=[""]
        book["reviewer_scores"]=[""]
        book["review_texts"]=[""]

    book["link"] = link
    book["page"] = webpage.text

    return book
