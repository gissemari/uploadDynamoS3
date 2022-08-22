import csv
import pandas as pd
import os
import argparse
import spacy
from spacy.lang.es.examples import sentences 

'''
parser = argparse.ArgumentParser(description='Obtaining Lemmas')
parser.add_argument('--srtPath', type=str, default='./../Data/PUCP_PSL_DGI156/SRT/SRT_SEGMENTED_SIGN/', help='Path where the original SRT is located')
args = parser.parse_args()
path = argparse.srtPath
'''

#path = "C:/Users/Gissella_BejaranoNic/Documents/PeruvianSignLanguage/Data/AEC/Videos/SEGMENTED_SIGN"
path ="C:/Users/Gissella_BejaranoNic/Documents/PeruvianSignLanguage/Data/pucp_pkl-video-srt-descargadDRIVE/PUCP_PSL_DGI156/Videos/SEGMENTED_SIGN_ADJUSTED"


# Check
# Building the ASL Signbank: Lemmatization Principles for ASL http://lrec-conf.org/workshops/lrec2018/W1/pdf/18048_W1.pdf


'''
# We could try with different lemma rules
es_core_news_sm
es_core_news_md
es_core_news_lg
es_dep_news_trf
'''

nlp = spacy.load("es_core_news_sm")
doc = nlp(sentences[0])
print(doc.text)

#print(token.text, token.pos_, token.dep_) # pos: verb, noun - dep: obj, advc1

# initiaizing list to collect original glosses, lemmas extracted of the glosses and paths (to select final video to upload)
glossColumn = []
pathsColumn = []
lemmaColumn = []
sameGlossLemma = []
vocab = {}
vocab2words = {}
#gloss2words = {}
# Gissella "C:\\Users\\Gissella_BejaranoNic\\Documents\\PeruvianSignLanguage\\Data\\PUCP_PSL_DGI156\\Videos\\SEGMENTED_SIGN"


# Collect all the glosses and simplified them in their lemma

for root, dirs, files in os.walk(path):

    for fileName in files:
    
        print(fileName)
        
        if fileName.endswith(".mp4"):
            # get rid of underscore with number of instance
            newFileName = fileName[:-4]
            posUnderScore = newFileName.find('_')
            # identify more than one word in a token (separated by hyphen, replacing it by blank)
            newFileName = newFileName[:posUnderScore].replace("-"," ")
            fileTokens = nlp(newFileName) # Converts a sentence in a list of words of the file name (without extension)

            # For the moment, work with the glosses that contain only one word
            if len(fileTokens)==1:
                print(fileTokens,fileTokens[0], len(fileTokens))
                gloss = fileTokens[0].text.lower()
                lemma = fileTokens[0].lemma_.lower()

                # Get the lemma of the word and add it in the vocabulary. This is to group the signs annotated as different conjugations, number and gender.

                if lemma in vocab:
                    vocab[lemma] +=1
                else:
                    vocab[lemma] = 1
                    
                if lemma == gloss:
                    sameGlossLemma.append(1)
                else:
                    sameGlossLemma.append(0)

                # Save lemma, original word, path
                lemmaColumn.append(lemma)
                glossColumn.append(gloss)
                pathsColumn.append(os.path.join(root,fileName))

            # glossses that contain more than one word would be storaged in a file for further analysis
            else:
                if fileTokens in vocab2words:
                    vocab2words[fileTokens] +=1
                else:
                    vocab2words[fileTokens] = 1
                    #gloss2words.append(fileName)

                print(fileTokens.text)


# Export an intermediate file with all isolated glosses, their lemmas and their paths
dictGloss = {"Original Raw Gloss":glossColumn ,"Lemma":lemmaColumn , "SameLemmaGloss": sameGlossLemma,"Path":pathsColumn}
df = pd.DataFrame(dictGloss)
df2words = pd.DataFrame.from_dict(vocab2words, orient='index', columns=['Frequence'])

df.to_csv("glosses.csv", encoding='utf-8')
df2words.to_csv("gloss2words.csv", encoding='utf-8')


# For each unique lemma, choose any video to represent it. It is recommended that is done after a cleaning to recognize what glosses can be mislabeled or wrongly annotated

listLemmasVideos = []
listLemmas = [] 
for lemma, freq in vocab.items():
    dfVideosOfLemma = df[df['Lemma']==lemma]
    videoPath = dfVideosOfLemma['Path'].iloc[0]
    listLemmas.append([lemma, freq, videoPath])
    #listLemmasVideos.append(videoPath)

dfLemma = pd.DataFrame(listLemmas, columns=["Lemma", "Frequence","Path"])
dfLemma.to_csv("lemma.csv", encoding='utf-8')