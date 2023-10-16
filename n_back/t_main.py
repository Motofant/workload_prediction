from multiprocessing import Process, Manager
import subprocess
import psutil
import sys
import signal
import threading
import multiprocessing
from sound_record import testFkt
import time
if __name__ == "__main__":
    # pool = multiprocessing.Pool(5)
    # y = Manager()

    # x = Process(target=testFkt)
    # #x = threading.Thread(target=testFkt)
    # x.start()
    # pool.apply_async(x)
    # i =0
    # while i < 3:
    #     print(i)
    #     i+=1
    #     time.sleep(1)

    # x.kill()
    # x.terminate()
    # x.close()

    mic_in = subprocess.Popen(f"{sys.executable} ./n_back/n_back_gen.py",shell = False,creationflags = subprocess.CREATE_NEW_CONSOLE)

    i =0
    while i < 3:
        print(i)
        i+=1
        time.sleep(1)
    #mic_in.communicate(input = )
    psutil.Process(mic_in.pid).kill()