import boto3
from botocore.exceptions import ClientError
import csv
import pandas as pd
import os
import argparse
import copy
from spacy.lang.es.examples import sentences 

import json


# initiaizing list to collect original glosses, lemmas extracted of the glosses and paths (to select final video to upload)
listFiles = []

#gloss2words = {}
path = "C:/Users/Gissella_BejaranoNic/Documents/SignLanguage/Upload AWS S3/videosSlowed"

def writeBatchItemDynamo(listDicts):

    client = boto3.client('dynamodb')
    try:
        response = client.batch_write_item( RequestItems={"sign": listDicts},
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
                                                "url": {"S": "s3://isolatedsigns/"}
                                            }
                                }
               }


# Collect all the glosses and simplified them in their lemma

for root, dirs, files in os.walk(path):
    for fileName in files:
        dictActual = copy.deepcopy(dictTemplate)
        newFileName = fileName[:-4]

        # add sort key, unique gloss, includes variants

        # putRequest does not exist
        #dictActual[PutRequest][Item]["sign_gloss"]["S"] += newFileName
        #dictActual[PutRequest][Item]["sign_gloss_var"]["S"] += newFileName
        #dictActual[PutRequest][Item]["url"]["S"] += newFileName

        dictActual["PutRequest"]["Item"]["sign_gloss"]["S"] += newFileName
        dictActual["PutRequest"]["Item"]["sign_gloss_var"]["S"] += newFileName
        dictActual["PutRequest"]["Item"]["url"]["S"] += newFileName
        
        print(fileName, os.path.join(root,fileName))
        listFiles.append(dictActual)

print(len(listFiles),listFiles)

todoOk, resp = writeBatchItemDynamo(listFiles)
print(todoOk, resp)
