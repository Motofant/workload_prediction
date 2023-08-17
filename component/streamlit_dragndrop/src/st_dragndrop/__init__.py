from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components
import os

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
    <body id = "bdid" style="background-color: coral;height: 500px;">
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
    file_dir = f"{Path(__file__).parent}/frontend/index.html".replace('\\','/')
    print(file_dir)
    with open(file_dir,"w") as f:
        f.write(out_str)

    return out_str

frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "st_dragndrop", path=str(frontend_dir)
)
# Create the python function that will be called
def st_dragndrop(
    images: list,
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        img = images,
        key=key,
    )

    return component_value

def main():
    # get data
    data = [1,2,3]

    # generate index.html
    #generateIndex(data, "str")

    st.write("## Example")

    value = st_dragndrop(data)

    #st.write(value)


if __name__ == "__main__":
    st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    #generateIndex([1,2,3],"str")

    # Tell streamlit that there is a component called st_dragndrop,
    # and that the code to display that component is in the "frontend" folder
    
    frontend_dir = (Path(__file__).parent / "frontend").absolute()
    _component_func = components.declare_component(
        "st_dragndrop", path=str(frontend_dir)
    )
    main()
