import psutil
import streamlit as st
import constants as c
import streamlit.components.v1 as components
from streamlit import session_state as sts
from utils import startSubprocesses, manageSubProc, getFocusString

# creative writing task 
# let the user write a text about provideed topic

def endTest():
    # end subprocesses
    manageSubProc("kill")

    # write outputs in logfile
    
    with open(f'./logging/{sts[c.USER]}_{c.WRITING_KEY}user_entered.txt', "w") as f:
        f.write(sts[c.W_T_INPUT])
    
    # block access to test
    sts[c.W_END] = True

def changeTest():
    sts[c.STATE] = 3

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.WRITING_KEY,sts[c.USER],c.WRITING_KEY, "easy")
    sts[c.W_START] = val
    manageSubProc("resume")

def initSessionState(elements):
    session_elements = {}
    for key in elements:
        full_key = key
        if full_key not in sts:
            sts[full_key] = False
        session_elements[key] = full_key
    return session_elements

def textWriteView():
    # first start 
    if sts[c.W_END]:
        # Test is completed
        st.success(c.SUCCESS)
        st.button(label = "Nächster Test", key = c.W_B_CHANGE, on_click=changeTest)
    # currently running
    elif not sts[c.W_START]:
        ## Test is not started yet
        st.write(c.W_TASK_DESC)
        st.button(label="Start Experiment", key=c.W_B_START, on_click=studyToggle, args=[True])   
    # finished --> get to next test
    else:
        st.text_area(label="Eingabe", key= c.W_T_INPUT)
        st.button(label="Stop Experiment", key=c.W_B_END, on_click=endTest)
