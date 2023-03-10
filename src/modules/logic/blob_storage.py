from azure.storage.blob import BlobServiceClient
from dataclasses import dataclass,field




@dataclass
class BlobStorage:
    """The Class handles all operations concerning uploading and checking uploads to a container """

    account_url:str = field(repr=False)
    container_name:str 


    def __post_init__(
        self
    ):
        self.blob_service_client = BlobServiceClient.from_connection_string(self.account_url)
    


    def upload_a_file(self,bytes_data:bytes,file_name:str)->None:
        """Uploads a file to a blob container"""

        blob_client = self.blob_service_client.get_blob_client(
            self.container_name,
            file_name
        )
        try:
            blob_client.upload_blob(bytes_data)
        except Exception as e:
            raise e



    def data_product_exists(self,dp_name:str)->bool:
        """Checks the blob storage if a given data product already exists
        Returns:
            True: it exists 
            False: does not exists
        """
        # get all data products 
        existing_data_products = self.data_products
        return dp_name.lower() in existing_data_products


    @property
    def data_products(self)->list[str]:
        """Returns a list of all data products currently in the blob"""

        blob_client = self.blob_service_client.get_container_client(self.container_name)
        blobs = blob_client.list_blobs()

        # data products are only the first string before the first "/"
        data_products = [str(blob.name).split("/")[0].lower() for blob in blobs]
        data_products = set(data_products)
        data_products = list(data_products)
        return data_products



    