import pytest
import io 
import pandas as pd
import src.modules.logic.data_reader as dr 


@pytest.fixture
def csv_data()->bytes:
    """Fixture that creates some csv data and returns it as byte array"""
    data = b"""a,b,c,d
    1,2,3,4
    5,6,7,8
    9,10,11,12
    """
    return data

@pytest.fixture
def excel_data()->bytes:
    """Figures that creates some excel data ans returns it as a byte array"""

    data_dct = {
        'a':[1,2,3,4,],
        'b':[6,7,8,9,],
        'c':['A','B','C','D',]
    }
    df = pd.DataFrame(data_dct)
    with io.BytesIO() as f:
        # move pointer to the beginning of the "file"
        f.seek(0)
        df.to_excel(f,index=False)
        
        # now read the data as bytes 
        data_bytes = f.getvalue()
    return data_bytes
    
def test_read_csv(csv_data):
    reader = dr.DataReader("data.csv", csv_data)
    assert isinstance(reader.data, pd.DataFrame)
    assert reader.data.shape == (3, 4)

def test_read_excel(excel_data):
    reader = dr.DataReader("data.xlsx", excel_data)
    assert isinstance(reader.data, pd.DataFrame)
    assert reader.data.shape == (4, 3)

def test_read_unsupported_file_type(excel_data):
    with pytest.raises(ValueError):
        reader = dr.DataReader("data.txt",excel_data)

def test_file_type_property(csv_data,excel_data):
    reader = dr.DataReader("data.csv", csv_data)
    assert reader.file_type == "csv"
    reader = dr.DataReader("data.xlsx", excel_data)
    assert reader.file_type == "xlsx"

def test_post_init(csv_data):
    reader = dr.DataReader("DATA.CSV", csv_data)
    assert reader.table_name == "data.csv"

def test_data_attribute(csv_data):
    reader = dr.DataReader("data.csv", csv_data)
    assert isinstance(reader.data, pd.DataFrame)
    assert reader.data.shape == (3, 4)