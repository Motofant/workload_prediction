import tobii_research as tr
import time
import logging
import io
import csv
import sys
import datetime

# help https://stackoverflow.com/questions/60470644/tobii-eyetracker-with-python-unable-to-print-gaze-data
# https://developer.tobiipro.com/tobii.research/python/reference/1.10.1.24-alpha-g6e250341/index.html

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

logging.basicConfig(filename=f'{sys.argv[1]}_{sys.argv[2]}_logging.log', filemode='w',level=logging.DEBUG,format='%(message)s')


found_eyetrackers = tr.find_all_eyetrackers()

def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
    
def pupil_data_callback(data):
    # pupil diameter
    print(f'pupil data ((left|right)): ({data["left_pupil_diameter"]}|{data["right_pupil_diameter"]}) at {data["system_time_stamp"]}')
    logging.info(f'{data["system_time_stamp"]}|eyetrack|{(data["left_pupil_diameter"],data["right_pupil_diameter"])}|pupil_diameter')
    

my_eyetracker = found_eyetrackers[0]

print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, pupil_data_callback, as_dictionary = True)

time.sleep(30)

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, pupil_data_callback)