import threading
import time

def func(sec):
    for i in range(3):
        print(f"Sleeping for {sec} seconds")

t1=threading.Thread(target=func,args=[4])
t2=threading.Thread(target=func,args=[2])
t3=threading.Thread(target=func,args=[1])


t1.start()
t1.join()
t2.start()
t3.start()
