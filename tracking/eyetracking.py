## Script logging eyetracking data
## based on 
    # help https://stackoverflow.com/questions/60470644/tobii-eyetracker-with-python-unable-to-print-gaze-data
    # https://developer.tobiipro.com/tobii.research/python/reference/1.10.1.24-alpha-g6e250341/index.html

# import 
import tobii_research as tr
import logging
import time
import sys
import datetime
from CSVFormatter import CSVFormatter
from tracking_utils import pupil_data_callback,gaze_data_callback

print("eyetracking started")

# preparing logging file
fp = open(f'./logging/{sys.argv[1]}_{sys.argv[2]}eye_logging.log',mode="w")
fp.write('time,perif,location,event,valid\n')
fp.close()

# initializing logger 
logging.basicConfig(filename=f'./logging/{sys.argv[1]}_{sys.argv[2]}eye_logging.log', filemode='a',level=logging.DEBUG,format='%(message)s')
logger = logging.getLogger(__name__)
logging.root.handlers[0].setFormatter(CSVFormatter())
logging.debug(f"{datetime.datetime.now()}|eyetrack|gen|listener started|start")

# find eyetracker
my_eyetracker = False
while not my_eyetracker:
    try:
        # find eyetrackers
        found_eyetrackers = tr.find_all_eyetrackers()
        my_eyetracker = found_eyetrackers[0]
        logging.info(f"{datetime.datetime.now()}|eyetrack|gen|eyetracker found|add callbacks")
        print("Address: " + my_eyetracker.address)
        print("Model: " + my_eyetracker.model)
        print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
        print("Serial number: " + my_eyetracker.serial_number)
    except:
        # retrying if no tracker found
        # allows 
        logging.info(f"{datetime.datetime.now()}|eyetrack|gen|no eyetracker found|retrying in 5s")
        time.sleep(5)


# subscribe callbacks
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, pupil_data_callback, as_dictionary = True)
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary = True)

print("Preparation completed.")

# end script to avoid overhead (sleep > 1 day) 
time.sleep(100000)
        
# unsubscribe
my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, pupil_data_callback)
my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

logging.info(f"{datetime.datetime.now()}|eyetrack|gen|time exceeded|ending script")      