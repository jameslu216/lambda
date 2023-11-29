import csv
import json

import boto3
from numpy import genfromtxt
from botocore.exceptions import NoCredentialsError

class S3Function:
    def __init__(self) -> None:
        self.s3_resource = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        return
    
    def get_data_from_S3(self, bucket, file_path):
        print('Reading File ...' + file_path)
        file_name = file_path.split('/')[-1]
        directory = "/tmp/" + file_name
        self.s3_resource.Bucket(bucket).download_file(file_path, directory)
        return directory
    
    def get_data_json_from_S3(self, bucket, file_path):
        print('Reading File ...' + file_path)
        file_name = file_path.split('/')[-1]
        directory = "/tmp/" + file_name
        self.s3_resource.Bucket(bucket).download_file(file_path, directory)
        return directory

    def get_data_csv_from_s3(self, bucket, file_path):
        print('Reading File ...' + file_path)
        file_name = file_path.split('/')[-1]
        directory = "/tmp/" + file_name
        self.s3_resource.Bucket(bucket).download_file(file_path, directory)
        return directory


    def key_exists(self, mybucket, mykey):
        try:
            response = self.s3_client.list_objects_v2(Bucket=mybucket, Prefix=mykey)
            for obj in response["Contents"]:
                if mykey == obj["Key"]:
                    return True
            return False  # no keys match
        except KeyError:
            return False  # no keys found
        except Exception as e:
            # Handle or log other exceptions such as bucket doesn't exist
            return False
    def put_to_public_s3(self,bucket_name,local_directory,picture_name):
        try:
            # 上傳圖片到S3
            self.s3_client.upload_file(local_directory, bucket_name, picture_name)
            print("Upload Picture to S3 Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False 