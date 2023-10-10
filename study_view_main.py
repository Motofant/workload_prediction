import streamlit as st
from streamlit import session_state as sts
from study_task_writing import textWriteView
from study_task_phrase import phraseWriteView
from study_task_dragging import draggingTaskView
from study_task_click import clickingTaskView
from study_view_login import loginView
from study_view_default import defaultView
from utils import radioFormat
import constants as c

st.set_page_config(initial_sidebar_state="expanded",layout="wide")

if c.FOCUS_SUP not in st.session_state:
        st.session_state[c.FOCUS_SUP] = 0
        
if c.STATE not in sts:
    sts[c.STATE] = 0

if c.WORK_OUT not in sts:
    sts[c.WORK_OUT] = {}

if c.USER not in sts:
    print("UserKey undefined")
    sts[c.USER] = ""

if c.W_START not in sts:
    sts[c.W_START] = False
    sts[c.W_END] = False

if c.P_START not in sts:
    sts[c.P_START] = False
    sts[c.P_END] = False

if c.D_START not in sts:
    sts[c.D_START] = False
    sts[c.D_END] = False   

if c.C_START not in sts:
    sts[c.C_START] = False
    sts[c.C_END] = False

if c.NEXT_TEST not in sts:
    sts[c.NEXT_TEST] = True
   
if sts[c.USER] == "" or sts[c.STATE] == 0:
    print("before "+sts[c.USER])
    loginView()
    print(sts[c.USER])
    
else:
    if sts[c.USER] == "admin":

        def radioChange():
            sts[c.STATE] = sts[c.M_R_TESTS] 

        test = st.sidebar.radio(
            label="Admin Page view",
            options=(0,1,2,3,4,5),
            key=c.M_R_TESTS,
            format_func=radioFormat,
            on_change=radioChange
            )
    if sts[c.STATE] in [1,6]:
        defaultView()
    elif sts[c.STATE] == 2:
        textWriteView()
    elif sts[c.STATE] == 3:
        phraseWriteView()
    elif sts[c.STATE] == 4:
        draggingTaskView()
    elif sts[c.STATE] == 5:
        clickingTaskView()