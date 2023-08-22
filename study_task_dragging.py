import component.streamlit_dragndrop.src.st_dragndrop as dnd
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 

NO_PHRASE = 5

def endTest():
    #pass
    # end subprocesses

    # write outputs in logfile
    '''
    sts[f"{DRAG_KEY}outputs"] = [val if val else "__" for val in sts[f"{DRAG_KEY}outputs"] ]
    with open(f'./logging/{sts["main_user"]}_{DRAG_KEY}user_entered.txt', "w") as f:
        for row in sts[f"{DRAG_KEY}outputs"]:
            f.write(row+"\n")'''
    st.balloons()
    # block access to test
    sts[c.D_END] = True

def changeTest():
    sts[c.STATE] = 5

def studyToggle(val:bool):
    sts[c.D_START] = val

def draggingTaskView():
    if sts[c.D_END]:
        # Test is completed
        st.success(c.SUCCESS)
        st.button(label = "Nächster Test", key = c.D_B_CHANGE, on_click=changeTest)
    elif not sts[c.D_START]:
        ## Test is not started yet
        st.write(c.D_TASK_DESC)
        st.button(label="Start Experiment", key=c.D_B_START, on_click=studyToggle, args=[True])   
    
    else:
    # TODO: generate index html before calling stuff 
        may = st.container()
        with may:
            dnd.st_dragndrop([9],"str")
        #st.components.v1.iframe(src = "http://localhost:8501", height=10)
        st.button("Beende Test",key = c.D_B_END, on_click = endTest,)