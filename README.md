# Modern Romance

Romance novels are a big business with more than a billion dollars in sales a year.  They account for at third of fiction titles sold in the USA. Romance readers are voracious, with almost half of them reading at least one book a week.The romance industry is also on the forefront of emerging technologies and trends in the literature world including eboks and self-publishing. The volume and speed of production of could allow publishers and authors to quickly capitalize on hot topics and themes.
I have two main objectives, with the ultimate goal of giving authors and publishers predictive tools about how to better design and sell their books. 
My first objective is to investigate trends in themes and topics though time  and the second is to examine the relationships between reader engagement and sales.
Goodreads is a literature focused social media website that allows consumers to rank and review books, find new recommendations and connect with other readers and authors. So far, I have scraped data on more than 10 000books, including more than a million consumer reviews and rankings.

## Scraping data from Goodreads
I used beautiful soup to scrape book information from goodreads (see python script new_releases.py and new_romances.py). This two scripts are very similar but in one case (new_romances.py) start with a Goodreads list, while new_releases.py starts with new releases on goodreads tagged as romance. Both make use of functions imported form scrape_new.py. See scripts for more details.

## Exploring and plotting the data
For natural language processing and accompanying exploratory regression analyses see nltk_clean.ipynb in the notebook folder. To colour code the relationship between book description words and past reader [engagment/ratings] see Color words based on score.ipynb. To predict the success of a book, see Predict average rating and engagment from description.ipynb. 
Initial descriptive and regression  plots were made using bokeh and altair. See scripts (bokeh)  and notebook (altair)  in plots folder for more details. 



