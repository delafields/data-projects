import boto3
from botocore.exceptions import NoCredentialsError
from secret import ACCESS_KEY, SECRET_KEY

# instantiate S3
s3 = boto3.resource('s3')

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', 
                     aws_access_key_id=ACCESS_KEY,
                     aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print('Upload sucessful')
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False