## Clicking Task

# imports
import component.streamlit_sortclick.src.st_sortclick as sc
import streamlit as st
from streamlit import session_state as sts
import constants as c
import config as conf 
from utils import startSubprocesses, manageSubProc,format_perf,format_gen
import json
from datetime import datetime as dt
import datetime

# constants
DATA={
        "Dateien aus Kalenderwoche 20":["dataKW20.txt","infoKW20.txt","info2KW20.txt",], 
        "Dateien aus Kalenderwoche 30":["dataKW30.txt","infoKW30.txt","info2KW30.txt",],
        "Dateien aus Kalenderwoche 40":["dataKW40.txt","infoKW40.txt","info2KW40.txt",],
        }

# functions
def endTest():
    # finishing up task

    # end subprocesses
    manageSubProc("kill", sub_group=c.SUB_LST)
    
    # write outputs in logfile
    with open(f'./logging/{sts[c.USER]}_{c.CLICK_KEY}user_entered.json', "w") as f:
        json.dump(sts[c.C_OUT], fp=f)
    
    # block access to test
    sts[c.C_END] = True

def changeTest():
    # change page to new test 
    sts[c.EXP_ITER] += 1

    if sts[c.EXP_ITER] >= 3:
        sts[c.STATE] = 6
    else:
        sts[c.STATE] = sts[c.ORDER_EXP][sts[c.STAGE_ITER]][sts[c.EXP_ITER]]

def studyToggle(val:bool):
    # start sensor logging when task is started
    sub_procs = startSubprocesses(c.CLICK_KEY,sts[c.USER],c.CLICK_KEY,sub_group=c.SUB_LST)
    sts[c.C_START] = val
    manageSubProc("resume",sub_group=c.SUB_LST)

def change(x):
    # save user input of task occurence 
    if not x:
        x = {}
    x["time_end"] = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    sts[c.C_OUT][sts[c.C_CURR]] = x 

    if c.C_C_INPUT in sts:
        del sts[c.C_C_INPUT]
        sts[c.C_B_NEXT] = None

    # add to counter
    sts[c.C_CURR] += 1
    if sts[c.C_CURR] >= conf.no_click:
        endTest()
    
def clickingExampleView():
    # draw task example
    # used to introduce user to type of experiment
    if "started" not in sts:
        sts["started"] = False 
        sts["init"] = True
    
    if not sts["started"]:
        # show explanation
        st.header("Beispiel: Klicken")
        st.write(c.C_TASK_DESC,unsafe_allow_html=True)
        start = st.button("Beginne Aufgabe")
        if start:
            sts["started"] = True
            st.experimental_rerun()
    else:
        # draw example task
        if sts["init"]:
            # start sensor logging
            startSubprocesses(c.CLICK_KEY,sts[c.USER],c.CLICK_KEY+"test_",sub_group=c.SUB_LST)
            manageSubProc("resume",sub_group=c.SUB_LST)
            sts["init"] = False
        
        # timer 
        if "time" not in sts:
            sts["time"] = dt.now()
        time_in_sec = conf.sec_per_example
        
        # draw new examples until 
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
            # end sensor logging
            manageSubProc("kill",sub_group=c.SUB_LST)
            # call toggle to nex example
            sts[c.STATE] = 10
            del sts["time"]
            del sts["started"]
            st.experimental_rerun()

def clickingTaskView():
    # draw task
    if sts[c.C_END]:
        # Test is completed
        
        def enableNext():
            sts[c.WORK_OUT][c.C_M_SLIDER] = sts[c.C_M_SLIDER] 
            sts[c.WORK_OUT][c.C_E_SLIDER] = sts[c.C_E_SLIDER] 
            sts[c.WORK_OUT][c.C_F_SLIDER] = sts[c.C_F_SLIDER] 
            sts[c.WORK_OUT][c.C_PHY_SLIDER] = sts[c.C_PHY_SLIDER] 
            sts[c.WORK_OUT][c.C_T_SLIDER] = sts[c.C_T_SLIDER] 
            sts[c.WORK_OUT][c.C_P_SLIDER] = sts[c.C_P_SLIDER] 
            print(sts[c.WORK_OUT])
            sts[c.NEXT_TEST] = 21 in sts[c.WORK_OUT].values()

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        
        # show Raw TLX
        # translation based on http://www.interaction-design-group.de/toolbox/wp-content/uploads/2016/05/NASA-TLX.pdf
        slid.select_slider(label="Geistige Anforderungen", key=c.C_M_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.MENTAL_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Körperliche Anforderungen", key=c.C_PHY_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.PHYS_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Zeitliche Anforderungen", key=c.C_T_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.TEMP_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Leistung", key=c.C_P_SLIDER, options=range(22),value=21, format_func=format_perf, on_change=enableNext, help=c.PERF_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Anstrengung", key=c.C_E_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.EFFORT_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Frustration", key=c.C_F_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.FRUST_DESC)

        st.button(label = "Nächster Test", key = c.C_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    elif not sts[c.C_START]:
        # Test is not started yet
        sts[c.NEXT_TEST] = True
        st.header("Klicken")
        st.write(c.C_TASK_DESC, unsafe_allow_html=True)
        st.button(label="Starten", key=c.C_B_START, on_click=studyToggle, args=[True])  
        
    else:
        # task ongoing 
        if c.C_CURR not in sts:
            sts[c.C_CURR] = 0
        drag_cont = st.empty()
        _,pos,nxt = drag_cont.columns([1,3,1])

        pos.markdown(f"<center><p style= 'font-size:20px'>{sts[c.C_CURR] + 1}/{conf.no_click}", unsafe_allow_html=True)
        if c.C_C_INPUT in sts:
            del sts[c.C_C_INPUT]

        # create custom component 
        x = {}
        x = sc.st_sortclick(DATA,key = c.C_C_INPUT+str(sts[c.C_CURR]), height=.8)
        button_ack = sum([len(v) > 1 for z, v in x.items() ])<1 if x else False # activate button when component is updated first
        y=nxt.button("Weiter", on_click = change,args=[x],disabled=button_ack) 
        if y:
            st.experimental_rerun()