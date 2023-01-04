from __future__ import annotations
import pandas as pd 
import io 
from dataclasses import dataclass,field
from enum import Enum 
from functools import partial

class SupportedFileTypes(Enum):
    """Enumeration Class that displays all supported file types """
    PARQUET = "parquet"
    CSV = "csv"
    XLS = "xls"
    XLSX = "xlsx"
    XLSM = "xlsm"
        
    def get_enum_member(value:str)->SupportedFileTypes:
        """Retrieves the right enumeration member based on a string value
        if no member is found, a valueerror is thrown
        """
        for member in SupportedFileTypes.__members__.values():
            if member.value == value.lower():
                return member
        raise ValueError(f'File Type: {value!r} not supported!')
            
            
    def get_reader(value:SupportedFileTypes)->callable:
        """Helper Function that can be called with a SupportFileType to get the associated
        function that can then be called later
        """
        # all read methods are in the dictionary that its easy to call 
        supported_read_methods = {
            SupportedFileTypes.PARQUET: pd.read_parquet,
            SupportedFileTypes.CSV: partial(pd.read_csv,sep=",",encoding="utf-8",header=0),
            SupportedFileTypes.XLS: pd.read_excel,
            SupportedFileTypes.XLSX: pd.read_excel,
            SupportedFileTypes.XLSM: pd.read_excel,

        }
        
        reader = supported_read_methods.get(value,None)
        if reader is None:
            raise ValueError(f'No reader method implemented for the particular Enumeration! Please contact the developers')
        return reader
            



        
@dataclass 
class DataReader:
    """Data Class that is able to load specific files into memory as a pandas DataFrame
    the 'data' variable holds the read dataframe     

    Important Note: 
    For CSV Files we always assume that the delimiter is a comma (,). Furthermore, the encoding must be utf-8 and the header must start in the first position (position 0),
    otherwise it will throw errors or produce wrong results.
    """
    table_name:str 
    data_as_bytes:bytes = field(repr=False)


    def __post_init__(self):
        self.table_name = self.table_name.lower()
        self.data = self._read()




    def _read(self)->pd.DataFrame:
        """Helper Function that reads a dataframe from a bytes array and returns it """
        
        # two step approach, get the right enumeration and then use the get_reader method to get the right pandas datareader function 

        supported_file_enum = SupportedFileTypes.get_enum_member(self.file_type)
        reader = SupportedFileTypes.get_reader(supported_file_enum)
        
        # convert the bytes data to a file-like object that can then be called be the pandas read methods 
        data_io = io.BytesIO(self.data_as_bytes)

        return reader(data_io)
    @property
    def file_type(self)->str:
        """Returns the extracted file type derived from the name of the file"""

        return self.table_name.split(".")[-1]


