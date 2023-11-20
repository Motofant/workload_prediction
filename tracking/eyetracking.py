import tobii_research as tr
import logging
import io
import csv
import time
import sys
import datetime
# help https://stackoverflow.com/questions/60470644/tobii-eyetracker-with-python-unable-to-print-gaze-data
# https://developer.tobiipro.com/tobii.research/python/reference/1.10.1.24-alpha-g6e250341/index.html
print("started")
screen_dimensions = [1920, 1080] 
screen_dimensions = [1, 1] # get scale 
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
    
fp = open(f'./logging/{sys.argv[1]}_{sys.argv[2]}eye_logging.log',mode="w")
fp.write('time,perif,location,event,valid\n')
fp.close()
logging.basicConfig(filename=f'./logging/{sys.argv[1]}_{sys.argv[2]}eye_logging.log', filemode='a',level=logging.DEBUG,format='%(message)s')

logger = logging.getLogger(__name__)
print(__name__)
logging.root.handlers[0].setFormatter(CSVFormatter())
logging.debug(f"{datetime.datetime.now()}|eyetrack|gen|listener started|start")


def gaze_data_callback(gaze_data):
    # print in screendimensions
    left_eye = (gaze_data['left_gaze_point_on_display_area'][0]*screen_dimensions[0],gaze_data['left_gaze_point_on_display_area'][1]*screen_dimensions[1])
    right_eye = (gaze_data['right_gaze_point_on_display_area'][0]*screen_dimensions[0],gaze_data['right_gaze_point_on_display_area'][1]*screen_dimensions[1])
    print(f"Left: {left_eye}, Right: {right_eye}")
    dat = datetime.datetime.now()
    #logging.info(f'{gaze_data["system_time_stamp"]}|eyetrack|gaze_pos|{(gaze_data["left_gaze_point_on_display_area"],gaze_data["right_gaze_point_on_display_area"])}')
    logging.info(f'{dat}|eyetrack|gaze_left|{left_eye}')
    logging.info(f'{dat}|eyetrack|gaze_right|{right_eye}')
    
def pupil_data_callback(data):
    # pupil diameter
    print(f'pupil data ((left|right)): ({data["left_pupil_diameter"]}|{data["right_pupil_diameter"]}) at {data["system_time_stamp"]}')
    t = data["system_time_stamp"]/1000000
    dobj = datetime.datetime.fromtimestamp(t)
    #print(dobj)
    #logging.info(f'{dobj}|eyetrack|pupil_diameter|{(data["left_pupil_diameter"],data["right_pupil_diameter"])}')
    dat = datetime.datetime.now()
    logging.info(f'{dat}|eyetrack|pupil_diameter|{(data["left_pupil_diameter"],data["right_pupil_diameter"])}')
    logging.info(f'{dat}|eyetrack|pupil_valid|{(data["left_pupil_validity"],data["right_pupil_validity"])}')
    logging.info(f'{dat}|eyetrack|pupil_timest|{data["system_time_stamp"]}')
    

while True:
    try:
        found_eyetrackers = tr.find_all_eyetrackers()
        my_eyetracker = found_eyetrackers[0]

        print("Address: " + my_eyetracker.address)
        print("Model: " + my_eyetracker.model)
        print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
        print("Serial number: " + my_eyetracker.serial_number)

        my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, pupil_data_callback, as_dictionary = True)
        my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary = True)
        time.sleep(1000000)
        break
    except:
        logging.info(f"{datetime.datetime.now()}|test|test|test")
        time.sleep(5)

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, pupil_data_callback)