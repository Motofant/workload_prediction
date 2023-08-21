import psutil
import streamlit as st
import constants as c
from streamlit import session_state as sts
from utils import startSubprocesses

# creative writing task 
# let the user write a text about provideed topic

WRITING_KEY = "writing_"
start = "start_button"
end = "end_button"
user_in = "user_input"
active = c.W_ACTIVE
ELEMENT_KEYS = [
    #start,
    #user_in,
    #end,
    active,
]

    
def manageSubProc(processes:list, mode:str):
    if mode == "resume":
        sts[c.W_ACTIVE] = True
        for proc in processes:
            psutil.Process(sts[proc].pid).resume()
        
    elif mode == "suspend":
        sts[c.W_ACTIVE] = False
        for proc in processes:
            psutil.Process(sts[proc].pid).suspend()

    elif mode == "kill":
        sts[c.W_ACTIVE] = False
        for proc in processes:
            psutil.Process(sts[proc].pid).kill()
            del sts[proc]
    


def initSessionState(elements):
    session_elements = {}
    for key in elements:
        full_key = key
        if full_key not in sts:
            sts[full_key] = False
        session_elements[key] = full_key
    return session_elements

def textWriteView():
    keys = initSessionState(ELEMENT_KEYS)
    sub_procs = startSubprocesses(c.WRITING_KEY,sts[c.USER],"text", "easy")
    
    if not sts[c.W_ACTIVE]:
        sub_procs = startSubprocesses(c.WRITING_KEY,sts[c.USER],"text", "easy")
        st.write(c.W_TASK_DESC)
        
        st.button(label="Start Experiment", key=c.W_B_START, on_click=manageSubProc, args=[sub_procs,"resume"])
        
    else:
        print(sts[c.USER])
        st.text_area(label="Eingabe", key= c.USER)
        st.button(label="Stop Experiment", key=c.W_B_END, on_click=manageSubProc, args=[sub_procs,"kill"])