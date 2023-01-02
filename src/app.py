"""This modules servers as app creation point, 
the create_app function takes care of the app creation and running and 
can be imported into other modules.
"""

import streamlit as st
import src.modules.ui_components.dp_form as dp_form


def create_app():
    """Creates the Streamlit Application and runs it"""
    # configure the page
    st.set_page_config("Data Product Registration", layout="wide")

    st.write("# Data Product Registration")
    st.write("## Welcome to the Data Product Registration Page")

    # get data product details

    dp_form.upload_data_product()

    # config = dp_form.register_dp_product()

    # st.write("## The Config:  ")
    # st.write(config)


if __name__ == "__main__":
    create_app()
