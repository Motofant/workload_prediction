from streamlit import session_state as sts
import subprocess
import psutil
import random

PHRASE_PATH = 'volume/phrases.txt'

def startSubprocesses(site_key:str, name:str, difficulty: str, ):
    # start logging scripts
    # keyboard/mouse
    if f'{site_key}_key_mouse' not in sts:
        key_mouse = subprocess.Popen(f"python ./tracking/keyboard_mouse_tracker.py {name} textTask {difficulty}", shell = False,creationflags = subprocess.CREATE_NEW_CONSOLE)
        psutil.Process(key_mouse.pid).suspend()
        sts[f'{site_key}_key_mouse'] = key_mouse

    # analog
    if f'{site_key}_analog' not in sts and False:
        analog = subprocess.Popen(f" {name} textTask {difficulty}", shell = False,creationflags = subprocess.CREATE_NEW_CONSOLE)
        psutil.Process(key_mouse.pid).suspend()
        sts[f'{site_key}_analog'] = analog

    # eyetracker

    return[f'{site_key}_key_mouse',]

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
