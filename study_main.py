import streamlit as st
from study_writing_task import textWriteView
from study_login import loginView

MAIN_KEY = "main_"
USER_KEY = "user"
st.set_page_config(layout="wide")

    

if MAIN_KEY+USER_KEY not in st.session_state:
    print("UserKey undefined")
    st.session_state[MAIN_KEY+USER_KEY] = ""

if st.session_state[MAIN_KEY+USER_KEY] == "":
    loginView()
    print(st.session_state[MAIN_KEY+USER_KEY])
    
else:
    textWriteView()

