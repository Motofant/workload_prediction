import streamlit as st

WRITING_KEY = "writing_"
start = "start_button"
end = "end_button"
user_in = "user_input"
active = "experiment_input"
ELEMENT_KEYS = [
    #start,
    #user_in,
    #end,
    active,
]

def activateStudy(started):
    st.session_state[WRITING_KEY+active] = started

def initSessionState(page_key, elements):
    session_elements = {}
    for key in elements:
        full_key = page_key+key
        if full_key not in st.session_state:
            st.session_state[full_key] = False
        session_elements[key] = full_key
    
    return session_elements

def textWriteView():
    keys = initSessionState(WRITING_KEY,ELEMENT_KEYS)
    
    if not st.session_state[keys[active]]:
            
        st.write("""
             Starten sie den Test mit drücken des Buttons. 
             Wenn Sie fertig sind drücken sie Stopp
             Schreiben sie einen text in dieses Feld
    
             """)
        print(st.session_state[keys[active]])
        st.button(label="Start Experiment", key=f"{WRITING_KEY}{start}", on_click=activateStudy, args=[True])
        
    else:
        print(st.session_state["main_user"])
        st.text_input(label="Eingabe", key= f"{WRITING_KEY}{user_in}")
        st.button(label="Stop Experiment", key=f"{WRITING_KEY}{end}", on_click=activateStudy, args=[False])