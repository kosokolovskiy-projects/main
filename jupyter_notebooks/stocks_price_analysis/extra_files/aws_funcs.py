import boto3
import streamlit as st
import os

from botocore.exceptions import NoCredentialsError

S3_BUCKET_NAME_PROJECTS = os.environ['STREAMLIT_S3_BUCKET_NAME_PROJECTS']
AWS_ACCESS_KEY_PROJECTS = os.environ['STREAMLIT_AWS_ACCESS_KEY_PROJECTS']
AWS_SECRET_KEY_PROJECTS = os.environ['STREAMLIT_AWS_SECRET_KEY_PROJECTS']
STREAMLIT_S3_BUCKET_NAME_PROJECTS = S3_BUCKET_NAME_PROJECTS
STREAMLIT_AWS_ACCESS_KEY_PROJECTS = AWS_ACCESS_KEY_PROJECTS
STREAMLIT_AWS_SECRET_KEY_PROJECTS = AWS_SECRET_KEY_PROJECTS




def upload_to_s3(file_path, object_path):
    """
    Uploads a file to an S3 bucket.

    Args:
        file_path (str): The local file path of the file to be uploaded.
        object_path (str): The object path in the S3 bucket where the file will be stored.

    Raises:
        NoCredentialsError: If the AWS credentials are not available.

    Example:
        upload_to_s3('/path/to/local/file.csv', 's3_folder/file.csv')
    """

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_PROJECTS, aws_secret_access_key=AWS_SECRET_KEY_PROJECTS)

    try:
        s3_client.upload_file(file_path, S3_BUCKET_NAME_PROJECTS, object_path,
                # ExtraArgs={
                #     'ACL': 'public-read',
                #     # 'ContentType': 'application/octet-stream'
                #     'ContentType': 'text/csv'
                # }
        )
        print(f'File {file_path} has been uploaded to {S3_BUCKET_NAME_PROJECTS}/{object_path}')
    except NoCredentialsError:
        print('Credentials not available')


def download_from_s3(object_path, file_path):
    """
    Downloads a file from an S3 bucket.

    Args:
        object_path (str): The object path in the S3 bucket of the file to be downloaded.
        file_path (str): The local file path where the downloaded file will be saved.

    Raises:
        NoCredentialsError: If the AWS credentials are not available.
        Exception: If an error occurs during the download process.

    Example:
        download_from_s3('s3_folder/file.csv', '/path/to/local/file.csv')
    """

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_PROJECTS, aws_secret_access_key=AWS_SECRET_KEY_PROJECTS)

    try:
        file = s3_client.download_file(S3_BUCKET_NAME_PROJECTS, object_path, file_path)
        print(f'Object {object_path} has been downloaded from {S3_BUCKET_NAME_PROJECTS} to {file_path}')
    except NoCredentialsError:
        print('Credentials not available')
    except Exception as e:
        print(f'An error occurred: {e}')
    

def get_from_s3(object_path):
    """
    Retrieves an object from an S3 bucket.

    Args:
        object_path (str): The object path in the S3 bucket of the object to be retrieved.

    Returns:
        dict: The metadata and data of the retrieved object.

    Raises:
        NoCredentialsError: If the AWS credentials are not available.
        Exception: If an error occurs during the retrieval process.
    """

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_PROJECTS, aws_secret_access_key=AWS_SECRET_KEY_PROJECTS)

    try:
        return s3_client.get_object(Bucket=S3_BUCKET_NAME_PROJECTS, Key=object_path)
    except NoCredentialsError:
        print('Credentials not available')
    except Exception as e:
        print(f'An error occurred: {e}')
    return 0 


def delete_folder_from_s3(folder_path):  # sourcery skip: use-named-expression
    """
    Deletes a folder and its contents from an S3 bucket.

    Args:
        folder_path (str): The path of the folder to be deleted.

    Raises:
        NoCredentialsError: If the AWS credentials are not available.
        Exception: If an error occurs during the deletion process.
    """

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_PROJECTS, aws_secret_access_key=AWS_SECRET_KEY_PROJECTS)

    try:
        # List all objects within the folder
        objects_to_delete = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME_PROJECTS, Prefix=folder_path)
        
        # Extract object keys from the response
        object_keys = [obj['Key'] for obj in objects_to_delete.get('Contents', [])]
        
        # Delete the objects
        if object_keys:
            response = s3_client.delete_objects(
                Bucket=S3_BUCKET_NAME_PROJECTS,
                Delete={
                    'Objects': [{'Key': obj_key} for obj_key in object_keys]
                }
            )
            print(f'Deleted objects: {object_keys}')
        else:
            print(f'No objects found in folder: {folder_path}')
    except NoCredentialsError:
        print('Credentials not available')
    except Exception as e:
        print(f'An error occurred: {e}')


def delete_object_from_s3(object_key):
    """
    Deletes an object from an S3 bucket.

    Args:
        object_key (str): The key of the object to be deleted.

    Raises:
        NoCredentialsError: If the AWS credentials are not available.
        Exception: If an error occurs during the deletion process.
    """

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_PROJECTS, aws_secret_access_key=AWS_SECRET_KEY_PROJECTS)

    try:
        response = s3_client.delete_object(
            Bucket=S3_BUCKET_NAME_PROJECTS,
            Key=object_key
        )
        print(response)
        print(f'Deleted object: {object_key}')
    except NoCredentialsError:
        print('Credentials not available')
    except Exception as e:
        print(f'An error occurred: {e}')