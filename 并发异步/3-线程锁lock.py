import threading
import time



class Account:
    def __init__(self, balance):
        self.balance = balance
    
def draw(account, amount):
    if account.balance >= amount:
        # 这里加上延迟后就会导致两个线程之间切换了
        time.sleep(0.1)
        print(threading.current_thread().name,'取钱成功')
        account.balance -= amount
        print(threading.current_thread().name,'余额', account.balance)
    else:
        print(threading.current_thread().name,'取钱失败')


lock = threading.Lock()
def draw_lock(account, amount):
    # 加了锁的，就不会被其他线程切过去
    with lock:
        if account.balance >= amount:
            # 这里加上延迟后就会导致两个线程之间切换了
            time.sleep(0.1)
            print(threading.current_thread().name,'取钱成功')
            account.balance -= amount
            print(threading.current_thread().name,'余额', account.balance)
        else:
            print(threading.current_thread().name,'取钱失败')


if __name__ =="__main__":
    account = Account(1000)
    if 0:
        ta = threading.Thread(name='ta', target = draw, args=(account, 800))
        tb = threading.Thread(name='tb', target = draw, args=(account, 800))
    else:
        ta = threading.Thread(name='ta', target = draw_lock, args=(account, 800))
        tb = threading.Thread(name='tb', target = draw_lock, args=(account, 800))
    ta.start()
    tb.start()