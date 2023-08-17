import component.streamlit_dragndrop.src.st_dragndrop as dnd
import streamlit as st
from streamlit import session_state as sts

DRAG_KEY = "dragging_"
NO_PHRASE = 5
SUCCESS_MSG="Sie Haben den Test Überstanden"
TASK_DESC = '''
    Bringen sie die Symbole in die richtige Reihenfolge
    Mit dem Drücken von "Beenden" schließen Sie den Text ab
'''
def endTest():
    pass
    # end subprocesses

    # write outputs in logfile
    '''
    sts[f"{DRAG_KEY}outputs"] = [val if val else "__" for val in sts[f"{DRAG_KEY}outputs"] ]
    with open(f'./logging/{sts["main_user"]}_{DRAG_KEY}user_entered.txt', "w") as f:
        for row in sts[f"{DRAG_KEY}outputs"]:
            f.write(row+"\n")'''
    st.balloons()
    # block access to test
    sts[f'{DRAG_KEY}completed'] = True


def studyToggle(val:bool):
    sts[f'{DRAG_KEY}started'] = val

def draggingTaskView():

    if sts[f'{DRAG_KEY}completed']:
        # Test is completed
        st.success(SUCCESS_MSG)
        
    elif not sts[f'{DRAG_KEY}started']:
        ## Test is not started yet --> giuve explenation
        st.write(TASK_DESC)
        st.button(label="Start Experiment", key=f"{DRAG_KEY}start", on_click=studyToggle, args=[True])   
    
    else:
    # TODO: generate index html before calling stuff 
        may = st.container()
        with may:
            dnd.st_dragndrop([9],"str")
        #st.components.v1.iframe(src = "http://localhost:8501", height=10)
        st.button("Beende Test",key = f'{DRAG_KEY}end', on_click = endTest,)