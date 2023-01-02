"""This modules holds all functions and components that make up the 
data product registration form
"""
import streamlit as st
import os
from dotenv import load_dotenv
from src.modules.logic.upload_handler import DataProductUpload


def upload_data_product():
    """Functions holds all streamlit components that make up the
    data product uploading part of the application.
    The uploaded format needs to adhere to the following format:
    1. Must be a .zip file!
    2. In the root of the zip file is only one folder, the name of the folder represents the name of the data product (must be identical to the provided name)
    3. The folder mentioned in 2. has only one level underneath it, the data product item level.
    4. The data product items must be in the supported file format, can cannot contain any further folders, if more folders are detected, the function will throw an excpection.

    Visualization of the zip file structure:

    |__ A ZipFile.zip
        |__ Data Product Name Folder
                Data Product Item (File)
                Data Product Item (File)
                Data Product Item (File)
                Data Product Item (File)
                Data Product Item (File)
    """

    with st.form("DPUpload"):
        zip_file = st.file_uploader(
            "Upload your Data Product as **Zip**",
            type="zip",
        )

        is_sub = st.form_submit_button("Upload your Data Product")
        if not is_sub or zip_file is None:
            # we will wait until the button is pressed
            st.stop()

    # TODO display all the items and the name of the data product for a check, and let the user decide if everything is correct or not

    # only for development -> load env variable
    load_dotenv()

    azure_account_name = os.environ["AZURE_ACCOUNT_URL"]
    azure_container_name = os.environ["DATA_PRODUCTS_CONTAINER_NAME"]

    dp_product = DataProductUpload(zip_file, azure_account_name, azure_container_name)
    dp_product.check_dp_in()

    st.balloons()
    st.success("Data Product is there ;) :smile:")


def register_dp_product():
    """Function holds all streamlit components that make up
    the registration process for a new data product.
    """
    # Tag List
    tag_list = [
        "PRODUCTION",
        "Test-Data",
        "Delta-Load",
        "Full-Load",
        "Business Logic",
        "RAW-Data",
    ]

    # Mandatory Information First
    dp_config = {}
    with st.form("ApplicationForm"):
        dp_name = st.text_input(
            "Data Product Name",
            placeholder="Name of the Data Product",
            help="""Please provide the name of the Data Product, the Name will be 
            displayed in the Data Shop and should help other users to identify easily what 
            the Data Product represents! 
            """,
        )

        data_domain = st.text_input(
            "Domain",
            placeholder="e.g., UEDH, SAS",
            help="""The domain descripes where the data is originated from.
            Furthermore, it also helps by searching, if a user wants to see all Data Products 
            of a specific domain. 
            """,
        )

        description = st.text_area(
            "Data Product Description",
            placeholder="A very detailled description of the Data Product",
            help="""The data product description helps users to identify and understand the data product faster.  
            The richer the description of the data product, the better and easier it is for users to determine if they 
            need the data from the data product.
            Make sure to provide a meaningful and informative description what your data product provides
            """,
        )
        tags = st.multiselect(
            "Tags",
            tag_list,
            help="""Tags help to descripe the data product by associating key words with the data product.  
            For example, if the data provided is 'only test data' its wise to provide the 'Test-Data' Tag.  
            So users know what to expect. On the contrary, if the data is production data, its wise to 
            provide the 'PRODUCTION' Tag to indicate the value & quality of the data product            
            """,
        )

        dp_business_owner = st.text_input(
            "Name of the Business Owner",
            placeholder="Max Mustermann",
            help="""Provide the name of the Business Owner that is responsible for the Data Product, if
            multiple Business owner are responsible, please separate them with a comma (,), .e.g,
            Max Mustermann, Jana Doe
            """,
        )
        dp_technical_owner = st.text_input(
            "Name of the Technical Owner",
            placeholder="Max Mustermann",
            help="""Provide the name of the Technical Owner that is responsible for the Data Product, if
            multiple Technical owner are responsible, please separate them with a comma (,), .e.g,
            Max Mustermann, Jana Doe
            """,
        )

        is_sub = st.form_submit_button("Submit Data Product Details")

        if not is_sub:
            # we will wait until the button is pressed
            st.stop()

    dp_config = {
        "Data Product Name": dp_name.strip(),
        "Business Owner": dp_business_owner.strip(),
        "Technical Owner": dp_technical_owner.strip(),
        "Tags": tags if tags else "",
        "Description": description.strip(),
    }
    # data product data uplaod

    st.write("## Upload Section")
    with st.expander("Show Upload Rules"):
        # Upload rules in resources later
        st.write(
            """Here you can find a detailled explanation of how the upload should look like.  
        This will include the following information:
        - a written description 
        - a visual description of the structure 
        """
        )

    return dp_config
