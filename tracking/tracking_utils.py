## functions used for tracking 

# imports
import logging
from datetime import datetime
from pynput.keyboard import Key
import os

# Eyetracking 
screen_dimensions = [1920, 1080] 
screen_dimensions = [1, 1] # get scale 


def gaze_data_callback(gaze_data):
    # Gaze direction
    # print in screendimensions
    left_eye = (gaze_data['left_gaze_point_on_display_area'][0]*screen_dimensions[0],gaze_data['left_gaze_point_on_display_area'][1]*screen_dimensions[1])
    right_eye = (gaze_data['right_gaze_point_on_display_area'][0]*screen_dimensions[0],gaze_data['right_gaze_point_on_display_area'][1]*screen_dimensions[1])
    print(f"Left: {left_eye}, Right: {right_eye}")

    dat = datetime.now()
    logging.info(f'{dat}|eyetrack|gaze_left|{left_eye}')
    logging.info(f'{dat}|eyetrack|gaze_right|{right_eye}')
    
def pupil_data_callback(data):
    # pupil diameter
    print(f'pupil data ((left|right)): ({data["left_pupil_diameter"]}|{data["right_pupil_diameter"]}) at {data["system_time_stamp"]}')
    dat = datetime.now()
    logging.info(f'{dat}|eyetrack|pupil_diameter|{(data["left_pupil_diameter"],data["right_pupil_diameter"])}')
    logging.info(f'{dat}|eyetrack|pupil_valid|{(data["left_pupil_validity"],data["right_pupil_validity"])}')
    logging.info(f'{dat}|eyetrack|pupil_timest|{data["system_time_stamp"]}')
    

# Keybord/Mouse
def on_move(x, y):
    logging.info(f'{datetime.now()}|mouse|pos|{(x,y)}')

def on_click(x, y, button, pressed):
    logging.info(f'{datetime.now()}|mouse|{button}|{"pressed" if pressed else "released"}')

def on_scroll(x, y, dx, dy):
    logging.info(f'{datetime.now()}|mouse|scroll|{"down" if dy < 0 else "up"} by {dy}')

def on_release (key):
    logging.info(f'{datetime.now()}|keyboard|{str(key).lower()}|released')
    if key == Key.esc:
        logging.debug(f'{datetime.now()}|keyboard|gen|end')
        os._exit(1)

def on_press (key):
    logging.info(f'{datetime.now()}|keyboard|{str(key).lower()}|pressed')
