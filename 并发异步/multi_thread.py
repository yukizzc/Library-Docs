import time
import requests
import threading
urls = [f"https://www.cnblogs.com/#p{page}"for page in range(1,50+1)]


def craw(url):
    r = requests.get(url)
    print(url, len(r.text))


def single_thread():
    print("single_thread begin")
    for url in urls:
        craw(url)
    print("single_thread begin")


def multi_thread():
    print("multi_thread begin")
    threads = []
    for url in urls:
        # args如果只有一个参数的话要加一个,构成元组
        threads.append(threading.Thread(target=craw, args=(url,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("multi_thread end")

if __name__ == "__main__":
    if 1:
        start = time.time()
        single_thread()
        end = time.time()
        print("single thread cost:", end-start, " seconds")
    else:
        start = time.time()
        multi_thread()
        end = time.time()
        print("multi_thread cost:", end - start, " seconds")