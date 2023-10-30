from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called st_sortclick,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"st_sortclick", path=str(frontend_dir)
)

# Create the python function that will be called
def st_sortclick(
    values: list,
    height: float,
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        values = values,
        comp_height = height,
        key = key,
    )

    return component_value


def main():
    st.set_page_config(layout="wide")
    st.write("## Example")
    data  ={
        "Datein aus Kalenderwoche 20":["dataKW20.txt","infoKW20.txt","info2KW20.txt",], 
        "Datein aus Kalenderwoche 30":["dataKW30.txt","infoKW30.txt","info2KW30.txt",],
        "Datein aus Kalenderwoche 40":["dataKW40.txt","infoKW40.txt","info2KW40.txt",],
        }
    value = st_sortclick(values=data,
        height=.8)

    st.write(value)


if __name__ == "__main__":
    main()
