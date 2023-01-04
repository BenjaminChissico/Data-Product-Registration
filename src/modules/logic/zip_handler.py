"""This modules handles the operations the zipfile that hold the data product information"""
from dataclasses import dataclass,field
from streamlit.runtime.uploaded_file_manager import UploadedFile
import zipfile 
import json 
from typing import Iterator



@dataclass
class ZipHandler:
    """Data Class that handles the integrity check of the data product ZipFile which is uploaded by the user and also
    handles the extraction of the items that need to be stored in the blob storage 
    """
    uploaded_file: UploadedFile = field(repr=False)
    data_product_name: str

    def __post_init__(self):
        # open file and store information 
        self.zip_file = zipfile.ZipFile(self.uploaded_file,'r')
        self.items = self.zip_file.namelist()
        if len(self.items) < 1:
            # we have an empty zipfile
            raise ValueError('The provided zipFile contains no data!')
        
        # check if the structure is okay 
        self._ensure_structural_integrity()

        self.data_product_name = self._get_dp_name()
        self.data_product_items = self._get_dp_items()
        

    

    def extract_dp_items(self)->Iterator[tuple[bytes,str]]:
        """Function provides an Iterator that provides all data items in bytes and their names including the file type"""

        for path,item_name in zip(self.items,self.data_product_items):
            yield self.zip_file.read(path),item_name




    def _get_dp_items(self)->list[str]:
        """Retrieves all data product items in the ZipFile and returns them as a list"""
        # data product items are in the last slash 
        dp_items = [item.split("/")[-1] for item in self.items]
        if len(dp_items) != len(set(dp_items)):
            #TODO: nice to have, show what items are duplicated
            raise ValueError(f'The Uploaded File contains duplicates, please make sure that no Data Product Items are duplicated')
        return dp_items


    def _get_dp_name(self)->str:
        """Retrieves the data product names from the zip_file and makes sure that only 1 data product folder is uploaded"""
        
        # namelist provides the full path to each file in the zip_file, hierarchy is indicated by a forward slash "/"
        # the data products must be the first string before the first slash "/"
        # only 1 data product is allowed to be uploaded, so we need to make sure that the first string before the first forward slash is always the same 

        possible_dps = set([dp.split("/")[0] for dp in self.items])
        if len(possible_dps) > 1:
            raise ValueError(f"Expected only one Data Product in the ZipFile, however receive {len(possible_dps):,} - the uploaded Data Products are: {possible_dps}, please make sure that you only upload 1 zipfile with 1 folder that represents the data product")
        
    def _ensure_structural_integrity(self)->None:
        """Ensures that the zipFile adheres to the schema that only 1 folder is allowed in the zip and that one folder can only contain files, no other folders
        This is checked with the forward slashes through all files in the ZipFile.
        If the ZipFile contains an object that has not exactly 1 slash, we raise an Exception
        """
        for item in self.items:
            if item.count("/") != 1:
                raise ValueError("ZipFile does not adhere to Schema, you are only allowed to Upload ZipFile that contain 1 Folder, and that 1 Folder is only allowed to contain Files")
            






