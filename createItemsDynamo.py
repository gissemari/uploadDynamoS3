import boto3
from botocore.exceptions import ClientError
import csv
import pandas as pd
import os
import argparse
import copy
from spacy.lang.es.examples import sentences 
import json

'''
Considering one word or two-word gloss a unique token
Creating file of gloss, lemma (first word of the token)
If more than one instance, selecting first one found
Building a file with paths of local videos of individual sign and sign in sentence.
In DynamoDB consider an iterative ID
Reviewed: echar-> cucharda, al-frente-> frente, no-saber -> desconocer
'''


# initiaizing list to collect original glosses, lemmas extracted of the glosses and paths (to select final video to upload)
listFiles = []

#gloss2words = {}
#path = "C:/Users/Gissella_BejaranoNic/Documents/SignLanguage/Upload AWS S3/videosSlowed"
#path = "C:/Users/Gissella_BejaranoNic/Documents/SignLanguage/Upload AWS S3/AWS/PUCP-DGI305-JOE/Videos"
path = "C:/Users/Gissella_BejaranoNic/Documents/SignLanguage/Upload AWS S3/videosSlowed305"
path = "..\\Datasets\\PUCP_PSL_DGI305\\Videos\\SEGMENTED_SIGN"
def writeBatchItemDynamo(listDicts):

    client = boto3.client('dynamodb')
    try:
        response = client.batch_write_item( RequestItems={"gloss": listDicts},
                                            ReturnConsumedCapacity='TOTAL',#'INDEXES'|'TOTAL'|'NONE',
                                            ReturnItemCollectionMetrics='SIZE'#'SIZE'|'NONE'
                                        )
    except ClientError as e:
        #logging.error(e)
        print(e)
        return False
    return True, response
    

'''
'N': 'string',
'B': b'bytes',
'SS': [ 'string',],
'NS': ['string',],
'BS': [b'bytes',],
'M': {'string': {'... recursive ...'}},
'L': [{'... recursive ...'},],
'NULL': True|False,
'BOOL': True|False
'''
                                                            
dictTemplate = {"PutRequest":   { "Item":   {   "sign_gloss": {"S": ""},
                                                "sign_gloss_var": {"S":""},
                                                "category": {"S": "categoria0"},
                                                "url": {"S": "s3://isolatedsigns/"},
                                                "urlSentence": {"S": "s3://sentencesigns/"},
                                                "text": {"S":""},
                                                "webname": {"S":""}
                                            }
                                }
               }


# Collect all the glosses and simplified them in their lemma

# Creating from file structure


# for root, dirs, files in os.walk(path):
#     for fileName in files:
#         dictActual = copy.deepcopy(dictTemplate)
#         newFileName = fileName[:-4]

#         # add sort key, unique gloss, includes variants

#         # putRequest does not exist
#         #dictActual[PutRequest][Item]["sign_gloss"]["S"] += newFileName
#         #dictActual[PutRequest][Item]["sign_gloss_var"]["S"] += newFileName
#         #dictActual[PutRequest][Item]["url"]["S"] += newFileName

#         dictActual["PutRequest"]["Item"]["test-sign_gloss"]["S"] += newFileName
#         dictActual["PutRequest"]["Item"]["test-sign_gloss_var"]["S"] += newFileName
#         dictActual["PutRequest"]["Item"]["url"]["S"] += newFileName
        
#         print(fileName, os.path.join(root,fileName))
#         listFiles.append(dictActual)


#creating dictionary from csv

dfLemmas = pd.read_csv("lemmaPUCP305-reviewed.csv", encoding='utf-8')
for index, row in dfLemmas.iterrows():
    dictActual = copy.deepcopy(dictTemplate)
    sign = row['word2search']
    gloss = row['GlossVar']#fileName[:-4]
    text = row['TextSentence']
    sentName = row['SentencePath']
    webname = row['Webname']

    # add sort key, unique gloss, includes variants

    # putRequest does not exist
    #dictActual[PutRequest][Item]["sign_gloss"]["S"] += newFileName
    #dictActual[PutRequest][Item]["sign_gloss_var"]["S"] += newFileName
    #dictActual[PutRequest][Item]["url"]["S"] += newFileName

    dictActual["PutRequest"]["Item"]["sign_gloss"]["S"] += sign
    dictActual["PutRequest"]["Item"]["sign_gloss_var"]["S"] += gloss
    dictActual["PutRequest"]["Item"]["url"]["S"] += gloss + '.mp4'
    dictActual["PutRequest"]["Item"]["urlSentence"]["S"] += sentName
    dictActual["PutRequest"]["Item"]["text"]["S"] += text
    dictActual["PutRequest"]["Item"]["webname"]["S"] += webname
    listFiles.append(dictActual)


print(len(listFiles),listFiles[:25])

# Split the listFiles into batches of 25 elements
batch_size = 25
num_batches = (len(listFiles) + batch_size - 1) // batch_size
print(f'Num of batches {num_batches}')
for i in range(num_batches):
    start_index = i * batch_size
    end_index = (i + 1) * batch_size
    batch_items = listFiles[start_index:end_index]

    todoOk, resp = writeBatchItemDynamo(batch_items)
    print(todoOk, resp)

# # Write the remaining elements (less than 25) as a separate batch
# remaining_items = listFiles[num_batches * batch_size:]
# if remaining_items:
#     todoOk, resp = writeBatchItemDynamo(remaining_items)
#     print(todoOk, resp)

