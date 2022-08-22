import boto3
from botocore.exceptions import ClientError
import io
import os
import glob
import argparse
import pandas as pd


dfLemmas = pd.read_csv("lemmaTestDynamo.csv", encoding='utf-8')

# Write command ffmpeg for each video
listFFcommands = ['ffmpeg -i '+LemmaPath.replace('\\','/')+' -filter:v "setpts=2.5*PTS" '+ 'videosSlowed/'+lemma+'.mp4' for (lemma, LemmaPath) in dfLemmas[["Lemma", "Path"]].values]

with open('slowDownVideos.sh', 'w') as f:
    for line in listFFcommands:
        f.write(line)
        f.write('\n')
        
        
# Write commands for aws cli update dynamodb item for each video uploaded to S3

#listFFcommands = ['ffmpeg -i '+LemmaPath.replace('\\','/')+' -filter:v "setpts=2.5*PTS" '+ 'videosSlowed/'+lemma+'.mp4' for (lemma, LemmaPath) in dfLemmas[["Lemma", "Path"]].values]