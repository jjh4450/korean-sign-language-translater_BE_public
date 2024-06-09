import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import quote
from itertools import chain
import re

if __name__ != '__main__':
    import parser.sep as sep
elif __name__ == '__main__':
    import sep as sep

class VideoFinder:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def fetch(self, url):
        """Fetch the content from the URL asynchronously."""
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                response.raise_for_status()
        return None

    async def get_soup_from_url(self, url):
        """Given a URL, return the parsed BeautifulSoup object asynchronously."""
        content = await self.fetch(url)
        if content:
            return BeautifulSoup(content, 'html.parser')
        return None

    def extract_video_info(self, soup):
        """Extract video information from the BeautifulSoup object."""
        video_list = []

        images = chain.from_iterable(
            div.find_all('li') for div in soup.find_all("div", class_="wrap_list")
        )

        for cnt, li in enumerate(images):
            if cnt % 2 == 0:  # 짝수 인덱스 요소만 처리
                video_img = li.find('img', alt="수어사전 동영상")
                if video_img:
                    video_url = video_img['src'].replace('215X161.jpg', '700X466.webm')
                    title = li.find_all('a')[1].text
                    title = re.sub(r"[^ㄱ-ㅣ가-힣\s,]", "", title).strip()
                    video_list.append({'title': title, 'url': video_url, 'length': None})

        return video_list

    async def finder(self, val):
        """Find videos for a given keyword asynchronously."""
        encoded_val = quote(val)
        url1 = f"https://sldict.korean.go.kr/front/search/searchSignCteList.do?top_category=&category=&searchKeyword={encoded_val}&searchCondition=&searchWay=&search_gubun=cte&pageIndex=1&pageJumpIndex="
        url2 = f"https://sldict.korean.go.kr/front/search/searchSignSpeList.do?top_category=&category=&searchKeyword={encoded_val}&searchCondition=&search_gubun=spe&searchWay=&pageIndex=1&pageJumpIndex="

        soup1, soup2 = await asyncio.gather(
            self.get_soup_from_url(url1),
            self.get_soup_from_url(url2)
        )

        return_list = []
        if soup1:
            return_list.extend(self.extract_video_info(soup1))
        if soup2:
            return_list.extend(self.extract_video_info(soup2))

        return return_list

    async def make_one_url(self, word):
        """Find the most appropriate URL for a given word asynchronously."""
        results = await self.finder(word)
        if results:
            url_info = sep.similar(word, results)  # Assuming sep.similar is defined elsewhere
            return url_info if url_info else None
        return None

    async def find_urls(self, words):
        """Find URLs for a list of words asynchronously."""
        urls = []
        if not words:
            return urls
        words = sep.clean(words)

        tasks = [self.make_one_url(word) for word in words]
        results = await asyncio.gather(*tasks)

        for word, dic in zip(words, results):
            url = dic['url'] if dic else None

            if url is None:
                split_words = sep.jamo_bunri(word)
                for split_word in split_words:
                    split_word = ''.join(sep.only_korean(split_word))
                    if split_word != '':
                        dic = await self.make_one_url(split_word)
                    if dic:
                        urls.append(dic)
            else:
                urls.append(dic)

        return urls

if __name__ == '__main__':  # Example
    import time

    input_text = "지구는 푸르다"

    async def main():
        async with VideoFinder() as finder:
            result_urls = await finder.find_urls(input_text)
            print(result_urls)
    
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    
    print(f"Execution time: {end_time - start_time} seconds")
