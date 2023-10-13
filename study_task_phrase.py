import streamlit as st
from streamlit import session_state as sts 
import streamlit.components.v1 as components
from utils import startSubprocesses, getPhrases,manageSubProc,getFocusString
import constants as c
import config as conf
from datetime import datetime

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.PHRASE_KEY,sts[c.USER],c.PHRASE_KEY)
    sts[c.P_START] = val
    manageSubProc("resume")

def phraseChange(change):
    sts[c.P_OUT][sts[c.P_CURR]] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f,') + sts[c.P_T_INPUT]
    if sts[c.P_CURR] == conf.no_phrases-1:
        endTest()
    sts[c.P_CURR] = min(max(sts[c.P_CURR]+change,0),conf.no_phrases-1)
    sts[c.P_T_INPUT] = ""


def endTest():
    # save last value
    sts[c.P_OUT][sts[c.P_CURR]] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f,')+sts[c.P_T_INPUT]
    # end subprocesses
    manageSubProc("kill")
    
    # write outputs in logfile
    sts[c.P_OUT] = [val if val else "__" for val in sts[c.P_OUT] ]
    with open(f'./logging/{sts[c.USER]}_{c.PHRASE_KEY}user_entered.csv', "w") as f:
        for row in sts[c.P_OUT]:
            f.write(row+"\n")

    # block access to test
    sts[c.P_END] = True

def changeTest():
    sts[c.EXP_ITER] += 1

    if sts[c.EXP_ITER] >= 3:
        sts[c.STATE] = 6
    else:
        sts[c.STATE] = sts[c.ORDER_EXP][sts[c.STAGE_ITER]][sts[c.EXP_ITER]]

def phraseWriteView():
    if sts[c.P_END]:

        def enableNext():
            sts[c.WORK_OUT][c.P_SLIDER] = sts[c.P_SLIDER] 
            sts[c.NEXT_TEST] = False

        st.success(c.SUCCESS)
        slid,_ = st.columns([1,4])
        slid.slider(label= "Geistige Anforderung", key=c.P_SLIDER,min_value=0, max_value=20, on_change= enableNext)
        st.button(label = "Nächster Test", key = c.P_B_CHANGE, on_click=changeTest, disabled= sts[c.NEXT_TEST])
    elif not sts[c.P_START]:
        ## building streamlit components
        sts[c.NEXT_TEST] = True
        st.write(c.P_TASK_DESC, unsafe_allow_html=True)
        st.button(label="Starten", key=c.P_B_START, on_click=studyToggle, args=[True])   
    
    else:
        ## get sentences displayed in case
        getPhrases(c.PHRASE_KEY, conf.no_phrases)
        phrases = sts[c.P_PHRASES]
        if c.P_CURR not in sts:
            sts[c.P_CURR] = 0
        
            ## Container --> everything changable 
        phrase_cont = st.container()
        prev,pos,nxt = phrase_cont.columns([1,3,1])
        #prev.button("vohergehender Eintrag",key = c.P_B_PREV, on_click = phraseChange, args=[-1],disabled=sts[c.P_CURR]<=0)
        #nxt.button("nächster Eintrag",key = c.P_B_NEXT, on_click = phraseChange, args=[1],disabled=sts[c.P_CURR]>=conf.no_phrases-1)
        pos.markdown(f"<center><p style= 'font-size:20px'>{sts[c.P_CURR] + 1}/{conf.no_phrases}",unsafe_allow_html=True)
        phrase_cont.markdown(f"<center><p style= 'font-size:24px'>{phrases[sts[c.P_CURR]]}",unsafe_allow_html=True)
        components.html(getFocusString("input[type=text]"),height=150)
        phrase_cont.text_input(label="text input", key = c.P_T_INPUT, on_change=phraseChange, args=[1],label_visibility="collapsed")

        #st.button("Beende Test",key = c.P_B_END, on_click = endTest,)

    

