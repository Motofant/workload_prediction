from streamlit import session_state as sts
import subprocess
import psutil
import random
import sys
import constants as c
import config as conf
from pathlib import Path

PHRASE_PATH = 'volume/phrases.txt'
CONSOLE_SHOWN = subprocess.CREATE_NEW_CONSOLE if conf.sensor_console else subprocess.CREATE_NO_WINDOW

def startSubprocesses(site_key:str, name:str, task :str):
    lst_sub = []
    # start logging scripts
    # keyboard/mouse
    if f'{site_key}{c.SUB_KM}' not in sts:
        key_mouse = subprocess.Popen(f"{sys.executable} ./tracking/keyboard_mouse_tracker.py {name} {task}", shell = False,creationflags = CONSOLE_SHOWN)
        psutil.Process(key_mouse.pid).suspend()
        sts[f'{site_key}{c.SUB_KM}'] = key_mouse
        lst_sub.append(f'{site_key}{c.SUB_KM}')

    # analog
    if f'{site_key}{c.SUB_AN}' not in sts:
        analog = subprocess.Popen(f"dotnet run --project ./c_sharp/ {name} {task}", shell = False,creationflags = CONSOLE_SHOWN)
        psutil.Process(analog.pid).suspend()
        sts[f'{site_key}{c.SUB_AN}'] = analog
        lst_sub.append(f'{site_key}{c.SUB_AN}')

    # eyetracker
    if f'{site_key}{c.SUB_EY}' not in sts:
        cmd = [f"./eyeenv/Scripts/python", './tracking/eyetracking.py', {name}, {task}]
        
        eyetr = subprocess.Popen(cmd, shell = False,creationflags = CONSOLE_SHOWN)
        psutil.Process(eyetr.pid).suspend()
        sts[f'{site_key}{c.SUB_EY}'] = eyetr
        lst_sub.append(f'{site_key}{c.SUB_EY}')

    sts[c.SUB_LST] = lst_sub
    return [f'{site_key}{c.SUB_KM}',f'{site_key}{c.SUB_AN}',f'{site_key}{c.SUB_EY}',]

def manageSubProc(mode:str):
    if mode == "resume":
        for proc in sts[c.SUB_LST]:
            psutil.Process(sts[proc].pid).resume()
        
    elif mode == "suspend":
        for proc in sts[c.SUB_LST]:
            psutil.Process(sts[proc].pid).suspend()

    elif mode == "kill":
        for proc in sts[c.SUB_LST]:
            psutil.Process(sts[proc].pid).kill()
            del sts[proc]
        sts[c.SUB_LST] = []

def getPhrases(site_key:str,n_o_phrase: int):
    # phrases used from https://www.yorku.ca/mack/chi03b.pdf
    if f"{site_key}phrases" not in sts:
        all_phrases = []
        with open(PHRASE_PATH, 'r') as f:
            all_phrases = [line.strip() for line in f]

        all_ids = random.sample(population = range(len(all_phrases)), k=n_o_phrase)
        output = [all_phrases[id] for id in all_ids]
        print(f'from {len(all_phrases)} phrases have been {n_o_phrase} selected')

        # save selected phrases for later analysis
        log_path = f'./logging/{sts["main_user"]}_easy_phrases.txt' 
        with open(log_path, "w") as f:
            for i in output:
                f.write(i+"\n")
        sts[f"{site_key}phrases"] = output
        sts[f"{site_key}outputs"] = [None]*n_o_phrase

def radioFormat(x):
    vals = {
        0: "login",
        1: "start",
        2: "text",
        3: "phrase",
        4: "maus_drag",
        5: "mouse_click",
    }
    return vals[x]

def getFocusString(input_type):
    return f"""
        <script>
        var input = window.parent.document.querySelectorAll("{input_type}");
            for (var i = 0; i < input.length; ++i) {{
                input[i].focus();
            }}
    </script>
    """
def removeStreamlitElements():
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    return hide_streamlit_style
def generateIndex(lst:list, tpe:str):
    start = '''<!DOCTYPE html>
    <html lang="en">
    <style>
    '''
    style ='\n'.join(["#img_"+str(num)+'''{\n'''+'cursor: move;\npadding: 10px;\nposition: absolute;\nbackground-color: #f1f1f1;\n'+'''}''' for num,_ in enumerate(lst)])
    stuff='''\n
    </style>
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>streamlit-dragndrop</title>
        <script src="./streamlit-component-lib.js"></script>
        <script src="./main.js"></script>
        <link rel="stylesheet" href="./style.css" />
    </head>
    <body id = "bdid" style="height: 500px;">
    <div id="root"></div>
    '''
    divs = '\n'.join([f'<div id="img_{num}">{val}</div>' for num,val in enumerate(lst)])# style="position: absolute;cursor:move;"
    fct_call = '\n'.join([f'dragElement(img_{num})' for num,_ in enumerate(lst)])
    end = '''
    function dragElement(elmnt) {
      x = document.getElementById(elmnt.id)
      x.style.color = '#2196F3';
      var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
      if (document.getElementById(elmnt.id)) {
        /* if present, the header is where you move the DIV from:*/
        document.getElementById(elmnt.id).onmousedown = dragMouseDown;
      } else {
        /* otherwise, move the DIV from anywhere inside the DIV:*/
        elmnt.onmousedown = dragMouseDown;
      }
      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
      }
      function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
      }
    
      function closeDragElement() {
        /* stop moving when mouse button is released:*/
        document.onmouseup = null;
        document.onmousemove = null;
      }
    }
    </script>
    </body>
    </html>
    '''
    out_str = start +style+stuff+ divs + '<script>' + fct_call+ end
    file_dir = f"{Path(__file__).parent}/component/streamlit_dragndrop/src/st_dragndrop/frontend/index.html".replace('\\','/')
    print(file_dir)
    with open(file_dir,"w") as f:
        f.write(out_str)

    return out_str