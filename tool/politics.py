import asyncio
import requests
from bs4 import BeautifulSoup

async def fetch_content(url):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    return response.text

async def politics():
    n = int(input("Enter the number of the last page, i.e scroll down and check\nNB: Add 1 to whatever number it is, E.g If it's 10 pages, type in 11\n>> "))
    print("<<------OK PROCESSING------>>")
    base_url = 'https://www.channelstv.com/category/politics/'
    tasks = []
    for num in range(1, n+1):
        url = f"{base_url}page/{num}"
        content = await fetch_content(url)
        soup = BeautifulSoup(content, 'html.parser')
        for data in soup.find_all('article'):
            """Title"""
            title = data.find('h3', {'class': 'post-title sumry-title'})
            if title is not None:
                print(title.text.strip())
                
            """Image"""
            img = data.find('img')
            if img:
                image = img.get('src')
                print(image)

            """Link""" 
            li = data.find('a')
            if li:
                link = li.get('href')
                print(link)
            print("\n")

# asyncio.run(politics())
