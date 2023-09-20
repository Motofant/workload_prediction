# based on https://pythonhosted.org/pynput/keyboard.html

from pynput.keyboard import Key, Listener
from pynput import mouse
import datetime
import logging
import sys
import os
import csv
import io

##logging 
class CSVFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output=io.StringIO()
        self.writer=csv.writer(self.output)

    def format(self,record):
        record_info = record.msg.split("|")
        self.writer.writerow([record_info[0],record_info[1],record_info[2],record_info[3]])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()
fp = open(f'./logging/{sys.argv[1]}_{sys.argv[2]}_key_mouse_logging.log',mode="w")
fp.write('time,perif,location,event\n')
fp.close()
logging.basicConfig(filename=f'./logging/{sys.argv[1]}_{sys.argv[2]}_key_mouse_logging.log', filemode='a',level=logging.DEBUG,format='%(message)s')#%(asctime)s|

logger = logging.getLogger(__name__)
print(__name__)
logging.root.handlers[0].setFormatter(CSVFormatter())

def on_press (key):
    logging.info(f'{datetime.datetime.now()}|keyboard|{str(key).lower()}|pressed')

def on_release (key):
    logging.info(f'{datetime.datetime.now()}|keyboard|{str(key).lower()}|released')
    if key == Key.esc:
        #sys.exit()
        logging.debug(f'{datetime.datetime.now()}|keyboard|gen|end')
        os._exit(1)
        # Stop listener
        return False

def on_move(x, y):
    logging.info(f'{datetime.datetime.now()}|mouse|pos|{(x,y)}')
    print(f'{datetime.datetime.now()}: pointer at {(x,y)} ')
    pass
    #print(f'{datetime.datetime.now()}: pointer at {(x,y)} ')

def on_click(x, y, button, pressed):
    logging.info(f'{datetime.datetime.now()}|mouse|{button}|{"pressed" if pressed else "released"}')
    if not pressed:
        pass
        #print(f'end mouzse')
        #return False


def on_scroll(x, y, dx, dy):
    logging.info(f'{datetime.datetime.now()}|mouse|scroll|{"down" if dy < 0 else "up"} by {dy}')


#with Listener(
#    on_press=on_press,
#    on_release=on_release
#    ) as listener:
#    listener.join()

listener = Listener(
    on_press=on_press,
    on_release=on_release
    )
listener.start()
logging.debug(f"{datetime.datetime.now()}|keyboard|gen|listener started")

with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as lstnr:
    lstnr.join()
    logging.debug(f"{datetime.datetime.now()}|mouse|gen|listener started")
