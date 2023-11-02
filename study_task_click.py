import component.streamlit_sortclick.src.st_sortclick as sc
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
from utils import startSubprocesses, manageSubProc,format_perf,format_gen
import json
from datetime import datetime as dt
import datetime

DATA = {
    "Powerpoint(.pptx)":["a.pptx","c.pptx","b.pptx",], 
    "Rohdaten(.xlsx)":["a.xlsx","c.xlsx","b.xlsx",],
    "Textdatein(.docx)":["a.docx","c.docx","b.docx",],       
}
DATA={
        "Datein aus Kalenderwoche 20":["dataKW20.txt","infoKW20.txt","info2KW20.txt",], 
        "Datein aus Kalenderwoche 30":["dataKW30.txt","infoKW30.txt","info2KW30.txt",],
        "Datein aus Kalenderwoche 40":["dataKW40.txt","infoKW40.txt","info2KW40.txt",],
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
    x["time_end"] = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    sts[c.C_OUT][sts[c.C_CURR]] = x #sts[c.C_C_INPUT]
    #sts[c.C_B_NEXT] = None
    if c.C_C_INPUT in sts:
        del sts[c.C_C_INPUT]
        sts[c.C_B_NEXT] = None

    sts[c.C_CURR] += 1
    if sts[c.C_CURR] >= conf.no_click:
        endTest()
    
def clickingExampleView():
    # used to introduce user to type of experiment
    if "started" not in sts:
        sts["started"] = False 
    
    if not sts["started"]:
        # show explanation
        st.header("Beispiel: Klick")
        st.write(c.C_TASK_DESC,unsafe_allow_html=True)
        start = st.button("Beginne Aufgabe")
        if start:
            sts["started"] = True
            st.experimental_rerun()
    else:
        # timer 
        if "time" not in sts:
            sts["time"] = dt.now()
        time_in_sec = conf.sec_per_example
        
        if dt.now() < (sts["time"] + datetime.timedelta(seconds=time_in_sec)): 
            if c.C_OUT not in sts:
                sts[c.C_OUT] = {}
            form = st.form(key= "hi",clear_on_submit=True)
            if "test" not in sts:
                sts["test"] = 0
            _,pos,nxt = form.columns([1,3,1])
            pos.markdown(f"<center><p style= 'font-size:20px'>1/?",unsafe_allow_html=True)
            with form:
                x = sc.st_sortclick({"Textdatei (.txt)":["a.txt"]}, key=f"x{sts['test']}", height=.6)
            y=nxt.form_submit_button("Weiter")
            if y:
                del sts[f"x{sts['test']}"]
                sts["test"] += 1
                st.experimental_rerun()
        else:
            # call toggle to nex example
            sts[c.STATE] = 10
            del sts["time"]
            del sts["started"]
            st.experimental_rerun()

def clickingTaskView():
    
    if sts[c.C_END]:
        # Test is completed
        # Test is completed
        def enableNext():
            sts[c.WORK_OUT][c.C_M_SLIDER] = sts[c.C_M_SLIDER] 
            sts[c.WORK_OUT][c.C_E_SLIDER] = sts[c.C_E_SLIDER] 
            sts[c.WORK_OUT][c.C_F_SLIDER] = sts[c.C_F_SLIDER] 
            sts[c.WORK_OUT][c.C_PHY_SLIDER] = sts[c.C_PHY_SLIDER] 
            sts[c.WORK_OUT][c.C_T_SLIDER] = sts[c.C_T_SLIDER] 
            sts[c.WORK_OUT][c.C_P_SLIDER] = sts[c.C_P_SLIDER] 
            print(sts[c.WORK_OUT])
            sts[c.NEXT_TEST] = False

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        # translation based on http://www.interaction-design-group.de/toolbox/wp-content/uploads/2016/05/NASA-TLX.pdf
        slid.select_slider(label="Geistige Anforderungen", key=c.C_M_SLIDER, options=range(21),value=10, format_func=format_gen, on_change=enableNext, help=c.MENTAL_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Körperliche Anforderungen", key=c.C_PHY_SLIDER, options=range(21),value=10, format_func=format_gen, on_change=enableNext, help=c.PHYS_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Zeitliche Anforderungen", key=c.C_T_SLIDER, options=range(21),value=10, format_func=format_gen, on_change=enableNext, help=c.TEMP_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Leistung", key=c.C_P_SLIDER, options=range(21),value=10, format_func=format_perf, on_change=enableNext, help=c.PERF_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Anstrengung", key=c.C_E_SLIDER, options=range(21),value=10, format_func=format_gen, on_change=enableNext, help=c.EFFORT_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Frustration", key=c.C_F_SLIDER, options=range(21),value=10, format_func=format_gen, on_change=enableNext, help=c.FRUST_DESC)

        st.button(label = "Nächster Test", key = c.C_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    elif not sts[c.C_START]:
        ## Test is not started yet
        sts[c.NEXT_TEST] = True
        st.header("Klick")
        st.write(c.C_TASK_DESC, unsafe_allow_html=True)
        st.button(label="Starten", key=c.C_B_START, on_click=studyToggle, args=[True])  
        """ 
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
            st.experimental_rerun() """
    
    
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