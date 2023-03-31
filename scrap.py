import requests
from bs4 import BeautifulSoup

url = "https://www.theverge.com/"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all('div', class_='max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10')

for id, article in articles:
    title_element = article.find("h2", class_="font-polysans text-20 font-bold leading-100 tracking-1 md:text-24 lg:text-20")
    title = title_element.text.strip()
    link = title_element.find("a")["href"]
    
    author_element = article.find("a", class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin")
    author_element2 = article.find("a", class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8")
    if author_element:
        author = author_element.text.strip()
    elif author_element2:
        author = author_element2.text.strip()
    else:
        author = ""
    
    date_element = article.find("span", class_="text-gray-63 dark:text-gray-94")
    date = date_element.text.strip() if date_element else ""
    
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Date: {date}")
    print(f"URL: https://www.theverge.com{link}\n")


