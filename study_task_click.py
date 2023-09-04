import component.streamlit_sortclick.src.st_sortclick as sc
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
from utils import startSubprocesses, generateIndex, manageSubProc
NO_CLICKS = 5
DATA = ["a","b","c","d"] 
def endTest():
    sts[c.C_OUT][sts[c.C_CURR]] = sts[c.C_C_INPUT+str(sts[c.C_CURR])]
    # end subprocesses
    manageSubProc("kill")
    # write outputs in logfile
    with open(f'./logging/{sts[c.USER]}_{c.CLICK_KEY}user_entered.txt', "w") as f:
        print(sts[c.C_OUT],file=f)

    st.balloons()
    # block access to test
    sts[c.C_END] = True

def changeTest():
    sts[c.STATE] = 6

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.PHRASE_KEY,sts[c.USER],c.CLICK_KEY, "easy")
    sts[c.C_START] = val
    manageSubProc("resume")

def change(x):
    sts[c.C_OUT][sts[c.C_CURR]] = x #sts[c.C_C_INPUT]
    sts[c.C_CURR] = min(max(sts[c.C_CURR]+1,0),NO_CLICKS-1)
    print("delete")
    #sts[c.C_B_NEXT] = None
    if c.C_C_INPUT in sts:
        print("del")
        del sts[c.C_C_INPUT]
        sts[c.C_B_NEXT] = None
        print(sts)
    #del sts[c.C_B_END]
    clickingTaskView()

def clickingTaskView():
    
    if sts[c.C_END]:
        # Test is completed
        st.success(c.SUCCESS)
        print(sts)
        st.button(label = "Nächster Test", key = c.C_B_CHANGE, on_click=changeTest)
    elif not sts[c.C_START]:
        ## Test is not started yet
        st.write(c.C_TASK_DESC)
        st.button(label="Start Experiment", key=c.C_B_START, on_click=studyToggle, args=[True])  
        if c.C_OUT not in sts:
            sts[c.C_OUT] = {}
        ## generate html for component
        generateIndex(DATA, True)
    
    else:
        if c.C_CURR not in sts:
            sts[c.C_CURR] = 0
        drag_cont = st.empty()
        _,pos,nxt = drag_cont.columns([1,3,1])

        pos.markdown(f"{sts[c.C_CURR] + 1}/{NO_CLICKS}")
        print(sts)
        if c.C_C_INPUT in sts:
            del sts[c.C_C_INPUT]
        x = sc.st_sortclick(DATA,key = c.C_C_INPUT+str(sts[c.C_CURR]))
        y=nxt.button("nächster Eintrag", on_click = change,args=[x],disabled=sts[c.C_CURR]>=NO_CLICKS-1)
        if y:
            x = None
        #print(sts[c.C_C_INPUT])
        #print(sts)
        st.button("Beende Test",key = c.C_B_END, on_click = endTest,)