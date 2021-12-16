# 总览

## 概要

参考地址[GitHub - peiss/ant-learn-python-concurrent: Python并发编程专题](https://github.com/peiss/ant-learn-python-concurrent)

- 多线程：threading，利用CPU和IO可以同时执行的原理，让CPU不会干巴巴等待IO完成

- 多进程：multiprocessing，利用多核CPU的能力，真正的并行执行任务

- 异步IO：asyncio，在单线程利用CPU和IO同时执行的原理，实现函数异步执行


- 使用Lock对资源加锁，防止冲突访问

- 使用Queue实现不同线程/进程之间的数据通信，实现生产者-消费者模式

- 使用线程池Pool/进程池Pool，简化线程/进程的任务提交、等待结束、获取结果

- 使用subprocess启动外部程序的进程，并进行输入输出交互

## CPU和IO密集型区别

- CPU密集型（CPU-bound）：


CPU密集型也叫计算密集型，是指I/O在很短的时间就可以完成，CPU需要大量的计算和处理，特点是CPU占用率相当高

例如：压缩解压缩、加密解密、正则表达式搜索

- IO密集型（I/O bound）：


IO密集型指的是系统运作大部分的状况是CPU在等I/O (硬盘/内存) 的读/写操作，CPU占用率仍然较低。

例如：文件处理程序、网络爬虫程序、读写数据库程序

## 多进程、多线程、多协程的对比

![](img\1.png)

# 多线程

## 创建多线程

```python
# 准备函数
def my_func(a,b):
    print(a,b)
    print('子线程%s,线程名%s'%(threading.current_thread(),threading.current_thread().name))
# 创建一个线程
import threading
t = threading.Thread(target = my_func, args = (10,20))
# 启动线程
t.start()
# 等待结束
t.join()
print('主线程%s,线程名%s'%(threading.current_thread(),threading.current_thread().name))
```

 Join方法：如果一个线程在执行过程中要调用另外一个线程，并且等到其完成以后才能接着执行那么在调用这个线程时可以使用join方法。主线程挨个调用子线程的 join()方法，当所调用子线程都执行完毕后主线程才会执行下面的代码

## 线程详解

### 默认多线程

```python
import threading
import time

def run():
    time.sleep(2)
    print('当前线程的名字是： ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':

    start_time = time.time()

    print('这是主线程：', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.start()

    print('主线程结束！' , threading.current_thread().name)
    print('一共用时：', time.time()-start_time)
```

这是主线程： MainThread
主线程结束！ MainThread        
一共用时： 0.002965688705444336
当前线程的名字是：  Thread-3
当前线程的名字是：  Thread-5
当前线程的名字是：  Thread-2
当前线程的名字是：  Thread-1
当前线程的名字是：  Thread-4

当一个进程启动之后，会默认产生一个主线程，因为线程是程序执行流的最小单元，当设置多线程时，主线程会创建多个子线程，在python中，默认情况下（其实就是setDaemon(False)），主线程执行完自己的任务以后，就退出了，此时子线程会继续执行自己的任务，直到自己的任务结束

### 设置守护线程

```python
import threading
import time

def run():

    time.sleep(2)
    print('当前线程的名字是:', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':

    start_time = time.time()

    print('这是主线程:', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    print('主线程结束了!' , threading.current_thread().name)
    print('一共用时:', time.time()-start_time)
```

这是主线程: MainThread
主线程结束了! MainThread      
一共用时: 0.000972747802734375

当我们使用setDaemon(True)方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行，可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止

### join的作用

```python
import threading
import time

def run():

    time.sleep(2)
    print('当前线程的名字是: ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':

    start_time = time.time()

    print('这是主线程:', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

    print('主线程结束了!' , threading.current_thread().name)
    print('一共用时:', time.time()-start_time)
```

这是主线程: MainThread
当前线程的名字是:  Thread-5
当前线程的名字是:  Thread-1
当前线程的名字是:  Thread-4
当前线程的名字是:  Thread-2
当前线程的名字是:  Thread-3
主线程结束了! MainThread
一共用时: 4.0111846923828125

join的作用就凸显出来了，join所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程在终止

## 生产消费者模式

在多线程开发当中，如果生产线程处理速度很快，而消费线程处理速度很慢，那么生产线程就必须等待消费线程处理完，才能继续生产数据。同样的道理，如果消费线程的处理能力大于生产线程，那么消费线程就必须等待生产线程。为了解决这个问题于是引入了生产者和消费者模式
生产者消费者模式是通过一个容器来解决生产者和消费者的强耦合问题。生产者和消费者彼此之间不直接通讯，而通过阻塞队列来进行通讯，所以生产者生产完数据之后不用等待消费者处理，直接扔给阻塞队列，消费者不找生产者要数据，而是直接从阻塞队列里取，阻塞队列就相当于一个缓冲区，平衡了生产者和消费者的处理能力。

```python
import queue
# 创建类对象
q = queue.Queue()
# 添加元素
q.put(item)
# 获取元素
item = q.get()
# 查看元素数量
q.qsize()
# 判断是否为空，是否已满
q.empty(), q.full()
```

queue.Queue用于多线程之间的线程数据通信，它遵循队列先进先出的原则。

```python
import queue
q = queue.Queue()
for i in range(10):
    q.put(i)
print('队列已满%s,队列长度为%s'%(q.full(),q.qsize()))
for j in range(q.qsize()):
    print('队列中第一个数为%s,队列长度为%s'%(q.get(),q.qsize()))
```

## 线程安全

多个线程操作同一个数据时候可能会发送同时修改，下面例子x这个全局变量按理只会被一个线程运行，但因为有延迟的IO等到导致两个线程同时挂起，最后x都被执行了

```python
import threading
import time
def do():
    global x
    if x == 0:
        time.sleep(1)
        print(threading.current_thread().name)
        x+=1
x = 0
t1 = threading.Thread(target=do,args=(),name='t1')
t2 = threading.Thread(target=do,args=(),name='t2')
t1.start()
t2.start()
t1.join()
t2.join()
print(x)
```

解决办法很简单加一个LOCK锁，当第一个线程运行到do函数时候把线程给锁了，其他线程就不会执行do函数

```python
import threading
import time
lock = threading.Lock()
def do():
    with lock:
        global x
        if x == 0:
            time.sleep(1)
            print(threading.current_thread().name)
            x+=1
x = 0
t1 = threading.Thread(target=do,args=(),name='t1')
t2 = threading.Thread(target=do,args=(),name='t2')
t1.start()
t2.start()
t1.join()
t2.join()
print(x)
```

## 线程池

自动创建多线程，这里创建几个多线程根据输入的任务长度有关，下面例子input_task_里有三个参数表示三个任务，会自动创建三个线程。每一个线程计算input_task里面的一个数。

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import time
input_task = [10, 20, 30]
# 准备函数
def my_func(x):
    print('子线程%s,线程名%s'%(threading.current_thread(),threading.current_thread().name))
    # print(x)
    time.sleep(1)
    return x
def multi_thread():
    with ThreadPoolExecutor() as pool:
        results = pool.map(my_func, input_task)
    # 线程池可以有 返回值
    for out in results:
        print(out)
multi_thread()
print('主线程%s,线程名%s'%(threading.current_thread(),threading.current_thread().name))
```



# 多进程

## 创建多进程

![](img\2.png)

```python
import multiprocessing
import time

def worker(delay, count):
    # 每个进程迭代计算count次数
    for i in range(count):
        print("进程ID:%s,进程名称:%s，第[%s]次执行"%
        (multiprocessing.current_process().pid,multiprocessing.current_process().name,i+1)
        )
        time.sleep(delay)
# 定义主函数
def main():
    # 创建3个进程
    for i in range(3):
        process = multiprocessing.Process(target=worker, args=(1,3), name='process%s'%i)
        process.start()

if __name__ =='__main__':
    print('cpu内核数量:%s' % multiprocessing.cpu_count())
    print("主进程ID:%s,主进程名称:%s"%
        (
        multiprocessing.current_process().pid,
        multiprocessing.current_process().name)
        )
    main()
```

# 协程

## 定义协程函数

协程函数：定义函数时候async def 函数名

协程对象：协程函数（）返回的对象

```python
import asyncio
async def fun():
    print('jugeng')
result = fun()
# 生成一个事件循环，好比while True
# loop = asyncio.get_event_loop()
# loop.run_until_complete(result)
# python 3.7 以后可以用这种方法代替上面得
# 用asyncio.run来运行协程
asyncio.run(result)
```

## 并发运行多个协程

main()是普通运行协程函数，执行的时候会依次执行

main2()通过creat_task创建并发的协程

```python
import asyncio
import time

async def say_after(delay, what):
    print(what+'__'+f"started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(what+'__'+f"finished at {time.strftime('%X')}")
    
async def main():
    await say_after(5, 'hello')
    await say_after(2, 'world')

async def main2():
    task1 = asyncio.create_task(say_after(5, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    await task1
    await task2
print('第一种')
asyncio.run(main())
print('第二种')
asyncio.run(main2())
```
输出的结果如下，可以看到第一种是依次执行hello然后是world。第二种方式hello和world是同时执行了
```tex
第一种
hello__started at 16:08:41
hello__finished at 16:08:46
world__started at 16:08:46
world__finished at 16:08:48
第二种
hello__started at 16:08:48
world__started at 16:08:48
world__finished at 16:08:50
hello__finished at 16:08:53
```

## await

await + 可等待得对象（协程对象，future对象，task对象 --> IO等待）

协程遇到await，事件循环将会挂起该协程，执行别的协程，直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行，协程的目的也是让一些耗时的操作异步化。

```python
import asyncio
import time
async def others(x):
    print(str(x)+'start')
    await asyncio.sleep(5)
    print(str(x)+'end')
    return str(x)+'的返回值'
async def func():
    print('执行协程内部代码')
    # await等执行结束了，执行后面程序
    response1 = await others(1)
    print('IO请求结束，结果为', response1)
    response2 = await others(2)
    print('IO请求结束，结果为', response2)
asyncio.run(func())
```

## Task对象

Task对象是指：与任务调度，和并发有关，是指帮助在事件循环中并发的向任务列表，添加多个任务。task用于并发调度协程，通过asyncio.create_task(协程对象)的方式创建Task对象，这样可以让协程加入事件循环中等待被调度执行

```python
import asyncio
import datetime
async def func(x):
    start_ti = datetime.datetime.today()
    print(x,start_ti)
    await asyncio.sleep(5)
    print(x,datetime.datetime.today()-start_ti)
    return str(x)+'返回值'
async def main():
    print('main开始')
    # 创建task对象，把任务添加到事件循环
    task1 = asyncio.create_task(func(1),name='guoli')
    task2 = asyncio.create_task(func(2),name='ft')
    print('main结束')
    res1 = await task1
    res2 = await task2
    print(res1)
    print(res2)
asyncio.run(main())
```

输出结果，可以看到1和2的任务同时开启了

```txt
main开始
main结束
1 2021-05-12 16:27:20.670393
2 2021-05-12 16:27:20.670393
1 0:00:05.012028
2 0:00:05.012028
1返回值
2返回值
```

