
import boto3
import os

from dotenv import load_dotenv

load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
bucket_name = 'mydevhackgenai'


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
