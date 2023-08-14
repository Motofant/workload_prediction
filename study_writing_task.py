import streamlit as st
import os 
import subprocess
import psutil
import signal

WRITING_KEY = "writing_"
start = "start_button"
end = "end_button"
user_in = "user_input"
active = "experiment_input"
ELEMENT_KEYS = [
    #start,
    #user_in,
    #end,
    active,
]



def startSubprocesses(site_key:str, name:str, difficulty: str, ):
    # start logging scripts
    # keyboard/mouse
    if f'{site_key}_key_mouse' not in st.session_state:
        key_mouse = subprocess.Popen(f"python ./keyboard_mouse_tracker.py {name} textTask {difficulty}", shell = False,creationflags = subprocess.CREATE_NEW_CONSOLE)
        psutil.Process(key_mouse.pid).suspend()
        st.session_state[f'{site_key}_key_mouse'] = key_mouse

    # analog


    # eyetracker

    return[f'{site_key}_key_mouse',]
    
def manageSubProc(processes:list, mode:str):
    if mode == "resume":
        st.session_state["writing_experiment_input"] = True
        for proc in processes:
            psutil.Process(st.session_state[proc].pid).resume()
        
    elif mode == "suspend":
        st.session_state["writing_experiment_input"] = False
        for proc in processes:
            psutil.Process(st.session_state[proc].pid).suspend()
    elif mode == "kill":
        st.session_state["writing_experiment_input"] = False
        for proc in processes:
            psutil.Process(st.session_state[proc].pid).kill()
            del st.session_state[proc]
    


def initSessionState(page_key, elements):
    session_elements = {}
    for key in elements:
        full_key = page_key+key
        if full_key not in st.session_state:
            st.session_state[full_key] = False
        session_elements[key] = full_key
    
    return session_elements

def textWriteView():
    keys = initSessionState(WRITING_KEY,ELEMENT_KEYS)
    sub_procs = startSubprocesses(WRITING_KEY,st.session_state["main_user"],"easy")
    
    if not st.session_state[keys[active]]:
        sub_procs = startSubprocesses(WRITING_KEY,st.session_state["main_user"],"easy")
        st.write(
            """
            Starten sie den Test mit drücken des Buttons. 
            Wenn Sie fertig sind drücken sie Stopp
            Schreiben sie einen text in dieses Feld
            """
        )
        
        st.button(label="Start Experiment", key=f"{WRITING_KEY}{start}", on_click=manageSubProc, args=[sub_procs,"resume"])
        
    else:
        print(st.session_state["main_user"])
        st.text_area(label="Eingabe", key= f"{WRITING_KEY}{user_in}")
        st.button(label="Stop Experiment", key=f"{WRITING_KEY}{end}", on_click=manageSubProc, args=[sub_procs,"kill"])