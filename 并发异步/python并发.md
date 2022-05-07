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
import time
# 准备函数
def my_func(a,b):
    print(a,b)
    time.sleep(2)
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

 输出：

10 20
子线程<Thread(Thread-1, started 3964)>,线程名Thread-1
主线程<_MainThread(MainThread, started 9588)>,线程名MainThread

不加join后的输出：

10主线程<_MainThread(MainThread, started 6444)>,线程名MainThread 20

子线程<Thread(Thread-1, started 6892)>,线程名Thread-1

- start()：创建线程后通过start启动线程，等待CPU调度。
- join([timeout])：阻塞挂起调用该函数的线程，直到被调用线程执行完成或超时。通常会在主线程中调用该方法，等待其他线程执行完成。
- daemon、isDaemon()&setDaemon()：守护线程相关。

## 线程详解

### 添加多个多线程

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

## 队列Queue

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

生产者和消费者模式

生产者模块儿负责产生数据，放入缓冲区，这些数据由另一个消费者模块儿来从缓冲区取出并进行消费者相应的处理。该模式的优点在于：

解耦：缓冲区的存在可以让生产者和消费者降低互相之间的依赖性，一个模块儿代码变化，不会直接影响另一个模块儿
并发：由于缓冲区，生产者和消费者不是直接调用，而是两个独立的并发主体，生产者产生数据之后把它放入缓冲区，就继续生产数据，不依赖消费者的处理速度

```python
from queue import Queue
import time, threading
q = Queue()


def product(name):
    count = 1
    while True:
        q.put('气球兵{}'.format(count))
        print('{}训练气球兵'.format(name, count))
        count += 1
        time.sleep(5)


def consume(name):
    while True:
        print('{}使用了{}'.format(name,q.get()))
        time.sleep(1)
        q.task_done()


t1 = threading.Thread(target=product, args=('zcc',))
t2 = threading.Thread(target=consume, args=('lyy',))
t3 = threading.Thread(target=consume, args=('others',))

t1.start()
t2.start()
t3.start()
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
import numpy as np
start_time = time.time()


def multi_process():
    process_list = []
    for i in range(6):
        process = multiprocessing.Process(target=cal, args=(i,), name='process%s' % i)
        process_list.append(process)
    for j in process_list:
        j.start()
    for k in process_list:
        k.join()


def single_process():
    for i in range(6):
        cal(i)


def cal(yy):
    print("进程ID:%s,进程名称:%s" % (multiprocessing.current_process().pid, multiprocessing.current_process().name))
    x = np.random.random([1000, 20000])
    y = np.random.random([20000, 1000])
    x_dot_y = sum(sum(x.dot(y)))
    print(yy, x_dot_y)


if __name__ == '__main__':
    print("主进程ID:%s,主进程名称:%s" % (multiprocessing.current_process().pid, multiprocessing.current_process().name))
    # multi_process()
    single_process()
    print('一共用时：', time.time() - start_time)
```

## 进程池

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import time
import numpy as np
start_time = time.time()


def multi_process():
    process_list = []
    with ProcessPoolExecutor() as executor:
        results = executor.map(cal, range(6))



def single_process():
    for i in range(6):
        cal(i)


def cal(yy):
    print("进程ID:%s,进程名称:%s" % (multiprocessing.current_process().pid, multiprocessing.current_process().name))
    x = np.random.random([1000, 20000])
    y = np.random.random([20000, 1000])
    x_dot_y = sum(sum(x.dot(y)))
    print(yy, x_dot_y)


if __name__ == '__main__':
    print("主进程ID:%s,主进程名称:%s" % (multiprocessing.current_process().pid, multiprocessing.current_process().name))
    multi_process()
    #single_process()
    print('一共用时：', time.time() - start_time)


```



# asyncio异步

中文地址：[asyncio --- 异步 I/O — Python 3.10.4 文档](https://docs.python.org/zh-cn/3/library/asyncio.html)

<font color="red">event_loop事件循环</font>：程序开启一个无限的循环，程序员会把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
<font color="red">coroutine 协程</font>：协程对象，指一个使用async关键字定义的函数，它的调用不会立即执行函数，而是会返回一个协程对象。协程对象需要注册到事件循环，由事件循环调用。
<font color="red">task 任务</font>：一个协程对象就是一个原生可以挂起的函数，任务则是对协程进一步封装，其中包含任务的各种状态。
<font color="red">future</font>： 代表将来执行或没有执行的任务的结果。它和task上没有本质的区别
<font color="red">async/await 关键字</font>：python3.5 用于定义协程的关键字，async定义一个协程，await用于挂起阻塞的异步调用接口。

## 创建协程

首先定义一个协程，在def前加入async声明，就可以定义一个协程函数。

一个协程函数不能直接调用运行，只能把协程加入到事件循环loop中。然后使用run_until_complete将协程注册到事件循环，并启动事件循环。

```python
import asyncio
async def func():
    print('lyy')
# 一个coroutine 协程对象
result = func()
# 一个事件循环对象
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# 启动事件循环
loop.run_until_complete(result)
```

python3.7以后使用下面方法

```python
import asyncio
async def main():
    print('lyy')
result = main()
asyncio.run(result)
```

asyncio提供了三种执行协程的机制

1、使用asyncio.run()执行协程。一般用于执行最顶层的入口函数，如main()

2、await一个协程。一般用于在一个协程中调用另一协程

3、用asyncio.create_task()方法将Coroutine（协程）封装为Task（任务），一般用于实现异步并发操作。 需要注意的是，只有在当前线程存在事件循环的时候才能创建任务（Task）

## await

```python
import time
import asyncio
async def say_after(delay,what):
    await asyncio.sleep(delay)
    print(what)
    return 'lyy'
async def main():
    print(f"started at {time.strftime('%X')}")
    # 通过await执行协程，协程函数也可以有返回值
    a1 = await say_after(1,"hello")
    print(a1)
    await say_after(2,"world")
    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())
```

如果一个对象能够被用在await表达式中，那么我们称这个对象是可等待对象（awaitable object）

主要有三类**可等待**对象：

- 协程coroutine
- 任务Task
- 未来对象Future

## Task

```python
import time
import asyncio
async def say_after(delay,what):
    print(what)
    await asyncio.sleep(delay)
    return 'lyy_'+what
async def main():
    task1 = asyncio.create_task(say_after(5,"hello"))
    task2 = asyncio.create_task(say_after(2,"world"))
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    # task的返回值
    print(task1.result(),task2.result())
    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())
```

Task用来**并发**的调度协程。当一个协程通过类似 asyncio.create_task() 的函数被封装进一个 Task时，这个协程 会很快被自动调度执行

### asyncio.gather

```python
import asyncio
async def func(name, number):
    print(name+'_start')
    await asyncio.sleep(number)
    print(name+'_end')
    return number
async def main():
    # 并发执行多个task
    return_list = await asyncio.gather(func("A", 2),func("B", 3),func("C", 7))
    print(return_list)
asyncio.run(main())

```

### asyncio.wait

```python
import asyncio
async def func(name, number):
    print(name+'_start')
    await asyncio.sleep(number)
    print(name+'_end')
    return number
async def main():
    task_list = [asyncio.create_task(func("A", 2), name='lgy'),
                 asyncio.create_task(func("B", 3), name='lyy'),
                 asyncio.create_task(func("C", 7), name='lgl')]
    # done表示已完成的任务，pending表示未完成（超过timeout的任务）
    done, pending = await asyncio.wait(task_list,timeout=3)
    for j in pending:
        print(j)
    for i in done:
        print(i)
        print(i.result(), i.get_name())
asyncio.run(main())
```

wait的使用
在内部wait()使用一个set集合保存它创建的Task实例：
1.因为set集合是无序的所以这也就是我们的任务不是顺序执行的原因。
2.wait的返回值是一个元组，包括两个集合，分别表示已完成和未完成的任务。

gather的使用
gather的作用和wait类似，但不同的是：
1.gather任务无法取消。
2.返回值是一个结果列表。
3.可以按照传入参数的 顺序，顺序输出。
