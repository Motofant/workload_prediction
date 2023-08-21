import streamlit as st
from streamlit import session_state as sts
import constants as c

def defaultView():
    def nextpage():
        sts[c.STATE] = 2

    if sts[c.STATE] < 2:
        st.subheader(c.DEF_MSG_START)
        st.button(label="Start", on_click=nextpage)
    elif sts[c.STATE] > 2:
        st.success(c.DEF_MSG_END)