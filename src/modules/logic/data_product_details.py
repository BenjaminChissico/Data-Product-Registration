from __future__ import annotations

"""This module holds the class definitions for the data product details
these classes include the data product itself, the data product tables and the data product columns 
"""
import uuid
import pandas as pd
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DataProductDetailsInformation:
    """Holds all necessary information of the data product details information key
    that is necessary to fullfill the requirements of the API"""

    domain: str
    description: str
    data_owner: str
    language: list[str]
    description_long: Optional[str] = None
    business_owner: Optional[str] = None
    technical_lead: Optional[str] = None

    def to_dict(self) -> dict[str, str | list[str]]:
        """Wrapper around the self.__dict__ method, returns all self variables of the object as dictionary"""
        return self.__dict__


@dataclass
class AccessDetails:
    """Data Class that holds all information about the access to a particular
    data product"""

    restriction_type: str
    request_mode: str
    # TODO:  nees to be figured out so hardcoded for now
    request_address: str = "TBD. LATER"

    def to_dict(self) -> dict[str, str | list[str]]:
        """Wrapper around the self.__dict__ method, returns all self variables of the object as dictionary"""
        return self.__dict__


@dataclass
class DataProductDetails:

    data_product_name: str
    schema_version: int
    access_details: AccessDetails
    data_product_details_information: DataProductDetailsInformation
    tags: Optional[list[str]] = field(default_factory=list)

    # TODO access_details & flags missing

    def __post_init__(self):
        self.id = str(uuid.uuid4())
        self.object_type = "DATA_PRODUCT_DETAILS"
        self.data_product_details_information = (
            self.data_product_details_information.to_dict()
        )

        # transform the accessdetails into a dictionary
        self.access_details = self.access_details.to_dict()

        # create the flags
        # TODO: didn't figure out how to provide the sample data, so its False for now
        # TODO: ask flo why he needs that information twice
        self.flags = {
            "has_sample_data": False,
            "access_restriciton": self.access_details["restriction_type"],
        }

        # TODO: Figure out how we can best provide this from both perspective, front-end and back-end
        # init empty sample_data list
        self.sample_data: list()

        # init dataproductdetailsampledatatable
        self.data_product_detail_sample_data_table = None

    def register_product_detail_sample_data_tables(
        self, sample_data_tables: list[DataProductDetailSampleDataTable]
    ):
        """Registers a list of data product detail sample data tables into the object"""
        self.data_product_detail_sample_data_table = sample_data_tables
        self.data_product_detail_sample_data_column = []

        # also save the columns in the data product class
        for table in self.data_product_detail_sample_data_table:
            self.data_product_detail_sample_data_column.extend(table.columns)

    def to_dict(self) -> dict[str, str | list[str]]:
        """Wrapper around the __dict__ method, returns all self variables as dictionary"""
        dp_data = {
            "id": self.id,
            "name": self.data_product_name,
            "object_type": self.object_type,
            "schema_version": self.schema_version,
            "tags": self.tags,
            "information": self.data_product_details_information,
            "flags": self.flags,
            "access_details": self.access_details,
        }
        return dp_data

    def to_json(self) -> list[str]:
        """Returns the data product details information as json string"""
        # starting with the data product
        # TODO dont forget!: the missing attributes need to be added here too!

        dp_data = self.to_dict()
        dp_json = json.dumps(dp_data, indent=2)

        return dp_json

    def whole_data_product_to_dict(self) -> list[dict[str, str | list[str]]]:
        """Returns the whole data product details, including the data product details, all tables ,and all columns as dictionary"""
        dp_data = self.to_dict()
        table_data = [
            table.to_dict() for table in self.data_product_detail_sample_data_table
        ]
        column_data = [
            column.to_dict() for column in self.data_product_detail_sample_data_column
        ]

        all_data = [dp_data] + table_data + column_data
        return all_data

    def whole_data_product_to_json(self) -> str:
        """Returns the whole data product details, including the data product details, all tables ,and all columns as json strings"""

        dp_data = self.to_dict()
        table_data = [
            table.to_dict() for table in self.data_product_detail_sample_data_table
        ]
        column_data = [
            column.to_dict() for column in self.data_product_detail_sample_data_column
        ]

        all_data = [dp_data] + table_data + column_data

        return json.dumps(all_data, indent=2)


@dataclass
class DataProductDetailSampleDataTable:
    """Class holds all information about a data product detail sample data table including the
    reference to its parent, the data product details"""

    data_table_name: str
    schema_version: int
    parent_id: str
    df: pd.DataFrame = field(repr=False)

    def __post_init__(self):
        self.object_type = "DATA_PRODUCT_SAMPLE_DATA_TABLE"
        self.id = str(uuid.uuid4())

        # init columns variable for later reference
        self.columns = self._extract_columns()

    def _extract_columns(self) -> list[DataProductDetailSampleDataColumn]:
        """Extracts the columns of the df class variable and returns them as data product detail sample data column objects"""
        sample_data_columns: list[DataProductDetailSampleDataColumn] = []
        for column in self.df_columns:
            # get the data_type information, the schema version is always 1 for now
            schema_version = 1
            parent_id = self.id
            data_type = str(self.df[column].dtype)
            if data_type == "object":
                data_type = "string"

            sample_data_columns.append(
                DataProductDetailSampleDataColumn(
                    column_name=column,
                    data_type=data_type,
                    schema_version=schema_version,
                    parent_id=parent_id,
                )
            )
        return sample_data_columns

    def get_all_registered_column_ids(self) -> list[str]:
        """Returns all the uuids of the registered columns as list"""
        return [column.id for column in self.columns]

    def to_dict(self) -> dict[str, str]:
        data = {
            "name": self.data_table_name,
            "schema_version": self.schema_version,
            "data_product_id": self.parent_id,
            "object_type": self.object_type,
            "id": self.id,
            "columns": self.get_all_registered_column_ids(),
        }
        return data

    def to_json(self) -> str:
        """Returns the data product detail sample data table information as json string"""
        data = self.to_dict()
        return json.dumps(data, indent=2)

    @property
    def df_columns(self) -> list[str]:
        """returns the columns of the df variable as list of strings"""
        return self.df.columns.tolist()


@dataclass
class DataProductDetailSampleDataColumn:
    column_name: str
    data_type: str
    schema_version: str
    parent_id: str

    def __post_init__(self):
        self.id = str(uuid.uuid4())
        self.object_type = "DATA_PRODUCT_SAMPLE_DATA_COLUMN"

        # init empty data variable, if we want to include sample data later on
        self.data = None

    def register_sample_data(self, sample_data: list[str]) -> None:
        """Registers Sample Data for the Data Product Column"""
        # TODO definitely not ready yet, will be implemented later ;)
        self.data = sample_data

    def to_dict(self) -> dict[str, str]:
        """Returns the most important variables as dictionary"""
        data = {
            "column_name": self.column_name,
            "id": self.id,
            "data_type": self.data_type,
            "schema_version": self.schema_version,
            "table_id": self.parent_id,
        }
        return data

    def to_json(self) -> str:
        """Returns the data product detail sample data column information as json string"""

        data = self.to_dict()
        # TODO Sample Data Flag needs to be added here

        data_json = json.dumps(data, indent=2)
        return data_json
