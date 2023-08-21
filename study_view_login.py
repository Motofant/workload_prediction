import streamlit as st
from streamlit import session_state as sts
import constants as c

def loginView():
    print("start")
    x = st.text_input(label="Name eingeben", key=c.L_T_NAME)
    if sts[c.L_T_NAME] != "":
        sts[c.USER] = x
        sts[c.STATE] = 2
        print(sts[c.USER])
        st.experimental_rerun()