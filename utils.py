from streamlit import session_state as sts
import subprocess
import psutil
import random
import sys
PHRASE_PATH = 'volume/phrases.txt'

def startSubprocesses(site_key:str, name:str, difficulty: str, task :str):
    # start logging scripts
    # keyboard/mouse
    if f'{site_key}_key_mouse' not in sts:
        key_mouse = subprocess.Popen(f"{sys.executable} ./tracking/keyboard_mouse_tracker.py {name} {task} {difficulty}", shell = False,creationflags = subprocess.CREATE_NEW_CONSOLE)
        psutil.Process(key_mouse.pid).suspend()
        sts[f'{site_key}_key_mouse'] = key_mouse

    # analog
    if f'{site_key}_analog' not in sts:
        analog = subprocess.Popen(f"dotnet run --project ./c_sharp/ {name} {task} {difficulty}", shell = False,creationflags = subprocess.CREATE_NEW_CONSOLE)
        psutil.Process(analog.pid).suspend()
        sts[f'{site_key}_analog'] = analog
    
    # eyetracker
    if f'{site_key}_eyetr' not in sts:
        cmd = [f"./eyeenv/Scripts/python", './tracking/eyetracking.py', {name}, {task}, {difficulty}]
        
        eyetr = subprocess.Popen(cmd, shell = False,creationflags = subprocess.CREATE_NEW_CONSOLE)
        psutil.Process(eyetr.pid).suspend()
        sts[f'{site_key}_eyetr'] = eyetr

    return[f'{site_key}_key_mouse',f'{site_key}_analog',f'{site_key}_eyetr',]

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
        4: "maus",
    }
    return vals[x]