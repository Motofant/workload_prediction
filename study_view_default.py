import streamlit as st
from streamlit import session_state as sts
from utils import startNBack,manageSubProc
import constants as c
import pandas as pd

def defaultView():
    def nextpage(page):
        sts[c.STATE] = page
        print(sts[c.ORDER_STAGE][sts[c.STAGE_ITER]])
        if page not in [2,7] and sts[c.ORDER_STAGE][sts[c.STAGE_ITER]] != 0:
            print("gestartet")
            startNBack(name = sts[c.USER], sub_group=c.SUB_SEC)
            manageSubProc("resume",sub_group=c.SUB_SEC)
            

    # introduction to Experiment
    if sts[c.STATE] == 1:
        st.subheader(c.DEF_MSG_START)
        st.button(label="Start", on_click=nextpage, args=[8])

    # introduction to Stage
    elif sts[c.STATE] == 7:
        #st.subheader("Introduction of stage")
        st.write(
            c.SEC_TASK_DESC[
                sts[c.ORDER_STAGE]
                    [sts[c.STAGE_ITER]]], unsafe_allow_html=True)
        st.button(
            label="Start", 
            on_click=nextpage, 
            args=[
                sts[c.ORDER_EXP]
                [sts[c.STAGE_ITER]]
                [sts[c.EXP_ITER]]
                ])
        
    # Last page of experiment
    else:
        mental_demand = pd.DataFrame(data=[sts[c.WORK_OUT]])
        mental_demand.to_csv(path_or_buf=f"./logging/{sts[c.USER]}_demand.csv", index=None)
        if c.SUB_SEC in sts:   
            manageSubProc("kill", c.SUB_SEC)
            del sts[c.SUB_SEC]
        
        st.success(c.DEF_MSG_END)
        # resetting everything
        sts[c.C_START] = False
        sts[c.C_END] = False
        sts[c.C_CURR] = 0

        sts[c.P_START] = False
        sts[c.P_END] = False
        sts[c.P_CURR] = 0

        sts[c.D_START] = False
        sts[c.D_END] = False
        sts[c.D_CURR] = 0

        sts[c.STAGE_ITER] += 1
        sts[c.EXP_ITER] = 0
        sts[c.USER] = sts[c.USER][:-1] + str(sts[c.STAGE_ITER])
        print(sts[c.STAGE_ITER])
        if sts[c.STAGE_ITER]<3:
            x = st.button(
                label="nächste Stufe", 
                on_click=nextpage, 
                args=[7]
                )

            if x:
                st.experimental_rerun()