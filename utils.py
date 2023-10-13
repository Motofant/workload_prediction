from streamlit import session_state as sts
import subprocess
import psutil
import random
import sys
import constants as c
import config as conf
from pathlib import Path

PHRASE_PATH = 'volume/phrases.txt'
CONSOLE_SHOWN = subprocess.CREATE_NEW_CONSOLE if conf.sensor_console else subprocess.CREATE_NO_WINDOW

def startSubprocesses(site_key:str, name:str, task :str):
    lst_sub = []
    # start logging scripts
    # keyboard/mouse
    if f'{site_key}{c.SUB_KM}' not in sts:
        key_mouse = subprocess.Popen(f"{sys.executable} ./tracking/keyboard_mouse_tracker.py {name} {task}", shell = False,creationflags = CONSOLE_SHOWN)
        psutil.Process(key_mouse.pid).suspend()
        sts[f'{site_key}{c.SUB_KM}'] = key_mouse
        lst_sub.append(f'{site_key}{c.SUB_KM}')

    # analog
    if f'{site_key}{c.SUB_AN}' not in sts:
        analog = subprocess.Popen(f"dotnet run --project ./c_sharp/ {name} {task}", shell = False,creationflags = CONSOLE_SHOWN)
        psutil.Process(analog.pid).suspend()
        sts[f'{site_key}{c.SUB_AN}'] = analog
        lst_sub.append(f'{site_key}{c.SUB_AN}')

    # eyetracker
    if f'{site_key}{c.SUB_EY}' not in sts:
        cmd = [f"./eyeenv/Scripts/python", './tracking/eyetracking.py', {name}, {task}]
        
        eyetr = subprocess.Popen(cmd, shell = False,creationflags = CONSOLE_SHOWN)
        psutil.Process(eyetr.pid).suspend()
        sts[f'{site_key}{c.SUB_EY}'] = eyetr
        lst_sub.append(f'{site_key}{c.SUB_EY}')

    sts[c.SUB_LST] = lst_sub
    return [f'{site_key}{c.SUB_KM}',f'{site_key}{c.SUB_AN}',f'{site_key}{c.SUB_EY}',]

def manageSubProc(mode:str):
    if mode == "resume":
        for proc in sts[c.SUB_LST]:
            psutil.Process(sts[proc].pid).resume()
        
    elif mode == "suspend":
        for proc in sts[c.SUB_LST]:
            psutil.Process(sts[proc].pid).suspend()

    elif mode == "kill":
        for proc in sts[c.SUB_LST]:
            psutil.Process(sts[proc].pid).kill()
            del sts[proc]
        sts[c.SUB_LST] = []

def getPhrases(site_key:str,n_o_phrase: int):
    # phrases used from https://www.yorku.ca/mack/chi03b.pdf
    if f"{site_key}phrases" not in sts:
        all_phrases = []
        with open(PHRASE_PATH, 'r') as f:
            all_phrases = [line.strip() for line in f]

        all_ids = random.sample(population = range(len(all_phrases)), k=n_o_phrase)
        output = [all_phrases[id] for id in all_ids]
        print(f'from {len(all_phrases)} phrases have been {n_o_phrase} selected')

        # save selected phrases for later analysis
        log_path = f'./logging/{sts["main_user"]}_easy_phrases.txt' 
        with open(log_path, "w") as f:
            for i in output:
                f.write(i+"\n")
        sts[f"{site_key}phrases"] = output
        sts[f"{site_key}outputs"] = [None]*n_o_phrase

def radioFormat(x):
    vals = {
        0: "login",
        1: "start",
        2: "text",
        3: "phrase",
        4: "maus_drag",
        5: "mouse_click",
    }
    return vals[x]

def getFocusString(input_type):
    return f"""
        <script>
        var input = window.parent.document.querySelectorAll("{input_type}");
            for (var i = 0; i < input.length; ++i) {{
                input[i].focus();
            }}
    </script>
    """

def removeStreamlitElements():
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    return hide_streamlit_style

def getExpOrder(input_name:str):
    mapping = c.ORDER_DICT
    add_value = 3
    gen = mapping[input_name[0]]
    sts[c.ORDER_EXP] = {
        0:[x+add_value for x in mapping[input_name[1]]],
        1:[x+add_value for x in mapping[input_name[2]]],
        2:[x+add_value for x in mapping[input_name[3]]],
    }
    sts[c.STAGE_ITER] = 0
    sts[c.EXP_ITER] = 0
    