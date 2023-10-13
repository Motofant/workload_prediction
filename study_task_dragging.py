import component.streamlit_dragndrop.src.st_dragndrop as dnd
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
from datetime import datetime
from utils import startSubprocesses, manageSubProc
import json

conf.no_mouse
DATA = {
    "Powerpoint(.pptx)":["a.pptx","c.pptx","b.pptx",], 
    "Rohdaten(.xlsx)":["a.xlsx","c.xlsx","b.xlsx",],
    "Textdatein(.docx)":["a.docx","c.docx","b.docx",],       
}
def endTest():
    #pass
    # end subprocesses
    manageSubProc("kill")
    # write outputs in logfile
    with open(f'./logging/{sts[c.USER]}_{c.DRAG_KEY}user_entered.json', "w") as f:
        json.dump(sts[c.D_OUT], fp=f)
        #print(sts[c.D_OUT],file=f)

    # block access to test
    sts[c.D_END] = True

def changeTest():
    sts[c.EXP_ITER] += 1

    if sts[c.EXP_ITER] >= 3:
        sts[c.STATE] = 6
    else:
        sts[c.STATE] = sts[c.ORDER_EXP][sts[c.STAGE_ITER]][sts[c.EXP_ITER]]

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.DRAG_KEY,sts[c.USER],c.DRAG_KEY)
    sts[c.D_START] = val
    manageSubProc("resume")

def change(x):
    if not x:
        x = {}
    x["time_end"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    sts[c.D_OUT][sts[c.D_CURR]] = x #sts[c.D_D_INPUT]

    print("delete")
    #sts[c.D_B_NEXT] = None
    if c.D_D_INPUT+str(sts[c.D_CURR]) in sts:
        del sts[c.D_D_INPUT+str(sts[c.D_CURR])]

    sts[c.D_CURR] += 1

    if sts[c.D_CURR] >= conf.no_mouse:
        endTest()


def draggingTaskView():
    
    if sts[c.D_END]:
        # Test is completed
        def enableNext():
            sts[c.WORK_OUT][c.D_SLIDER] = sts[c.D_SLIDER] 
            sts[c.NEXT_TEST] = False
            

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        slid.slider(label= "Geistige Anforderung", key=c.D_SLIDER,min_value=0, max_value=20, on_change= enableNext)
        st.button(label = "Nächster Test", key = c.D_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    elif not sts[c.D_START]:
        ## Test is not started yet
        sts[c.NEXT_TEST] = True
        st.write(c.D_TASK_DESC,unsafe_allow_html=True)
        st.button(label="Starten", key=c.D_B_START, on_click=studyToggle, args=[True])  
        if c.D_OUT not in sts:
            sts[c.D_OUT] = {}
        form = st.form(key= "hi",clear_on_submit=True)
        if "test" not in sts:
            sts["test"] = 0
        _,pos,nxt = form.columns([1,3,1])
        pos.markdown(f"<center><p style= 'font-size:20px'>1/?",unsafe_allow_html=True)
        with form:
            x = dnd.st_dragndrop({"Textdatei (.txt)":["a.txt"]},key=f"x{sts['test']}", height=.6)
        y=nxt.form_submit_button("Weiter")
        if y:
            del sts[f"x{sts['test']}"]
            sts["test"] += 1
            st.experimental_rerun()
    
    else:
        if c.D_CURR not in sts:
            sts[c.D_CURR] = 0
        _,pos,nxt = st.columns([1,3,1])
        pos.markdown(f"<center><p style= 'font-size:20px'>{sts[c.D_CURR] + 1}/{conf.no_mouse}",unsafe_allow_html=True)
        x = dnd.st_dragndrop(DATA,key = c.D_D_INPUT+str(sts[c.D_CURR]),height=.8)
        y=nxt.button("Weiter", on_click = change,args=[x])
        if y:
            st.experimental_rerun()