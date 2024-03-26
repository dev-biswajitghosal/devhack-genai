# Import the necessary libraries
from datetime import datetime

import boto3
import os
# Import other modules of project directory
from dotenv import load_dotenv

load_dotenv()

# Load the environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("S3_BUCKET_NAME")

# Create a client object for S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


def download_files_from_s3(directory):
    files = []
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            key = obj['Key']
            local_path = os.path.join(directory, key)
            s3.download_file(bucket_name, key, local_path)
            files.append(local_path)  # Append local path instead of URL
        return files
    except Exception as e:
        print(f"Error: {e}")


def get_file_from_s3(prefix):
    prefix = f"archive/{prefix}"
    try:
        files = []
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        for obj in response.get('Contents', []):
            key = obj['Key']
            txt = s3.get_object(Bucket=bucket_name, Key=key)
            files.append(txt['Body'].read().decode('utf-8'))
        return files
    except Exception as e:
        print(f"Error: {e}")
        return False


def upload_file_to_s3(data, category, industry, state):
    try:
        key = f"archive/{category}/{(datetime.now())}.json"
        #     upload data as a file to S3 bucket
        formatted_data = {
            "response": data,
            "industry": industry,
            "state": state,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        s3.put_object(Bucket=bucket_name, Key=key, Body=str(formatted_data))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

