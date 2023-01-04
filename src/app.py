"""This modules servers as app creation point, 
the create_app function takes care of the app creation and running and 
can be imported into other modules.
"""

import os 
import streamlit as st
import src.modules.ui_components.dp_form as dp_form
import src.modules.logic.blob_storage as bs


# only needed for local testing 
from dotenv import load_dotenv



def create_app():
    st.set_page_config(layout="wide",page_title="Data Product Ingestion")
    st.write("# Welcome :wave:")
    st.write("## Data Product Ingestion")

    # will hold all tutorial information later, either youtube video or saved movie clip in storage
    with st.expander("""New here? Watch the tutorial, then :point_down:"""):
        url = "https://www.youtube.com/watch?v=gy1B3agGNxw"
        st.video(url)


    # get all the information of the data product 
    dp_details = dp_form.data_product_form()    
    file = dp_form.upload_data_product()

    # read the content of the data product and create details 
    # afterwards push the data product to azure 

    # init azure account details 
    
    # only for local development 
    load_dotenv()

    azure_account_url = os.environ['AZURE_ACCOUNT_URL']
    azure_container_name = os.environ['DATA_PRODUCTS_CONTAINER_NAME']
    blob_handler = bs.BlobStorage(azure_account_url,azure_container_name)
    filled_dp_details = dp_form.register_product(file,dp_details,blob_handler)
    
    data  = filled_dp_details.whole_data_product_to_dict()
    st.success("Succesfully uploaded to azure & here are the details")
    

    # only for testing 
    import json 
    for dct in data:
        with open(f'./data/{dct["id"]}.JSON','w') as f:
            f.write(json.dumps(dct,indent=2))










if __name__ == "__main__":
    create_app()
