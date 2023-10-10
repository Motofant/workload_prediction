from streamlit import session_state as sts
# Session states variables
MAINKEY = "main_"
USER = MAINKEY+"user"
STATE = MAINKEY+"state"
M_R_TESTS = MAINKEY+"tests"

### Focus
FOCUS_SUP = "focus"

### subprocesses 
SUB_KM = "key_mouse"
SUB_AN = "analog"
SUB_EY = "eyetr"
SUB_LST = "sub_list"

### Login
LOGINKEY = "login_"
L_T_NAME = LOGINKEY+"text"

### Default
DEFKEY = "default_"
DEF_MSG_START = "lets start"
DEF_MSG_END = "Vielen Dank für die Teilnahme."

### Writing
WRITING_KEY = "writing_"
W_ACTIVE = WRITING_KEY + "active"
W_START = WRITING_KEY + "started"
W_END = WRITING_KEY + "completed"
# Buttons
W_B_START = WRITING_KEY + "start"
W_B_END = WRITING_KEY + "end"
W_B_CHANGE = WRITING_KEY+"change"
# Text Inputs
W_T_INPUT = WRITING_KEY + "user_input"
# Text
W_TASK_DESC ="""
    <p style= "font-size:20px">In der folgenden Aufgaben schreiben eine Email an einem Kollegen.\n
    <p style= "font-size:20px">Beachten Sie dabei die Aufgaben, die über dem Textfeld angezeigt werden.\n
    <p style= "font-size:20px">Schließen Sie den Test mit einem Klick auf 'Beenden' ab.
"""
W_M_TASK_A = """
- Anschrift an Empfänger: (Herr Müller)
- Absage der monatlichen Besprechung 
- Absagegrund: (Teilnahme an einem Experiment zum Thema verhalten am Arbeitsplatz)
- 2 Alternativtermine 
    - nächste Woche Montag zwischen 13 und 17 Uhr 
    - nächste Woche Dienstag bis 12 Uhr
"""
W_M_TASK_B = """
- kurze Zusammenfassung des letzten Monats
    - Erster Prototyp fertiggestellt
    - Kleinere Probleme in ersten Tests festgestellt
- Frau Meier ist nicht wegen Rückfragen zu erreichen
    - Wer ist die Vertretung
- Empfänger muss einer Lieferung am Empfang abholen
- Unterschreibe mit Nutzernamen
"""
### Phrase
PHRASE_KEY = "phrase_"
P_START = PHRASE_KEY+"started"
P_OUT = PHRASE_KEY+"outputs"
P_CURR = PHRASE_KEY+"curr"
P_PHRASES = PHRASE_KEY+"phrases"
P_END = PHRASE_KEY+"completed"
# Buttons
P_B_START = PHRASE_KEY+"start"
P_B_PREV = PHRASE_KEY+"prev"
P_B_NEXT = PHRASE_KEY+"next"
P_B_END = PHRASE_KEY+"end"
P_B_CHANGE = PHRASE_KEY+"change"
# Text Inputs
P_T_INPUT = PHRASE_KEY+"user_input"
# Text
P_TASK_DESC = """
    <p style= "font-size:20px">Schreiben Sie die angezeigten englsichen Phrasen in das angezeigte Textfeld.\n
    <p style= "font-size:20px">Bestätigen Sie Ihre Eingabe mit Enter.\n
"""

### Dragging
DRAG_KEY = "dragging_"
D_START = DRAG_KEY+"started"
D_END = DRAG_KEY+"completed"
D_CURR = DRAG_KEY+"curr"
# Buttons
D_B_START = DRAG_KEY+"start"
D_B_PREV = DRAG_KEY+"prev"
D_B_NEXT = DRAG_KEY+"next"
D_B_END = DRAG_KEY+"end"
D_B_CHANGE = DRAG_KEY+"change"
# custom drag
D_D_INPUT = DRAG_KEY+"input"
D_OUT = DRAG_KEY+"outputs"
# Text
D_TASK_DESC = '''
    <p style= "font-size:20px">Verschieben Sie die Elemente in die entsprechende Box per "Drag and Drop".\n
    <p style= "font-size:20px">Bestätigen Sie Ihre Eingabe mit einem Klick auf 'Weiter'.\n
'''

### Clicking
CLICK_KEY = "clicking_"
C_START = CLICK_KEY+"started"
C_END = CLICK_KEY+"completed"
C_CURR = CLICK_KEY+"curr"
# Buttons
C_B_START = CLICK_KEY+"start"
C_B_PREV = CLICK_KEY+"prev"
C_B_NEXT = CLICK_KEY+"next"
C_B_END = CLICK_KEY+"end"
C_B_CHANGE = CLICK_KEY+"change"
# custom drag
C_C_INPUT = CLICK_KEY+"input"
C_OUT = CLICK_KEY+"outputs"
# Text
C_TASK_DESC = '''
    <p style= "font-size:20px">Verschieben Sie die Elemente in die entsprechende Box.\n
    <p style= "font-size:20px">Klicken Sie hierfür zuerst auf ein Element oben und danach auf die Zielbox.\n
    <p style= "font-size:20px">Bestätigen Sie Ihre Eingabe mit einem Klick auf 'Weiter'.\n
'''
### Generell
SUCCESS='''
Test abgeschlossen. Um fortzufahren schätzen Sie ein, wie stark Sie diese Aufgabe kognitiv belastet hat (0: sehr niedrig, 20: sehr hoch).
'''

### Cognitive Load 
MENTAL = "mental"
I_SLIDER = DEFKEY+MENTAL
W_SLIDER = WRITING_KEY+MENTAL
P_SLIDER = PHRASE_KEY+MENTAL
D_SLIDER = DRAG_KEY+MENTAL
C_SLIDER = CLICK_KEY+MENTAL

WORK_OUT = "demand_output"
NEXT_TEST = "allow_change"
