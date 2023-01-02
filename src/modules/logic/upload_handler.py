"""This modules contains all functionality for the upload to work as intended"""
import zipfile
import io
from src.modules.logic.storage_handler import BlobHandler
from streamlit.runtime.uploaded_file_manager import UploadedFile


class DataProductUpload:
    """DataProductUpload Class that contains the uploaded information
    of the Data Product.
    """

    def __init__(
        self,
        data_product_zip_data: io.BytesIO | UploadedFile,
        account_url: str,
        container_name: str,
    ):
        """The data_product_zip_data can either be a io.BytesIO object which contains the zip file information
        or can be an UploadedFile from the streamlit runtime.
        """

        self.data_product_zip_data = data_product_zip_data
        self.account_url = account_url
        self.container_name = container_name
        # making sure the structure is okay
        self._check_general_structure()

    def _check_general_structure(self) -> bool:
        """Internal Helper Function that checks if the zip_file adheres to the"""

        # get all paths
        paths = self.data_product_item_paths

        # check if all paths contain exactly 1 "/"
        for path in paths:
            if path.count("/") != 1:
                raise DataStructureError()

        if self.is_already_registered():
            raise DataProductDuplicationError(self.data_product_name)

    def is_already_registered(self) -> bool:
        """Checks if a data product is already registered or not
        returns True if it is already and returns False if it isn't
        """

        blob_hanlder = BlobHandler(self.account_url, self.container_name)
        if blob_hanlder.is_dp_registered(self.data_product_name):
            return True
        return False

    def check_dp_in(self) -> bool:
        """checks a Data Product and its Items in."""

        # init the blob_handler
        # TODO: possible refactor is to provide the blob_handler as arg instead of init them in the function itself makes it easier
        blob_handler = BlobHandler(self.account_url, self.container_name)

        # get the zipFile data
        with zipfile.ZipFile(self.data_product_zip_data, "r") as zip_:
            items = zip_.namelist()
            files = [zip_.read(item) for item in items]
            check, err = blob_handler.upload_files(files, items)
            if not check:
                raise err
        return True

    @property
    def data_product_item_paths(self) -> list[str]:
        """Returns a list of all objects/items in the zipfile with their full path"""
        with zipfile.ZipFile(self.data_product_zip_data, "r") as zip_:
            return zip_.namelist()

    @property
    def data_product_name(self) -> str:
        """Returns the name of the root folder in the zip file (the root folder's name is the name of the
        data product)"""
        with zipfile.ZipFile(self.data_product_zip_data, "r") as zip_:
            name = zip_.namelist()[0].split("/")[0]
            return name

    @property
    def data_product_items(self) -> list[str]:
        """Provides all data product items in the zip folder"""

        # get all data product paths
        paths = self.data_product_item_paths

        # reduce to only the names
        names = list(map(lambda x: x.split("/")[-1], paths))
        return names


class DataProductDuplicationError(Exception):
    """Custom Expection Class that is thrown if the uploaded zipfile's data product name is already
    in the database
    """

    def __init__(self, name: str):
        msg = f"Data Product {name!r} is already registered"
        super().__init__(msg)


class DataStructureError(Exception):
    """Custom Expection Class that is thrown if the uploaded zipFile doesn't adhere to the
    structure requried
    """

    def __init__(
        self,
    ):
        msg = """The uploaded Zipfile contains one or multiple items that do not adhere to the strucutre!
            """
        super().__init__(msg)
