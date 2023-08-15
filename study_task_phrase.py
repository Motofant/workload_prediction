import streamlit as st
from streamlit import session_state as sts 
from random import randrange
import random
from utils import startSubprocesses, getPhrases

PHRASE_KEY = "phrase_"
NO_PHRASE = 5 # count to make ~800 symbole
TASK_DESC = """
    Schreiben Sie die angezeigten Phrasen in das angezeigte Textfeld. 
    Haben Sie eine Phrase abgeschieben, navigieren Sie sich mit den Buttons weiterruntem zum Abschließen
"""
SUCCESS_MSG="Sie Haben den Test Überstanden"

def phraseChange(change):
    sts[f"{PHRASE_KEY}outputs"][sts[f"{PHRASE_KEY}curr"]] = sts[f'{PHRASE_KEY}user_input']
    sts[f"{PHRASE_KEY}curr"] = min(max(sts[f"{PHRASE_KEY}curr"]+change,0),NO_PHRASE-1)
    sts[f'{PHRASE_KEY}user_input'] = ""

def endTest():
    # end subprocesses

    # write outputs in logfile
    sts[f"{PHRASE_KEY}outputs"] = [val if val else "__" for val in sts[f"{PHRASE_KEY}outputs"] ]
    with open(f'./logging/{sts["main_user"]}_{PHRASE_KEY}user_entered.txt', "w") as f:
        for row in sts[f"{PHRASE_KEY}outputs"]:
            f.write(row+"\n")
    st.balloons()
    
    # block access to test
    sts[f'{PHRASE_KEY}completed'] = True

def studyToggle(val:bool):
    sts[f'{PHRASE_KEY}started'] = val

def phraseWriteView():
    if sts[f'{PHRASE_KEY}completed']:
        st.success(SUCCESS_MSG)
        
    elif not sts[f'{PHRASE_KEY}started']:
        ## building streamlit components
        st.write(TASK_DESC)
        st.button(label="Start Experiment", key=f"{PHRASE_KEY}start", on_click=studyToggle, args=[True])   
    
    else:
        ## get sentences displayed in case
        getPhrases(PHRASE_KEY, NO_PHRASE)
        phrases = sts[f'{PHRASE_KEY}phrases']
        if f"{PHRASE_KEY}curr" not in sts:
            sts[f"{PHRASE_KEY}curr"] = 0
        
            ## Container --> everyting changable 
        phrase_cont = st.container()
        prev,pos,nxt = phrase_cont.columns([1,3,1])
        prev.button("vohergehender Eintrag",key = f'{PHRASE_KEY}prev', on_click = phraseChange, args=[-1],disabled=sts[f'{PHRASE_KEY}curr']<=0)
        nxt.button("nächster Eintrag",key = f'{PHRASE_KEY}next', on_click = phraseChange, args=[1],disabled=sts[f'{PHRASE_KEY}curr']>=NO_PHRASE-1)
        pos.markdown(f"{sts[f'{PHRASE_KEY}curr'] + 1}/{NO_PHRASE}")
        phrase_cont.subheader(phrases[sts[f"{PHRASE_KEY}curr"]])
        user_input = phrase_cont.text_input(label="schreiben", key = f'{PHRASE_KEY}user_input')


        st.button("Beende Test",key = f'{PHRASE_KEY}end', on_click = endTest,)

    

