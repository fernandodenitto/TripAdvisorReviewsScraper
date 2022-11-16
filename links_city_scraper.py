import requests
import json
from bs4 import BeautifulSoup 
import math,time # compute number of pages and reviews
import random # as above
from utils import getCookiesFromDomain
import pandas as pd
import re


BASE_URL = input("Paste the link of the city you want to (bulk) scrape:\t")
#BASE_URL="https://www.tripadvisor.com/Hotels-g187895-Florence_Tuscany-Hotels.html"

outputfile = input("Write the name of the file you want to save all the link about the city to scrape:\t")

#Set an headers to avoid blocking from Tripadvisor
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


response = requests.get(BASE_URL,headers=headers).text
soup = BeautifulSoup(response,features="lxml")

#Getting the number of properties per page
properties_link = soup.find_all("a", {"data-clicksource": "HotelName"}) 
PROPERTIES_PER_PAGE = len(properties_link) 
print(f"There are {len(properties_link)} properties per page!")

#We will use 30 as default value since the URL change in 30 multiples
PER_PAGE=30

#Getting the total number of properties and compute values for navigate web pages
span = soup.select('.MOBILE_SORT_FILTER_BUTTONS + div span')[0]
N_PROPERTIES = int(re.sub('([^0-9])', '', span.text))
print(f'There are {N_PROPERTIES} properties')
N_PAGES = math.ceil(N_PROPERTIES / PER_PAGE)
print(f'There are {N_PAGES} different pages')


# for div in mydivs:
#     print(div['href'])


def get_id_from_url(url):
  # Split URL by -g to divide it before the ID
  prefix, suffix = url.split('-g', maxsplit=1)
  # Divide the URL after the ID (first dash)
  id, slug = suffix.split('-', maxsplit=1)
  return int(id)

def get_listing_url(page, base_url=BASE_URL, per_page=PER_PAGE):
  assert page >= 0
  id = get_id_from_url(base_url)
  if page == 0:
    return BASE_URL

  return BASE_URL.replace(f'-g{id}-', f'-g{id}-oa{page * per_page}-')


#Ask how many pages of spots the user want to download
SPOT_PAGES=int(input(f"How many pages of spots do you want to scrape? (each page contains {PER_PAGE} spots)\t"))
N_PAGES=min(N_PAGES,SPOT_PAGES)

listings = []
for i in range(N_PAGES):
    url = get_listing_url(i)
    print(url)
    print(f'Collecting the first {(i+1)*PER_PAGE} Hotels... (Page {i+1} of {N_PAGES})')
    # Random delay to avoid TripAdvisor blocking us
    time.sleep(random.randint(2, 8))

    # Download current page

    response = requests.get(url,headers=headers).text
    soup = BeautifulSoup(response,features="lxml")

    # Add hotels to listings
    raw_listings = soup.find_all("a", {"data-clicksource": "HotelName"}) 
    
    for raw_listing in raw_listings:
        listings.append('https://www.tripadvisor.com' + raw_listing['href'])
        print('https://www.tripadvisor.com' + raw_listing['href'])
            

listings=list(set(listings)) #Delete duplicates since TripAdvisor Pages often have the same "sponsored" spots

with open(outputfile, "a+") as file_object:
  for listing in listings:
    file_object.write(listing+'\n')
file_object.close()

print(f"Collected {len(listings)} Hotels from {BASE_URL}! (Appended to the file hotel_links.txt)")