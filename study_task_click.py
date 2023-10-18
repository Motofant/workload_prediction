import component.streamlit_sortclick.src.st_sortclick as sc
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
from datetime import datetime
from utils import startSubprocesses, manageSubProc
import json

DATA = {
    "Powerpoint(.pptx)":["a.pptx","c.pptx","b.pptx",], 
    "Rohdaten(.xlsx)":["a.xlsx","c.xlsx","b.xlsx",],
    "Textdatein(.docx)":["a.docx","c.docx","b.docx",],       
}
def endTest():
    
    # end subprocesses
    manageSubProc("kill", sub_group=c.SUB_LST)
    # write outputs in logfile
    with open(f'./logging/{sts[c.USER]}_{c.CLICK_KEY}user_entered.json', "w") as f:
        json.dump(sts[c.C_OUT], fp=f)
    # block access to test
    sts[c.C_END] = True

def changeTest():
    sts[c.EXP_ITER] += 1

    if sts[c.EXP_ITER] >= 3:
        sts[c.STATE] = 6
    else:
        sts[c.STATE] = sts[c.ORDER_EXP][sts[c.STAGE_ITER]][sts[c.EXP_ITER]]

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.PHRASE_KEY,sts[c.USER],c.CLICK_KEY,sub_group=c.SUB_LST)
    sts[c.C_START] = val
    manageSubProc("resume",sub_group=c.SUB_LST)

def change(x):
    if not x:
        x = {}
    x["time_end"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    sts[c.C_OUT][sts[c.C_CURR]] = x #sts[c.C_C_INPUT]
    #sts[c.C_B_NEXT] = None
    if c.C_C_INPUT in sts:
        del sts[c.C_C_INPUT]
        sts[c.C_B_NEXT] = None

    sts[c.C_CURR] += 1
    if sts[c.C_CURR] >= conf.no_click:
        endTest()
    

def clickingTaskView():
    
    if sts[c.C_END]:
        # Test is completed
        def enableNext():
            sts[c.WORK_OUT][c.C_SLIDER] = sts[c.C_SLIDER] 
            sts[c.NEXT_TEST] = False

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        slid.slider(label= "Geistige Anforderung", key=c.C_SLIDER,min_value=0, max_value=20, on_change= enableNext)
        st.button(label = "Nächster Test", key = c.C_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    elif not sts[c.C_START]:
        ## Test is not started yet
        sts[c.NEXT_TEST] = True
        st.write(c.C_TASK_DESC, unsafe_allow_html=True)
        st.button(label="Starten", key=c.C_B_START, on_click=studyToggle, args=[True])  
        if c.C_OUT not in sts:
            sts[c.C_OUT] = {}
        form = st.form(key= "hi",clear_on_submit=True)
        if "test" not in sts:
            sts["test"] = 0
        _,pos,nxt = form.columns([1,3,1])
        pos.markdown(f"<center><p style= 'font-size:20px'>1/?",unsafe_allow_html=True)
        with form:
            x = sc.st_sortclick({"Textdatei (.txt)":["a.txt"]}, key=f"x{sts['test']}", height=.6)
        y=nxt.form_submit_button("Beispiel zurücksetzen")
        if y:
            del sts[f"x{sts['test']}"]
            sts["test"] += 1
            st.experimental_rerun()
    
    
    else:
        if c.C_CURR not in sts:
            sts[c.C_CURR] = 0
        drag_cont = st.empty()
        _,pos,nxt = drag_cont.columns([1,3,1])

        pos.markdown(f"<center><p style= 'font-size:20px'>{sts[c.C_CURR] + 1}/{conf.no_click}", unsafe_allow_html=True)
        if c.C_C_INPUT in sts:
            del sts[c.C_C_INPUT]
        x = sc.st_sortclick(DATA,key = c.C_C_INPUT+str(sts[c.C_CURR]), height=.8)
        y=nxt.button("Weiter", on_click = change,args=[x])
        if y:
            st.experimental_rerun()