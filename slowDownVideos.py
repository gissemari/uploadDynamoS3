import boto3
from botocore.exceptions import ClientError
import io
import os
import glob
import argparse
import pandas as pd

# path = "C:/Users/Gissella_BejaranoNic/Documents/SignLanguage/Upload AWS S3/AWS/PUCP-DGI305-JOE/Videos"
path = "../datasets/PUCP_PSL_DGI305/Videos"
# dfLemmas = pd.read_csv("lemmaPUCP305-reviewed.csv", encoding='utf-8')

dfLemmas = pd.read_csv("lemmaPUCP305-reviewed.csv", encoding='utf-8')
shFile = 'slowDownVideos305.sh'

# Write command ffmpeg for each video
#LemmaPath.replace('\\','/')
listFFcommands = ['ffmpeg -i "'+os.path.join(path,"SEGMENTED_SIGN",LemmaPath).replace('\\','/')+'" -filter:v "setpts=2.5*PTS" '+ 'videosSlowed305/'+gloss+'.mp4' for (gloss, LemmaPath) in dfLemmas[["GlossVar", "Path"]].values]
print("TOTAL VIDEOS: ", len(listFFcommands))


sh_header = '''#!/bin/bash

function show_time() {
  SECONDS_NOW=$(date +%s)
  PROCESSING_TIME=$((SECONDS_NOW - START_TIME))
  REMAINING_TIME=$((PROCESSING_TIME * (TOTAL_VIDEOS - VIDEO_COUNT) / VIDEO_COUNT))
  echo "Processing Time: $PROCESSING_TIME seconds"
  echo "Remaining Time: $REMAINING_TIME seconds"
}

START_TIME=$(date +%s)
TOTAL_VIDEOS={}
VIDEO_COUNT=0

'''.format(len(listFFcommands))


with open(shFile, 'w') as f:
    f.write(sh_header)
    f.write('\n')
    for line in listFFcommands:
        f.write(line)
        f.write('\n')
        
        
# Write commands for aws cli update dynamodb item for each video uploaded to S3

#listFFcommands = ['ffmpeg -i '+LemmaPath.replace('\\','/')+' -filter:v "setpts=2.5*PTS" '+ 'videosSlowed/'+lemma+'.mp4' for (lemma, LemmaPath) in dfLemmas[["Lemma", "Path"]].values]