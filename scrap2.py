import requests
from bs4 import BeautifulSoup
import csv
import datetime
import sqlite3

# Create a file name based on current date
file_name = datetime.datetime.now().strftime("%d%m%Y") + "_verge.csv"

# Create CSV file and write header
with open(file_name, mode='w') as csv_file:
    fieldnames = ['id', 'URL', 'headline', 'author', 'date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Scrape articles from The Verge homepage
    url = "https://www.theverge.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all('article')

    # Write article data to CSV file and SQLite database
    conn = sqlite3.connect('verge_articles.db')
    for idx, article in enumerate(articles):
        a_tag = article.find("h2", class_="font-polysans text-20 font-bold leading-100 tracking-1 md:text-24 lg:text-20")
        if a_tag is not None:
            headline = a_tag.text.strip()
            url = a_tag.find("a")['href']
        else:
            headline = "Eror"
            url = "Error"
        author_tag = article.find("a", class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin")
        author_tag2 = article.find("a", class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8")
        if author_tag is not None:
            author = author_tag.text.strip()
        elif author_tag2 is not None:
            author = author_tag2.text.strip()
        else:
            author = "Error"
        date_tag = article.find("span", class_="text-gray-63 dark:text-gray-94")
        if date_tag is not None:
            date = date_tag['datetime']
        else:
            date = "Error"

        writer.writerow({'id': idx+1, 'URL': url, 'headline': headline, 'author': author, 'date': date})
        conn.execute('''INSERT OR IGNORE INTO articles
                     (id, URL, headline, author, date)
                     VALUES (?, ?, ?, ?, ?)''',
                     (idx+1, url, headline, author, date))
        
        

    # Save changes and close connection
    conn.commit()
    conn.close()