"""This modules handles the operations regarding the storage devices in the application.
This includes the creation or uploading of files to the REST API 
"""

from azure.storage.blob import BlobServiceClient


class BlobHandler:
    """Class that allows blob operations on already existing containers."""

    def __init__(
        self,
        account_url: str,
        container_name: str,
    ):
        self.account_url = account_url
        self.container_name = container_name

        # init blob_service_client for blob manipulation
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.account_url
        )

    def upload_files(self, file_data: list[bytes], blob_names: list[str]):
        """Uploads a file into a container under the blob_name.
        The blob_name can have slashes to indicate a folder structure.
        """

        if not isinstance(file_data, list):
            file_data = [file_data]
        if not isinstance(blob_names, list):
            blob_names = [blob_names]

        try:
            for file, blob_name in zip(file_data, blob_names):
                blob_client = self.blob_service_client.get_blob_client(
                    self.container_name, blob_name
                )
                blob_client.upload_blob(file)
            return True, "ok"
        except Exception as e:
            return False, e

    def is_dp_registered(self, dp_name: str) -> bool:
        """Checks whether a specific data product is already in the container"""
        if dp_name.lower() in [dp.lower() for dp in self.all_data_products]:
            return True
        return False

    @property
    def all_data_products(self) -> list[str]:
        """Returns a list of all data products currently present in the container"""
        blob_client = self.blob_service_client.get_container_client(self.container_name)
        blobs = blob_client.list_blobs()

        # data products are only the first string before the first "/"
        data_products = [str(blob).split("/")[0] for blob in blobs]
        data_products = set(data_products)
        data_products = list(data_products)
        return data_products
