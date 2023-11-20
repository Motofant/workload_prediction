import playsound
import random
import time
import datetime
from pynput.keyboard import Key, Listener
import logging
import io
import csv
import sys
# based on 
# https://www.frontiersin.org/articles/10.3389/fnagi.2016.00240/full --> genutzt bei z.B. https://www.frontiersin.org/articles/10.3389/fnagi.2019.00160/full#B7
# --> Zahlen 0-9, 2,5 sec pause
# --> kannst du auch nehmen https://www.researchgate.net/profile/Bruce-Mehler/publication/230729111_MIT_AgeLab_Delayed_Digit_Recall_Task_n-backPaper_2011-3B2011-06-28/links/0912f503951996399e000000/MIT-AgeLab-Delayed-Digit-Recall-Task-n-backPaper-2011-3B2011-06-28.pdf
##logging 
class CSVFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output=io.StringIO()
        self.writer=csv.writer(self.output)

filename = f'./logging/{sys.argv[1]}_{sys.argv[2]}_n_back_in.log'

fp = open(filename,mode="w")
fp.write('time,number,event\n')
fp.close()
logging.basicConfig(filename=filename, filemode='a',level=logging.DEBUG,format='%(message)s')#%(asctime)s|

logger = logging.getLogger(__name__)
print(__name__)
logging.root.handlers[0].setFormatter(CSVFormatter())

FILE_PATH = "./n_back/speech/"

while True:
    x = random.randint(0, 9)
    logging.info(f"{datetime.datetime.now()}, {x}, called")
    print(f"{datetime.datetime.now()}, {x}, called")
    playsound.playsound(f"{FILE_PATH}{str(x)}.wav")
    
    
    time.sleep(2.5)