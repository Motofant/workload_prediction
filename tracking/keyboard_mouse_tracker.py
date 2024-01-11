## Script logging keyboard and mouse events
## based on 
    # based on https://pythonhosted.org/pynput/keyboard.html

# imports 
from pynput.keyboard import Listener
from pynput import mouse
from CSVFormatter import CSVFormatter
from tracking_utils import on_scroll,on_click,on_move,on_press,on_release
import datetime
import logging
import sys

print("keyboard-/mouse-tracking started")

# preparing logging file
fp = open(f'./logging/{sys.argv[1]}_{sys.argv[2]}key_mouse_logging.log',mode="w")
fp.write('time,perif,location,event\n')
fp.close()

# initializing logger 
logging.basicConfig(filename=f'./logging/{sys.argv[1]}_{sys.argv[2]}key_mouse_logging.log', filemode='a',level=logging.DEBUG,format='%(message)s')
logger = logging.getLogger(__name__)
logging.root.handlers[0].setFormatter(CSVFormatter())

# subscribing to callbacks
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

