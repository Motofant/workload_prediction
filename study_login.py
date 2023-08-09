import streamlit as st
import subprocess
import psutil
MAIN_KEY = "main_"
USER_KEY = "user"

def loginView():
    print("start")
    x = st.text_input(label="Name eingeben" )
    if x != "":
        st.session_state[MAIN_KEY+USER_KEY] = x
        print(st.session_state[MAIN_KEY+USER_KEY])
        proc_text = subprocess.Popen(f"python ./keyboard_mouse_tracker.py {st.session_state['main_user']} textTask", shell = False,)#creationflags = subprocess.CREATE_NEW_CONSOLE)
        print("generation: "+str(proc_text.pid))
        psutil.Process(proc_text.pid).suspend()
        st.session_state["subprocess"] =  proc_text

        print(st.session_state["subprocess"])
        st.experimental_rerun()