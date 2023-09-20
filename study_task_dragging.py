import component.streamlit_dragndrop.src.st_dragndrop as dnd
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
import json
from datetime import datetime
from utils import startSubprocesses, generateIndex, manageSubProc
NO_PHRASE = 5
DATA = {
    "Powerpoint(.ppx)":["a.ppx","c.ppx","b.ppx",], 
    "Rohdaten(.xlsx)":["a.xlsx","c.xlsx","b.xlsx",],
    "Textdatein(.docs)":["a.docs","c.docs","b.docs",],       
}
def endTest():
    #pass
    # end subprocesses
    manageSubProc("kill")
    # write outputs in logfile
    with open(f'./logging/{sts[c.USER]}_{c.DRAG_KEY}user_entered.txt', "w") as f:
        print(sts[c.D_OUT],file=f)

    # block access to test
    sts[c.D_END] = True

def changeTest():
    sts[c.STATE] = 5

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.DRAG_KEY,sts[c.USER],c.DRAG_KEY, "easy")
    sts[c.D_START] = val
    manageSubProc("resume")

def change(x):
    if not x:
        x = {}
    x["time_end"] = datetime.now().strftime('%Y%m%d%H%M%S%f')
    sts[c.D_OUT][sts[c.D_CURR]] = x #sts[c.D_D_INPUT]

    print("delete")
    #sts[c.D_B_NEXT] = None
    if c.D_D_INPUT+str(sts[c.D_CURR]) in sts:
        #print("akljsdhfkljasdhjkldfsahjklsdfahjklfsdhlkjdfkhjlfafashjdklsdafhlhlhlhlhlhlhlhlhlhlhlkj")
        del sts[c.D_D_INPUT+str(sts[c.D_CURR])]


    sts[c.D_CURR] = min(max(sts[c.D_CURR]+1,0),NO_PHRASE-1)


def draggingTaskView():
    
    if sts[c.D_END]:
        # Test is completed
        st.success(c.SUCCESS)
        st.button(label = "Nächster Test", key = c.D_B_CHANGE, on_click=changeTest)
    elif not sts[c.D_START]:
        ## Test is not started yet
        st.write(c.D_TASK_DESC)
        st.button(label="Start Experiment", key=c.D_B_START, on_click=studyToggle, args=[True])  
        if c.D_OUT not in sts:
            sts[c.D_OUT] = {}
        ## generate html for component
        #generateIndex(DATA, True)
    
    else:
        if c.D_CURR not in sts:
            sts[c.D_CURR] = 0
        #nxt.button("nächster Eintrag",key=c.D_B_NEXT, on_click = change,disabled=sts[c.D_CURR]>=NO_PHRASE-1)
        _,pos,nxt = st.columns([1,3,1])
        pos.markdown(f"{sts[c.D_CURR] + 1}/{conf.no_phrases}")
        x = dnd.st_dragndrop(DATA,key = c.D_D_INPUT+str(sts[c.D_CURR]))
        y=nxt.button("nächster Eintrag", on_click = change,args=[x],disabled=sts[c.D_CURR]>=NO_PHRASE-1)
        if y:
            st.experimental_rerun()
        st.button("Beende Test",key = c.D_B_END, on_click = endTest,)
        

        #print(sts[c.D_D_INPUT])
        #print(sts)
        