import aiohttp
import asyncio
from bs4 import BeautifulSoup

links = ['https://habr.com/ru/hubs/programming/articles/',
         'https://habr.com/ru/hubs/python/articles/']

async def send_request(url) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            return await resp.text()


async def parse_category(category_url):
    html_responce = await send_request(category_url)
    soup = BeautifulSoup(html_responce, 'lxml')
    block = soup.find('div', class_='tm-pagination__pages')
    pages_count = block.find_all('a', class_='tm-pagination__page')[-1].text.strip()

    for page in range(0, int(pages_count)):
        page_responce = await send_request(url=f'{category_url}page{page}/')
        page_soup = BeautifulSoup(page_responce, 'lxml')
        articles = page_soup.find_all('div', class_='tm-articles-list')
        for article in articles:
            info_block = article.find("article", class_="tm-articles-list__item")
            find_tag_h2 = info_block.find('h2', class_='tm-title tm-title_h2')
            find_tag_a = find_tag_h2.find('a', class_='tm-title__link')
            title = find_tag_a.find('span').text.strip()
            link = f'https://habr.com{find_tag_a.get("href")}'
            with open('urls_habr.txt', 'a', encoding="utf-8") as file:
                count = 0
                category_name = category_url.split('/')[5]
                result_string = f"{category_name} | {title} | {link}\n"
                file.write(result_string)
                print(result_string, end='')





async def main():
    data = [parse_category(category) for category in links]
    await asyncio.gather(*data)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print('exit')