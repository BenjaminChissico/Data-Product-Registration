"""This modules handles the parsing to the various APIS."""
import requests
from src.modules.logic.data_product_details import DataProductDetails
import logging


logger = logging.getLogger(__name__)


def post_data_product_details(
    dp_details: DataProductDetails, endpoint_url: str
) -> None:
    """Posts the Data Product Details information to the REST-API that handles
    the data product details
    """
    # get data product details to dict
    logger.info("Pushing Data Product Details in Data Shop Store")
    data = dp_details.to_dict()
    r = requests.post(endpoint_url, json=data)
    r.raise_for_status()
    logger.info("Posting Done")


def post_data_product_data_table_details(
    dp_details: DataProductDetails, endpoint_url: str
) -> None:
    """Posts the Data Product Data Details Table Information to the REST-API that handles
    the data product details"""

    # the tables are in the data_prodcut_detail_sample_data_table object
    logger.info("Pushing Data Product Table Details in Data Shop Store")
    tables = dp_details.data_product_detail_sample_data_table
    for table in tables:
        data = table.to_dict()
        r = requests.post(endpoint_url, json=data)
        r.raise_for_status()

    logger.info("Posting Done")


def post_data_product_data_column_details(
    dp_details: DataProductDetails, endpoint_url: str
) -> None:
    """Posts the Data Product Data Details ColumnInformation to the REST-API that handles
    the data product details"""
    # the columns are in the data_rpdocut_details_sample_data_column object
    logger.info("Pushing Data Product Column Details in Data Shop Store")
    columns = dp_details.data_product_detail_sample_data_column
    for column in columns:
        data = column.to_dict()
        r = requests.post(endpoint_url, json=data)
        r.raise_for_status()

    logger.info("Posting Done")
