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
    print(x)
    time.sleep(1)

def multi_thread():
    with ThreadPoolExecutor() as pool:
        pool.map(my_func, input_task)
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
async def fun():
    pass
result = func()
```

<font color='red'>注意：这里函数不会执行，要执行协程函数内代码，必须要将协程对象交给事件循环来处理。</font>

## 事件循环

```python
import asyncio
async def fun():
    print('jugeng')
result = fun()
# 生成一个事件循环，好比while True
# loop = asyncio.get_event_loop()
# loop.run_until_complete(result)
# python 3.7 以后可以用这种方法代替上面得
asyncio.run(result)
```

## await

await + 可等待得对象（协程对象，future对象，task对象 --> IO等待）

await就是等待对象的计算结果后再执行下去。

案例1：

```python
import asyncio
async def fun():
    print('come')
    response = await asyncio.sleep(2)
    print('over')
asyncio.run(fun())
```

案例2：

```python
import asyncio
async def others():
    print('start')
    await asyncio.sleep(5)
    print('end')
    return '返回值'
async def func():
    print('执行协程内部代码')
    response = await others()
    print('IO请求结束，结果为', response)
asyncio.run(func())
```

案例3：

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

```python
import asyncio
async def func(x):
    print(x)
    await asyncio.sleep(5)
    print(x)
    return str(x)+'返回值'
async def main():
    print('main开始')
    # 创建task对象，把任务添加到事件循环
    task_list = [
        asyncio.create_task(func(1),name='guoli'),
        asyncio.create_task(func(2),name='ft')
    ]
    done,pending = await asyncio.wait(task_list)
    print(done)
    print('-------------------------------')
    print(pending)
    print('main结束')
asyncio.run(main())
```

