import multiprocessing
import time
# print('cpu内核数量:%s' % multiprocessing.cpu_count())

def worker(delay, count):
    # 每个进程迭代计算count次数
    for i in range(count):
        print("[%s]进程ID:%s,进程名称:%s"%
        (i,
        multiprocessing.current_process().pid,
        multiprocessing.current_process().name)
        )
        time.sleep(delay)
# 定义主函数
def main():
    # 创建3个进程
    for i in range(3):
        process = multiprocessing.Process(target=worker, args=(1,10), name='进程%s'%i)
        process.start()

if __name__ =='__main__':
    print("主进程ID:%s,主进程名称:%s"%
        (
        multiprocessing.current_process().pid,
        multiprocessing.current_process().name)
        )
    main()