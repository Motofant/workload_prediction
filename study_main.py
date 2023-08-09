import streamlit as st
from study_writing_task import textWriteView
from study_login import loginView
import subprocess
import os

MAIN_KEY = "main_"
USER_KEY = "user"
st.set_page_config(layout="wide",initial_sidebar_state="expanded")

    

if MAIN_KEY+USER_KEY not in st.session_state:
    print("UserKey undefined")
    st.session_state[MAIN_KEY+USER_KEY] = ""

if st.session_state[MAIN_KEY+USER_KEY] == "":
    
    loginView()
    print(st.session_state[MAIN_KEY+USER_KEY])
    
else:
    test = st.sidebar.radio(
        label="Modus",
        options=('default', 'text', 'mouse'),
        key=f'{MAIN_KEY}tests',
        )
    if st.session_state[f'{MAIN_KEY}tests'] == 'default':
        st.write("default")
    if st.session_state[f'{MAIN_KEY}tests'] == 'text':
        process = st.session_state["subprocess"]
        id = process.pid
        print(f'process Id {id}')
        textWriteView(process, id)
    if st.session_state[f'{MAIN_KEY}tests'] == 'mouse':
        st.write("TODO: mouse")
    