"""This modules holds all functions and components that make up the 
data product registration form
"""
import streamlit as st
import src.modules.logic.data_reader as dr
import src.modules.logic.data_product_details as dp
from streamlit.runtime.uploaded_file_manager import UploadedFile
import src.modules.logic.zip_handler as zh
import src.modules.logic.blob_storage as bs


def data_product_form()->dp.DataProductDetails:
    """Functions asks user for all required information to register a data product.
    """
    with st.form('metadata-registration-form'):

        st.markdown("""
        <h3 align=middle> Data Product Detail Information</h3>
        Please provide all necessary information to catalogue your new Data Product and make it accessable.<br><br>""",unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<h5 align=middle>Mandatory Information</h5>",unsafe_allow_html=True)
            dp_name = st.text_input(
                'Data Product Name',placeholder="",
                help="The Name of the Data Product must match the Name of the Uploaded Folder that contains all data product items"
                )
            description = st.text_input(
                'Data Product Description',
                placeholder="",
                help="Please provide an **informative** and **short** description of what the Data Product is about."
            )
            schema_version = st.number_input(
                'Schema Version',
                min_value=1,
                help="Please Provide a **Sehma Version Number** of your Data Product to ensure up to dateness."
            )
            domain = st.text_input(
                'Data Product Domain',
                placeholder="e.g., UEDH, ODS, SAS",
                help="Please provide the data product's domain it belongs to."
            )

            data_owner = st.text_input(
                'Data Product Data Owner',
                placeholder="e.g., Max Mustermann, Jana Doe",
                help="Please provide the Name of the **Data Owner** of the data product."
            )
            language = st.multiselect(
                'Please provide the language your data contains',
                ['en','de'],
                help="Please provide the **Language** your data product is in, you can also supply multiple languages."
            )
            
            restriction_type = st.selectbox(
                'Restriction Type',
                #TODO: should be in its own file to easily update
                ['private','public'],
                help="Please provide the **Restriction Type** of your data product, to help automate access if possible."
            )

        with col2:
            st.markdown("<h5 align=middle>Optional Information</h5>",unsafe_allow_html=True)

            description_long = st.text_area(
                'Data Product Extended Description (Optional)',
                placeholder="",
                help="Please provide an **informative** and **longer** description of what the Data Product is about, in more detail."
            )
    
            tags = st.multiselect(
                'Data Product Tags',
                #TODO: Tags should be in there on file to easily update
                ['PRODUCTION','TEST-DATA','FAKE-DATA','Life'],
                help="Please provide **Tags** that help to describe your data product and make it more transparent."
            )

            technical_lead = st.text_input(
                'Data Product Technical Lead',
                placeholder="e.g., Max Mustermann, Jana Doe",
                help="Please provide the Name(s) of the **Technical Lead** of the data product."
            )
            business_owner = st.text_input(
                'Data Product Business Owner',
                placeholder="e.g., Max Mustermann, Jana Doe",
                help="Please provide the Name(s) of the **Business Owner** of the data product."
            )


        is_sub = st.form_submit_button('Submit Data Product Information')
        
        if not is_sub and  (not dp_name  or not description  or not  domain or not data_owner):
            st.stop()
        if is_sub and (not dp_name  or not description  or not  domain or not data_owner):
            st.error("Please make sure to fill-out all **mandatory information**!")
            st.stop()
    
    # create a data product details information class 

    dp_info = {
        'domain':domain,
        'description':description,
        'data_owner':data_owner,
        'language':language,
        'description_long':description_long if description_long else None,
        'business_owner':business_owner if business_owner else None,
        'technical_lead':technical_lead if technical_lead else None,
    }    
    dp_info_obj = dp.DataProductDetailsInformation(**dp_info)

    # create a Data Product Details Object that holds all necessary information 
    
    dp_details_dct = {
        'data_product_name':dp_name.strip(),
        'schema_version':schema_version,
        'data_product_details_information':dp_info_obj,
        'tags': tags
    }

    dp_details = dp.DataProductDetails(**dp_details_dct)
    return dp_details



def upload_data_product()->UploadedFile:
    """Function that create the streamlit component and logic for the zip file upload"""
    allowed_type = "zip"
    zip_file = st.file_uploader(
        'Upload the Data Product',
        type=allowed_type,
        help="Upload the ZipFile which contains the Data Product"
    )

    if zip_file is None:
        st.stop()
    
    return zip_file



def register_product(file:UploadedFile,data_product_details:dp.DataProductDetails,blob_handler)->dp.DataProductDetails:
    """Function handles the extraction of the zip data.
    It returns the data one by one to be uploaded and also be analysed for the catalog which is needed in the front-end
    """

    # will hold all tables extracted from the zipFile (including the column information)
    tables: list[dp.DataProductDetailSampleDataTable] = []
    

    # init the zip file 
    zip_file = zh.ZipHandler(file,data_product_details.data_product_name)
    

    # loop over the zip content 
    for bytes_data,file_name in zip_file.extract_dp_items():
        # get the Table & Column information for the front-end catalog 
        table = create_table_n_column_details(file_name,data_product_details,bytes_data,dr.DataReader)
        tables.append(table)
    
        # upload the data to the blob 
        # the file_name must be combined with the data product name with a forward flash to create a "folder" in the container
        file_name = f"{data_product_details.data_product_name}/{file_name}"


        upload_data(file_name,bytes_data,blob_handler)
    
    # register all tables and columns 

    data_product_details.register_product_detail_sample_data_tables(tables)
    return data_product_details

    



def upload_data(item_name:str,data:bytes,blob_handler:bs.BlobStorage)->None:
    """Uploads a item to the BlobStorage specified in the blob_handler
    the item_name must consist of the full path, including folders indicated with "/"
    """
    blob_handler.upload_a_file(data,item_name)

def create_table_n_column_details(file_name:str,data_product_details:dp.DataProductDetails,data:bytes,data_reader:dr.DataReader)->dp.DataProductDetailSampleDataTable:
    """Reads the byte code in and turns it into a Data Product Detail Sample Data Table, with Data Columns already registered"""

    data_r = data_reader(file_name,data)
    table = dp.DataProductDetailSampleDataTable(file_name,data_product_details.schema_version,data_product_details.id,data_r.data)
    return table 