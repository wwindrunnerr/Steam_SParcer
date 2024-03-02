import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
import json


async def handle_response(response_json):
    soup = BeautifulSoup(response_json['results_html'], 'lxml')

    game_titles = soup.find_all('span', attrs={'class':'title'})

    print(tuple(map(lambda game_title: game_title.text, 
                    game_titles,)))
    
    titles = tuple(map(lambda game_title: game_title.text,game_titles)),
    with open('titles.json', 'w') as file:
        json.dump(titles, file)



async def call_page(session,url):
    print("starting call_page")
    async with session.get(url, verify_ssl=False) as resp:
        await handle_response(await resp.json())

async def main():
    url = "https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&term=strategy&snr=1_7_7_151_7&supportedlang=english&infinite=1"

    coroutines = []

    async with aiohttp.ClientSession() as session:
        for start in range(0, 101, 50):
            coroutines.append(asyncio.create_task(call_page(session,url.format(start=start))))
        await asyncio.wait(coroutines)

asyncio.run(main())