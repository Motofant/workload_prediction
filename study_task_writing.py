import psutil
import streamlit as st
import constants as c
import streamlit.components.v1 as components
from streamlit import session_state as sts
from utils import startSubprocesses, manageSubProc, getFocusString,format_gen,format_perf

# creative writing task 
# let the user write a text about provideed topic

def endTest():
    # end subprocesses
    manageSubProc("kill",sub_group=c.SUB_LST)

    # write outputs in logfile
    
    with open(f'./logging/{sts[c.USER]}_{c.WRITING_KEY}user_entered.txt', "w") as f:
        f.write(sts[c.W_T_INPUT])
    
    # block access to test
    sts[c.W_END] = True

def changeTest():
    sts[c.STATE] = 7

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.WRITING_KEY,sts[c.USER],c.WRITING_KEY,sub_group=c.SUB_LST)
    sts[c.W_START] = val
    manageSubProc("resume",sub_group=c.SUB_LST)

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
            sts[c.WORK_OUT][c.W_M_SLIDER] = sts[c.W_M_SLIDER] 
            sts[c.WORK_OUT][c.W_PHY_SLIDER] = sts[c.W_PHY_SLIDER] 
            sts[c.WORK_OUT][c.W_T_SLIDER] = sts[c.W_T_SLIDER] 
            sts[c.WORK_OUT][c.W_E_SLIDER] = sts[c.W_E_SLIDER] 
            sts[c.WORK_OUT][c.W_F_SLIDER] = sts[c.W_F_SLIDER] 
            sts[c.WORK_OUT][c.W_P_SLIDER] = sts[c.W_P_SLIDER] 
            print(sts[c.WORK_OUT])
            sts[c.NEXT_TEST] = False

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        # translation based on http://www.interaction-design-group.de/toolbox/wp-content/uploads/2016/05/NASA-TLX.pdf
        slid.select_slider(label="Geistige Anforderungen", key=c.W_M_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.MENTAL_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Körperliche Anforderungen", key=c.W_PHY_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.PHYS_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Zeitliche Anforderungen", key=c.W_T_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.TEMP_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Leistung", key=c.W_P_SLIDER, options=range(22),value=21, format_func=format_perf, on_change=enableNext, help=c.PERF_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Anstrengung", key=c.W_E_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.EFFORT_DESC)
        slid.markdown("""---""")
        slid.select_slider(label="Frustration", key=c.W_F_SLIDER, options=range(22),value=21, format_func=format_gen, on_change=enableNext, help=c.FRUST_DESC)
        st.button(label = "Nächster Test", key = c.W_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    # currently running
    elif not sts[c.W_START]:
        ## Test is not started yet
        sts[c.NEXT_TEST] = True
        if c.NEXT_TEST in sts:
            del sts[c.NEXT_TEST]
        st.header("Fließtext schreiben")
        st.write(c.W_TASK_DESC, unsafe_allow_html=True)
        st.button(label="Starten", key=c.W_B_START, on_click=studyToggle, args=[True])   
    # finished --> get to next test
    else:
        _,header = st.columns([1,3])
        header.markdown("<h1>Inhalte der E-Mail",unsafe_allow_html=True)
        x,y = st.columns(2)
        x.write(c.W_M_TASK_A,unsafe_allow_html=True)
        y.write(c.W_M_TASK_B,unsafe_allow_html=True)
        st.text_area(label="Eingabe",height=400, key= c.W_T_INPUT, label_visibility="collapsed")
        components.html(getFocusString("textarea"),height=1)

        st.button(label="Beenden", key=c.W_B_END, on_click=endTest)
