import streamlit as st
from streamlit import session_state as sts 
from random import randrange
from utils import startSubprocesses, getPhrases,manageSubProc
import constants as c
import config as conf

def studyToggle(val:bool):
    sub_procs = startSubprocesses(c.PHRASE_KEY,sts[c.USER],"text", "easy")
    sts[c.P_START] = val
    manageSubProc("resume")

def phraseChange(change):
    sts[c.P_OUT][sts[c.P_CURR]] = sts[c.P_T_INPUT]
    sts[c.P_CURR] = min(max(sts[c.P_CURR]+change,0),conf.no_phrases-1)
    sts[c.P_T_INPUT] = ""

def endTest():
    # end subprocesses
    manageSubProc("kill")
    
    # write outputs in logfile
    sts[c.P_OUT] = [val if val else "__" for val in sts[c.P_OUT] ]
    with open(f'./logging/{sts[c.USER]}_{c.PHRASE_KEY}user_entered.txt', "w") as f:
        for row in sts[c.P_OUT]:
            f.write(row+"\n")
    st.balloons()
    
    # block access to test
    sts[c.P_END] = True

def changeTest():
    sts[c.STATE] = 4

def phraseWriteView():
    if sts[c.P_END]:
        st.success(c.SUCCESS)
        st.button(label = "Nächster Test", key = c.P_B_CHANGE, on_click=changeTest)
    elif not sts[c.P_START]:
        ## building streamlit components
        st.write(c.P_TASK_DESC)
        st.button(label="Start Experiment", key=c.P_B_START, on_click=studyToggle, args=[True])   
    
    else:
        ## get sentences displayed in case
        getPhrases(c.PHRASE_KEY, conf.no_phrases)
        phrases = sts[c.P_PHRASES]
        if c.P_CURR not in sts:
            sts[c.P_CURR] = 0
        
            ## Container --> everyting changable 
        phrase_cont = st.container()
        prev,pos,nxt = phrase_cont.columns([1,3,1])
        prev.button("vohergehender Eintrag",key = c.P_B_PREV, on_click = phraseChange, args=[-1],disabled=sts[c.P_CURR]<=0)
        nxt.button("nächster Eintrag",key = c.P_B_NEXT, on_click = phraseChange, args=[1],disabled=sts[c.P_CURR]>=conf.no_phrases-1)
        pos.markdown(f"{sts[c.P_CURR] + 1}/{conf.no_phrases}")
        phrase_cont.subheader(phrases[sts[c.P_CURR]])
        phrase_cont.text_input(label="schreiben", key = c.P_T_INPUT)


        st.button("Beende Test",key = c.P_B_END, on_click = endTest,)

    

