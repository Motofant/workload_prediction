import component.streamlit_dragndrop.src.st_dragndrop as dnd
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
import json
from utils import startSubprocesses, generateIndex, manageSubProc
NO_PHRASE = 5
DATA = ["a","b","c","d"] 
def endTest():
    #pass
    # end subprocesses
    manageSubProc("kill")
    # write outputs in logfile
    with open(f'./logging/{sts[c.USER]}_{c.DRAG_KEY}user_entered.txt', "w") as f:
        print(sts[c.D_OUT],file=f)

    st.balloons()
    # block access to test
    sts[c.D_END] = True

def changeTest():
    sts[c.STATE] = 5

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.PHRASE_KEY,sts[c.USER],"dragging", "easy")
    sts[c.D_START] = val
    manageSubProc("resume")

def change(x):
    sts[c.D_OUT][sts[c.D_CURR]] = x #sts[c.D_D_INPUT]
    sts[c.D_CURR] = min(max(sts[c.D_CURR]+1,0),NO_PHRASE-1)
    print("delete")
    #sts[c.D_B_NEXT] = None
    if c.D_D_INPUT in sts:
        print("del")
        del sts[c.D_D_INPUT]
        #del sts[c.D_B_NEXT]
        sts[c.D_B_NEXT] = None
        print(sts)
    #del sts[c.D_B_END]
    draggingTaskView()

def draggingTaskView():
    
    if sts[c.D_END]:
        # Test is completed
        st.success(c.SUCCESS)
        print(sts)
        st.button(label = "Nächster Test", key = c.D_B_CHANGE, on_click=changeTest)
    elif not sts[c.D_START]:
        ## Test is not started yet
        st.write(c.D_TASK_DESC)
        st.button(label="Start Experiment", key=c.D_B_START, on_click=studyToggle, args=[True])  
        if c.D_OUT not in sts:
            sts[c.D_OUT] = {}
        ## generate html for component
        generateIndex(DATA, True)
    
    else:
        if c.D_CURR not in sts:
            sts[c.D_CURR] = 0
        drag_cont = st.empty()
        prev,pos,nxt = drag_cont.columns([1,3,1])
        #nxt.button("nächster Eintrag",key=c.D_B_NEXT, on_click = change,disabled=sts[c.D_CURR]>=NO_PHRASE-1)
        
        pos.markdown(f"{sts[c.D_CURR] + 1}/{NO_PHRASE}")
        print(sts)
        if c.D_D_INPUT in sts:
            del sts[c.D_D_INPUT]
        x = dnd.st_dragndrop(DATA,key = c.D_D_INPUT+str(sts[c.D_CURR]))
        y=nxt.button("nächster Eintrag", on_click = change,args=[x],disabled=sts[c.D_CURR]>=NO_PHRASE-1)
        if y:
            x = None
        #print(sts[c.D_D_INPUT])
        #print(sts)
        st.button("Beende Test",key = c.D_B_END, on_click = endTest,)