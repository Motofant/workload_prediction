import streamlit as st
from study_task_writing import textWriteView
from study_task_phrase import phraseWriteView
from study_task_dragging import draggingTaskView
from study_login import loginView
import subprocess

MAIN_KEY = "main_"
PHRASE_KEY = "phrase_"
DRAG_KEY = "dragging_"
USER_KEY = "user"
st.set_page_config(layout="wide",initial_sidebar_state="expanded")

if MAIN_KEY+USER_KEY not in st.session_state:
    print("UserKey undefined")
    st.session_state[MAIN_KEY+USER_KEY] = ""

if f'{PHRASE_KEY}completed' not in st.session_state:
    st.session_state[f'{PHRASE_KEY}started'] = False
    st.session_state[f'{PHRASE_KEY}completed'] = False

if f'{DRAG_KEY}completed' not in st.session_state:
    st.session_state[f'{DRAG_KEY}started'] = False
    st.session_state[f'{DRAG_KEY}completed'] = False    

if st.session_state[MAIN_KEY+USER_KEY] == "":
    loginView()
    print(st.session_state[MAIN_KEY+USER_KEY])
    
else:
    test = st.sidebar.radio(
        label="Modus",
        options=('default', 'text', 'phrase','maus'),
        key=f'{MAIN_KEY}tests',
        )
    if st.session_state[f'{MAIN_KEY}tests'] == 'default':
        st.write("default")
    elif st.session_state[f'{MAIN_KEY}tests'] == 'text':
        textWriteView()
    elif st.session_state[f'{MAIN_KEY}tests'] == 'phrase':
        phraseWriteView()
    elif st.session_state[f'{MAIN_KEY}tests'] == 'maus':
        draggingTaskView()