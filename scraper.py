import requests
from bs4 import BeautifulSoup
import csv

import time
url = "https://lurer.com"

response = requests.get(url)

links = []

# Check response
if response.status_code == 200:

    soup = BeautifulSoup(response.content, "html.parser")

    div_element = soup.find("div", class_="dropDown")

    anchor_tags = div_element.find_all("a")

    for anchor in anchor_tags:
        link = anchor.get("href")

        if not link.startswith("http"):
            link = url + link
        links.append(link)

    # for link in links:
        # print(link)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

# print("-" * 30)
# print("-" * 30)

website_links = {}

for link in links:
    response = requests.get(link)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, "html.parser")

        div_el = soup.find("div", class_="categoryShow")
        category = div_el.find("h1").text

        # print(category)

        div_element = soup.find("div", class_="catBox clearfix")

        # website_links = {}

        anchor_tags = div_element.find_all("a")

        for anchor in anchor_tags:
            website_link = anchor.get("href")

            if not website_link.startswith("http"):
                website_link = url + website_link
            website_links.setdefault(category, []).append(website_link)

            # website_links[category].append(website_link) #append

        # print(website_links)
        # Print the extracted URLs

        # print("-" * 30)

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

# print(website_links)

corpus_dict = {}

for category in website_links:
    for w_link in website_links[category]:

        response = requests.get(w_link)

        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            div_el = soup.find("div", class_="mainCenterWrapperLeft")
            text_paragraphs = div_el.find_all("p")
            for text_p in text_paragraphs:
                text = text_p.text
                text = text.replace(u'\xa0', u' ')
                corpus_dict.setdefault(category, []).append(text)
    time.sleep(2)

# print(corpus_dict)
# print("-" * 30)
# print(type(corpus_dict))

# total_strings = 0

# for lst in corpus_dict.values():

    # total_strings += len(lst)

# print(f'Total strings in the dictionary: {total_strings}')

csv_file = 'corpus_articles.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Article Text', 'Category'])

    for key, values in corpus_dict.items():

        for value in values:

            writer.writerow([value, key])

print(f'CSV file "{csv_file}" has been created successfully.')
