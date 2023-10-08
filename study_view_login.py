import streamlit as st
import streamlit.components.v1 as components
from streamlit import session_state as sts
from utils import getFocusString
import constants as c

def loginView():

    print("start")
    x = st.text_input(label="Name eingeben", key=c.L_T_NAME)
    components.html(getFocusString("input[type=text]"),height=150)
    if sts[c.L_T_NAME] != "":
        sts[c.USER] = x
        sts[c.STATE] = 3 if x[-1] in ["2","3"] else 2 # skip freetext when n back task  
        print(sts[c.USER])
        st.experimental_rerun()