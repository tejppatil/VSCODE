# It keeps the count before releasing the semaphores
from threading import *
import time
l =Semaphore()
l.acquire()
# l.acquire()
print("main")
l.release()
l.release()
print("main1")