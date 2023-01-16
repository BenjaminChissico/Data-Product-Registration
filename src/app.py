"""This modules servers as app creation point, 
the create_app function takes care of the app creation and running and 
can be imported into other modules.
"""

import os
import streamlit as st
import src.modules.ui_components.dp_form as dp_form
import src.modules.logic.blob_storage as bs
from src.modules.logic.posts import (
    post_data_product_data_column_details,
    post_data_product_data_table_details,
    post_data_product_details,
)
from dotenv import load_dotenv
import requests
import json
import logging


# only needed for local testing
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def create_app():
    st.set_page_config(layout="wide", page_title="Data Product Ingestion")
    st.markdown(
        "<h1 align=middle>Welcome to the Data Shop Ingestion Application Very deployed</h1>",
        unsafe_allow_html=True,
    )
    # will hold all tutorial information later, either youtube video or saved movie clip in storage
    with st.expander("""New here? Watch the tutorial, then :point_down:"""):
        url = "https://www.youtube.com/watch?v=gy1B3agGNxw"
        st.video(url)

    # only for local development
    load_dotenv()

    azure_account_url = os.environ["AZURE_ACCOUNT_URL"]
    azure_container_name = os.environ["DATA_PRODUCTS_CONTAINER_NAME"]
    blob_handler = bs.BlobStorage(azure_account_url, azure_container_name)

    # get all the information of the data product
    dp_details = dp_form.data_product_form(blob_handler)
    file = dp_form.upload_data_product()

    # read the content of the data product and create details
    # afterwards push the data product to azure

    filled_dp_details = dp_form.register_product(file, dp_details, blob_handler)

    # push the data products, data product table and data product column details to the front-end database

    data_product_endpoint_url = os.environ["DATA_PRODUCT_DETAIL_ENDPOINT"]
    data_product_table_endpoint_url = os.environ["DATA_PRODUCT_TABLE_DETAIL_ENDPOINT"]
    data_product_column_endpoint_url = os.environ["DATA_PRODUCT_COLUMN_DETAIL_ENDPOINT"]

    logger.info("Data Processed")
    logger.info("Start with Posting")

    post_data_product_details(filled_dp_details, data_product_endpoint_url)
    post_data_product_data_table_details(
        filled_dp_details, data_product_table_endpoint_url
    )
    post_data_product_data_column_details(
        filled_dp_details, data_product_column_endpoint_url
    )

    # push minimal data_product inforamtion to api back-end
    admin_pw = os.environ["ADMIN_PW"]
    backend_endpoint = os.environ["CREATE_ENDPOINT_BACKEND"]
    dp_dict = dp_details.to_dict()

    data_body = {
        "name": dp_dict["name"],
        "data_owner": dp_dict["information"]["data_owner"],
        "schema_version": dp_dict["schema_version"],
        "restriction_type": dp_dict["access_details"]["restriction_type"],
        "data_product_id": dp_dict["id"],
        "password": admin_pw,
    }

    logger.info("Start Posting to Backend API")
    r = requests.post(backend_endpoint, data=data_body)
    r.raise_for_status()

    st.balloons()
    st.success("Successfully uploaded the Data Product")


if __name__ == "__main__":
    create_app()
