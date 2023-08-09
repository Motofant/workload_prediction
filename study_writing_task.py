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


def activateStudy(started, process):
    st.session_state[WRITING_KEY+active] = started
    print(f'in Onclick proc {process.pid}')
    if started:
        print("start")
        psutil.Process(process.pid).resume()
    else:
        print("stop")
        psutil.Process(process.pid).kill()


def initSessionState(page_key, elements):
    session_elements = {}
    for key in elements:
        full_key = page_key+key
        if full_key not in st.session_state:
            st.session_state[full_key] = False
        session_elements[key] = full_key
    
    return session_elements

def textWriteView(process, id):
    keys = initSessionState(WRITING_KEY,ELEMENT_KEYS)
    pid = id
    print(f'popen retuned {id}')
    #print(f'parent ID  {os.getppid()}')
    print(f'popen current {process.pid}')
    #psutil.Process(process.pid).suspend()
    
    
    if not st.session_state[keys[active]]:
        
        st.write(
            """
            Starten sie den Test mit drücken des Buttons. 
            Wenn Sie fertig sind drücken sie Stopp
            Schreiben sie einen text in dieses Feld
            """
        )
        
        st.button(label="Start Experiment", key=f"{WRITING_KEY}{start}", on_click=activateStudy, args=[True,process])
        
    else:
        print(st.session_state["main_user"])
        st.text_area(label="Eingabe", key= f"{WRITING_KEY}{user_in}")
        st.button(label="Stop Experiment", key=f"{WRITING_KEY}{end}", on_click=activateStudy, args=[False,process])