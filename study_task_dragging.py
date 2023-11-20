import component.streamlit_dragndrop.src.st_dragndrop as dnd
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
from utils import startSubprocesses, manageSubProc,format_gen,format_perf
import json
from datetime import datetime as dt
import datetime

conf.no_mouse
DATA = {
    "Powerpoint(.pptx)":["a.pptx","c.pptx","b.pptx",], 
    "Rohdaten(.xlsx)":["a.xlsx","c.xlsx","b.xlsx",],
    "Textdatein(.docx)":["a.docx","c.docx","b.docx",],       
}
DATA = {
        "Dateien aus Kalenderwoche 20":["dataKW20.txt","infoKW20.txt","info2KW20.txt",], 
        "Dateien aus Kalenderwoche 30":["dataKW30.txt","infoKW30.txt","info2KW30.txt",],
        "Dateien aus Kalenderwoche 40":["dataKW40.txt","infoKW40.txt","info2KW40.txt",],
        }
def endTest():
    #pass
    # end subprocesses
    manageSubProc("kill",sub_group=c.SUB_LST)
    # write outputs in logfile
    with open(f'./logging/{sts[c.USER]}_{c.DRAG_KEY}_user_entered.json', "w") as f:
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
    sub_procs = startSubprocesses(c.DRAG_KEY,sts[c.USER],c.DRAG_KEY,sub_group=c.SUB_LST)
    sts[c.D_START] = val
    manageSubProc("resume",sub_group=c.SUB_LST)

def change(x):
    if not x:
        x = {}
    x["time_end"] = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    sts[c.D_OUT][sts[c.D_CURR]] = x #sts[c.D_D_INPUT]

    print("delete")
    #sts[c.D_B_NEXT] = None
    if c.D_D_INPUT+str(sts[c.D_CURR]) in sts:
        del sts[c.D_D_INPUT+str(sts[c.D_CURR])]

    sts[c.D_CURR] += 1

    if sts[c.D_CURR] >= conf.no_mouse:
        endTest()

def draggingExampleView():
    # used to introduce user to type of experiment
    if "started" not in sts:
        sts["started"] = False 
        sts["init"] = True
    if not sts["started"]:
        # show explanation
        st.header("Beispiel: Ziehen")
        st.write(c.D_TASK_DESC,unsafe_allow_html=True)
        start = st.button("Beginne Aufgabe")
        if start:
            sts["started"] = True
            st.experimental_rerun()
    else:
        # timer 
        if sts["init"]:
            startSubprocesses(site_key=c.DRAG_KEY+"test_",name=sts[c.USER],task=c.DRAG_KEY+"test_",sub_group=c.SUB_LST)
            manageSubProc("resume",sub_group=c.SUB_LST)
            sts["init"] = False
        if "time" not in sts:
            sts["time"] = dt.now()
        time_in_sec = conf.sec_per_example
        
        if dt.now() < (sts["time"] + datetime.timedelta(seconds=time_in_sec)): 
            if c.D_OUT not in sts:
                sts[c.D_OUT] = {}
            form = st.form(key= "hi",clear_on_submit=True)
            if "test" not in sts:
                sts["test"] = 0
            _,pos,nxt = form.columns([1,3,1])
            pos.markdown(f"<center><p style= 'font-size:20px'>1/?",unsafe_allow_html=True)
            with form:
                x = dnd.st_dragndrop({"Textdatei (.txt)":["a.txt"]},key=f"x{sts['test']}", height=.6)
            y=nxt.form_submit_button("weiter")
            if y:
                del sts[f"x{sts['test']}"]
                sts["test"] += 1
                st.experimental_rerun()
        else:
            # call toggle to nex example
            manageSubProc("kill",sub_group=c.SUB_LST)
            sts[c.STATE] = 9
            del sts["time"]
            del sts["started"]
            st.experimental_rerun()

def draggingTaskView(): 
    if sts[c.D_END]:
        # Test is completed
        # Test is completed
        def enableNext():
            sts[c.WORK_OUT][c.D_M_SLIDER] = sts[c.D_M_SLIDER] 
            sts[c.WORK_OUT][c.D_E_SLIDER] = sts[c.D_E_SLIDER] 
            sts[c.WORK_OUT][c.D_F_SLIDER] = sts[c.D_F_SLIDER] 
            sts[c.WORK_OUT][c.D_PHY_SLIDER] = sts[c.D_PHY_SLIDER] 
            sts[c.WORK_OUT][c.D_T_SLIDER] = sts[c.D_T_SLIDER] 
            sts[c.WORK_OUT][c.D_P_SLIDER] = sts[c.D_P_SLIDER] 
            print(sts[c.WORK_OUT])
            sts[c.NEXT_TEST] = 21 in sts[c.WORK_OUT].values()

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        # translation based on http://www.interaction-design-group.de/toolbox/wp-content/uploads/2016/05/NASA-TLX.pdf
        slid.select_slider(label="Geistige Anforderungen", key=c.D_M_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.MENTAL_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Körperliche Anforderungen", key=c.D_PHY_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.PHYS_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Zeitliche Anforderungen", key=c.D_T_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.TEMP_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Leistung", key=c.D_P_SLIDER, options=range(22),value=21, format_func=format_perf, on_change=enableNext, help=c.PERF_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Anstrengung", key=c.D_E_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.EFFORT_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Frustration", key=c.D_F_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.FRUST_DESC)

        st.button(label = "Nächster Test", key = c.D_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    elif not sts[c.D_START]:
        ## Test is not started yet
        sts[c.NEXT_TEST] = True
        st.header("Ziehen")
        st.write(c.D_TASK_DESC,unsafe_allow_html=True)
        st.button(label="Starten", key=c.D_B_START, on_click=studyToggle, args=[True])  
    
    else:
        if c.D_CURR not in sts:
            sts[c.D_CURR] = 0
        _,pos,nxt = st.columns([1,3,1])
        pos.markdown(f"<center><p style= 'font-size:20px'>{sts[c.D_CURR] + 1}/{conf.no_mouse}",unsafe_allow_html=True)
        x = dnd.st_dragndrop(DATA,key = c.D_D_INPUT+str(sts[c.D_CURR]),height=.8)
        button_ack = sum([len(v) > 1 for z, v in x.items() ])<1 if x else False # activate button when component is updated first
        y=nxt.button("Weiter", on_click = change,args=[x],disabled=button_ack)
        if y:
            st.experimental_rerun()