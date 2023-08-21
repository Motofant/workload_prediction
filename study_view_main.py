import streamlit as st
from streamlit import session_state as sts
from study_task_writing import textWriteView
from study_task_phrase import phraseWriteView
from study_task_dragging import draggingTaskView
from study_view_login import loginView
from study_view_default import defaultView
from utils import radioFormat
import constants as c
import subprocess

DRAG_KEY = "dragging_"

st.set_page_config(layout="wide",initial_sidebar_state="expanded")

if c.STATE not in sts:
    sts[c.STATE] = 0

if c.USER not in sts:
    print("UserKey undefined")
    sts[c.USER] = ""

if c.P_START not in sts:
    sts[c.P_START] = False
    sts[c.P_END] = False

if c.D_START not in sts:
    sts[c.D_START] = False
    sts[c.D_END] = False    

if sts[c.USER] == "":
    loginView()
    print(sts[c.USER])
    
else:
    if sts[c.USER] == "admin":

        def radioChange():
            sts[c.STATE] = sts[c.M_R_TESTS] 

        test = st.sidebar.radio(
            label="Admin Page view",
            options=(0,1,2,3,4),
            key=c.M_R_TESTS,
            format_func=radioFormat,
            on_change=radioChange
            )
    if sts[c.STATE] in [1,5]:
        defaultView()
    elif sts[c.STATE] == 2:
        textWriteView()
    elif sts[c.STATE] == 3:
        phraseWriteView()
    elif sts[c.STATE] == 4:
        draggingTaskView()