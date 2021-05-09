import time
import requests
import threading
from bs4 import BeautifulSoup
import queue
import random
urls = [f"https://www.cnblogs.com/#p{page}"for page in range(1,50+1)]


# 下载网页内容
def craw(url):
    r = requests.get(url)
    return r.text


# 解析网页
def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('a', class_="post-item-title")
    return [(link['href'], link.get_text()) for link in links]


# 生产者
def do_craw(url_queue:queue.Queue, html_queue:queue.Queue):
    while True:
        url = url_queue.get()
        html = craw(url)
        html_queue.put(html)
        print(threading.current_thread().name, f"craw {url}","url_queue.size=", url_queue.qsize())
        time.sleep(random.randint(1, 2))


# 消费者
def do_parse(html_queue:queue.Queue, fout):
    while True:
        html = html_queue.get()
        results = parse(html)
        for result in results:
            fout.write(str(result) + "\n")
        print(threading.current_thread().name, f"results.size", len(results), "html_queue.size=", html_queue.qsize())
        time.sleep(random.randint(1, 2))


if __name__ == "__main__":
    if 1:
        for result in parse(craw(urls[2])):
            print(result)
    else:
        url_queue = queue.Queue()
        html_queue = queue.Queue()
        for url in urls:
            url_queue.put(url)
        for idx in range(3):
            t = threading.Thread(target=do_craw, args=(url_queue, html_queue), name=f"craw{idx}")
            t.start()
        fout = open("02.data.txt", "w")
        for idx in range(2):
            t = threading.Thread(target=do_parse, args=(html_queue, fout), name=f"craw{idx}")
            t.start()