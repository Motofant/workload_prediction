import streamlit as st
from streamlit import session_state as sts 
import streamlit.components.v1 as components
from utils import startSubprocesses, getPhrases,manageSubProc,getFocusString
import constants as c
import config as conf
from datetime import datetime as dt
import datetime
PHRASE_PATH = 'volume/phrases.txt'
EXAMPLE_PATH = 'volume/example_phrases.txt'
def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.PHRASE_KEY,sts[c.USER],c.PHRASE_KEY,sub_group=c.SUB_LST)
    sts[c.P_START] = val
    manageSubProc("resume",sub_group=c.SUB_LST)

def phraseChange(change):
    sts[c.P_OUT][sts[c.P_CURR]] = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f,') + sts[c.P_T_INPUT]
    if sts[c.P_CURR] == conf.no_phrases-1:
        endTest()
    sts[c.P_CURR] = min(max(sts[c.P_CURR]+change,0),conf.no_phrases-1)
    sts[c.P_T_INPUT] = ""


def endTest():
    # save last value
    sts[c.P_OUT][sts[c.P_CURR]] = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f,')+sts[c.P_T_INPUT]
    # end subprocesses
    manageSubProc("kill",sub_group=c.SUB_LST)
    
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

def phraseExampleView():
    # used to introduce user to type of experiment
    if "started" not in sts:
        sts["started"] = False 
    
    if not sts["started"]:
        # read data:
        getPhrases(c.PHRASE_KEY, 30,EXAMPLE_PATH)
        sts[c.P_CURR] = 0

        # show explanation
        
        st.write("Example: Phrases",unsafe_allow_html=True)
        st.write(c.P_TASK_DESC,unsafe_allow_html=True)
        start = st.button("start example")
        
        if start:
            sts["started"] = True
            st.experimental_rerun()
    else:
        # timer 
        if "time" not in sts:
            sts["time"] = dt.now()
   
        time_in_min = 2
        phrases = sts[c.P_PHRASES]
        if dt.now() < (sts["time"] + datetime.timedelta(seconds=time_in_min)): 
            if c.C_OUT not in sts:
                sts[c.C_OUT] = {}
            if "test" not in sts:
                sts["test"] = 0
            _,pos,nxt = st.columns([1,3,1])
            pos.markdown(f"<center><p style= 'font-size:20px'>{(sts[c.P_CURR])%30 + 1}/?",unsafe_allow_html=True)
            st.markdown(f"<center><p style= 'font-size:24px'>{phrases[sts[c.P_CURR]%30]}",unsafe_allow_html=True)
            components.html(getFocusString("input[type=text]"),height=1)
            def newExample():
                print(sts["time"])
                print(dt.now())
                sts[c.P_T_INPUT] = ""
                sts[c.P_CURR] += 1
            st.text_input(label="text input", key = c.P_T_INPUT, on_change=newExample,label_visibility="collapsed")

        else:
            print(sts["time"])
            # call toggle to nex example
            sts[c.STATE] = 2
            del sts["time"]
            del sts["started"]
            del sts[f"{c.PHRASE_KEY}phrases"]
            del sts[f"{c.PHRASE_KEY}outputs"]
            #del sts[c.P_PHRASES]
            del sts[c.P_CURR]
            del sts[c.P_T_INPUT]
            st.experimental_rerun()

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
        getPhrases(site_key=c.PHRASE_KEY, n_o_phrase=conf.no_phrases, path = PHRASE_PATH)
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

    

