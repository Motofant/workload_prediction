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
    sub_procs = startSubprocesses(c.WRITING_KEY,sts[c.USER],c.WRITING_KEY)
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
        def enableNext():
            sts[c.WORK_OUT][c.W_SLIDER] = sts[c.W_SLIDER] 
            sts[c.NEXT_TEST] = False

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        slid.slider(label= "Geistige Anforderung", key=c.W_SLIDER,min_value=0, max_value=20, on_change= enableNext)
        st.button(label = "Nächster Test", key = c.W_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    # currently running
    elif not sts[c.W_START]:
        ## Test is not started yet
        sts[c.NEXT_TEST] = True
        
        if c.NEXT_TEST in sts:
            del sts[c.NEXT_TEST]
        st.write(c.W_TASK_DESC, unsafe_allow_html=True)
        st.button(label="Starten", key=c.W_B_START, on_click=studyToggle, args=[True])   
    # finished --> get to next test
    else:
        
        st.markdown("<center><p style= 'font-size:36px'>Inhalte der E-Mail",unsafe_allow_html=True)
        x,y = st.columns(2)
        x.markdown(c.W_M_TASK_A)
        y.markdown(c.W_M_TASK_B)
        st.text_area(label="Eingabe",height=400, key= c.W_T_INPUT, label_visibility="collapsed")
        components.html(getFocusString("textarea"),height=1)

        st.button(label="Beenden", key=c.W_B_END, on_click=endTest)
