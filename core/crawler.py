import asyncio
import re
from collections import namedtuple

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import Comment

TotalOccurrences = namedtuple('TotalOccurrences', ['url', 'word', 'total_occurrences'])


def normalize_url(url):
    return 'http://'+url if url.startswith('www') else url


async def fetch_url(session, url):
    async with session.get(normalize_url(url), timeout=60 * 60) as response:
        return await response.text()


async def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]'] or isinstance(element,
                                                                                                       Comment):
        return False
    return True


async def text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


async def count_word(word, text):
    return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word.lower()), text.lower()))


async def extract_url_count(url, word, session):
    html = await fetch_url(session, url)
    text = await text_from_html(html)
    qtn_palavras = await count_word(word, text)
    return TotalOccurrences(url, word, qtn_palavras)


async def count_url(urls, word, session):
    results = await asyncio.gather(*[extract_url_count(url, word, session) for url in urls], return_exceptions=True)
    return results


def execute(urls, word):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    connector = aiohttp.TCPConnector(limit=100)
    with aiohttp.ClientSession(loop=loop, connector=connector) as session:
        resp = loop.run_until_complete(count_url(urls, word, session))
    loop.close()
    return resp
