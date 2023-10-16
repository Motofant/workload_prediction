import playsound
import random
import time
import datetime
from pynput.keyboard import Key, Listener
import logging
import io
import csv
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

filename = "test"

fp = open(f'./{filename}.log',mode="w")
fp.write('time,number,event\n')
fp.close()
logging.basicConfig(filename=f'./{filename}.log', filemode='a',level=logging.DEBUG,format='%(message)s')#%(asctime)s|

logger = logging.getLogger(__name__)
print(__name__)
logging.root.handlers[0].setFormatter(CSVFormatter())

end = False
def on_press (key):
    if key == Key.enter:
        global end
        print("fals")
        end = True
    print(f'{datetime.datetime.now()},{str(key).lower()}, pressed')
    logging.info(f'{datetime.datetime.now()},{key}, pressed')

listener = Listener(
    on_press=on_press,
    )
listener.start()

FILE_PATH = "./speech/"

while not end:
    x = random.randint(0, 9)

    playsound.playsound(f"{FILE_PATH}{str(x)}.wav")
    print(f"{datetime.datetime.now()}, {x}, called")
    logging.info(f"{datetime.datetime.now()}, {x}, called")
    time.sleep(2.5)