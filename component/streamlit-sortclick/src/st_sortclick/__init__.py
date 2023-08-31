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
    key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        values = values,
        key=key,
    )

    return component_value


def main():
    st.set_page_config(layout="wide")
    st.write("## Example")
    value = st_sortclick(values=["a","b","c","d","e","f","g","h",])

    st.write(value)


if __name__ == "__main__":
    main()
