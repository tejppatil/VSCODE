from threading import *

# This class extends the Thread class
# It means that it is child of the Thread class

class MyThread(Thread):
    def run(self):
        for i in range(10):
            print(i, "child thread")

t = MyThread()
t.start()
t.run()

for i in range(10):
    print(i, "main thread")
