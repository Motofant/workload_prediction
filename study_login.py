import streamlit as st
import subprocess
import psutil
MAIN_KEY = "main_"
USER_KEY = "user"

def loginView():
    print("start")
    x = st.text_input(label="Name eingeben" )
    if x != "":
        st.session_state[MAIN_KEY+USER_KEY] = x
        print(st.session_state[MAIN_KEY+USER_KEY])
        st.experimental_rerun()