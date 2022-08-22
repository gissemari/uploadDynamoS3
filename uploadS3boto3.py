import boto3
from botocore.exceptions import ClientError
import io
import os
import glob
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Obtaining Lemmas')
#parser.add_argument('--accessKey', type=str, default='', help='AWS Access key. Generate one')
#parser.add_argument('--accessSecretKey', type=str, default='', help='AWS Access Secret key. Generate one')
parser.add_argument('--path', type=str, default="C:/Users/Gissella_BejaranoNic/Documents/PeruvianSignLanguage/Data/testS3", help='Path from which to take files to uploda')

args = parser.parse_args()


# fie with unique lemmas with a selected video file (from all the instances)
dfLemmas = pd.read_csv("lemmaDynamo.csv", encoding='utf-8')


#s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=accessKey, aws_secret_access_key=accessSecretKey)

# AWS page
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        print(file_name, object_name)
        response = s3_client.upload_file(file_name, bucket,object_name) #, "archivo"+str(cont)
        
    except ClientError as e:
        logging.error(e)
        print(e)
        return False
    return True

# tutorial    
def upload_my_file(bucket, folder, file_as_binary, file_name):
        file_as_binary = io.BytesIO(file_as_binary)
        key = folder+"/"+file_name
        try:
            s3_client.upload_fileobj(file_as_binary, bucket, key)
        except ClientError as e:
            print(e)
            return False
        return True

bucket = 'isolatedsigns'

#for fileName in os.listdir(path):
# uploading from folder directly
'''
for fileName in glob.glob(path):# files:
        newName = os.path.abspath(fileName)
        print(fileName)
        print(newName)
        object_name = os.path.basename(fileName)
        print(object_name)
        print(os.path.basename(newName))
        
        #get file as binary
        #file_binary = open(newName, "rb").read()
        #uploading file
        upload_file(newName,bucket, cont,object_name)
        #upload_my_file("bucket-name", "folder-name", file_binary, "test.html")
'''
        
#uploading from csv
#[print(LemmaPath,bucket,lemma) for (lemma, LemmaPath) in dfLemmas[["Lemma", "Path"]].values]

[upload_file(LemmaPath,bucket,lemma) for (lemma, LemmaPath) in dfLemmas[["Lemma", "Path"]].values]