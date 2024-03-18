import os
import asyncio
import requests
from bs4 import BeautifulSoup
import sqlite3


def create_db():
    current_directory = os.getcwd()

    
    db_path = os.path.join(current_directory, 'newsdata.db')

    
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                      id INTEGER PRIMARY KEY,
                      title TEXT,
                      content TEXT,
                      category TEXT,
                      image TEXT,
                      date_published DATE)''')
    
    # Commit the changes and return the database connection and cursor
    db.commit()  
    return db, cursor

async def fetch_content(url):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    return response.text

async def sport(db, cursor):
    n = int(input("Enter the number of the last page, i.e scroll down and check\nNB: Add 1 to whatever number it is, E.g If it's 10 pages, type in 11\n>> "))
    print("<<------OK PROCESSING------>>")
    base_url = 'https://www.channelstv.com/category/sport/'
    for num in range(1, n+1):
        url = f"{base_url}page/{num}"
        content = await fetch_content(url)
        soup = BeautifulSoup(content, 'html.parser')
        for data in soup.find_all('article'):
            """Title"""
            title = data.find('h3', {'class': 'post-title sumry-title'})
            if title is not None:
                title_text = title.text.strip()
                
            """Image"""
            img = data.find('img')
            if img is not None:
                image = img.get('src')
                
            """Link"""
            li = data.find('a')
            if li:
                link = li.get('href')
                # Check if link is valid
                if link and link != '#':
                    # Fetching and parsing individual article
                    article_content = await fetch_content(link)
                    article_soup = BeautifulSoup(article_content, 'html.parser')
                    # Extracting article content
                    article_paragraphs = article_soup.find_all('p')
                    content_text = '\n'.join(paragraph.get_text(strip=True) for paragraph in article_paragraphs)
                    
                    # Insert data into the database
                    cursor.execute("INSERT INTO articles (title, content, category, image, date_published) VALUES (?, ?, ?, ?, ?)",
                                   (title_text, content_text, 'entertainment', image, None))  # Here, date_published is None since it's not provided in the scraping
                    
                    print(f"Scraped and stored: {title_text}")

    # Commit changes and close connection
    db.commit()
    db.close()

async def spt():

    db, cursor = create_db()
    await sport(db, cursor)

# Run the asyncio loop

