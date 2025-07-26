from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
from config import Config

class AzureBlobStorage:
    def __init__(self):
        # Use connection string from config (recommended way)
        self.blob_service_client = BlobServiceClient.from_connection_string(
            Config.AZURE_CONNECTION_STRING
        )
        self.container_name = Config.AZURE_CONTAINER_NAME
        # Get container client
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def upload_file(self, file_obj, filename):
        """Upload a file-like object to Azure Blob Storage"""
        try:
            blob_client = self.container_client.get_blob_client(filename)
            # upload_blob can take a stream for file-like objects
            blob_client.upload_blob(file_obj, overwrite=True)
            return True
        except AzureError as e:
            print(f"Error uploading file: {e}")
            return False

    def get_file(self, filename):
        """Download a blob content as a stream (file-like object)"""
        try:
            blob_client = self.container_client.get_blob_client(filename)
            stream = blob_client.download_blob()
            return stream
        except AzureError as e:
            print(f"Error retrieving file: {e}")
            return None

























# import boto3
# from botocore.exceptions import ClientError
# from config import Config

# class S3Storage:
#     def __init__(self):
#         self.s3 = boto3.client(
#             's3',
#             aws_access_key_id=Config.AWS_ACCESS_KEY,
#             aws_secret_access_key=Config.AWS_SECRET_KEY
#         )
#         self.bucket = Config.AWS_BUCKET_NAME

#     def upload_file(self, file_obj, filename):
#         try:
#             self.s3.upload_fileobj(file_obj, self.bucket, filename)
#             return True
#         except ClientError as e:
#             print(f"Error uploading file: {e}")
#             return False

#     def get_file(self, filename):
#         try:
#             response = self.s3.get_object(Bucket=self.bucket, Key=filename)
#             return response['Body']
#         except ClientError as e:
#             print(f"Error retrieving file: {e}")
#             return None