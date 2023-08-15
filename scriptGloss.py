import csv
import pandas as pd
import os
import argparse
import spacy
from spacy.lang.es.examples import sentences 
from spellchecker import SpellChecker
import time

def find_second_underscore(input_string):
    return input_string.find("_", input_string.find("_") + 1)
# parser = argparse.ArgumentParser(description='Obtaining Lemmas')
# parser.add_argument('--videoPath', type=str, default='../Datasets/PUCP_PSL_DGI305/Videos/SEGMENTED_SIGN', help='Path where segmented videos are located')
# args = parser.parse_args()
# path = argparse.videoPath
path = '../Datasets/PUCP_LSP_DGI305/Videos/SEGMENTED_SIGN'
# path = "../datasets/PUCP_PSL_DGI305/Videos/SEGMENTED_SIGN"
# Check
# Building the ASL Signbank: Lemmatization Principles for ASL http://lrec-conf.org/workshops/lrec2018/W1/pdf/18048_W1.pdf


'''
# We could try with different lemma rules
es_core_news_sm
es_core_news_md
es_core_news_lg
es_dep_news_trf
'''

#download model/vocabulary

#nlp = spacy.load("es_core_news_sm") #
nlp = spacy.load("es_dep_news_trf")
doc = nlp(sentences[0])
print(doc.text)

spell = SpellChecker()

#print(token.text, token.pos_, token.dep_) # pos: verb, noun - dep: obj, advc1

# initiaizing list to collect original glosses, lemmas extracted of the glosses and paths (to select final video to upload)
glossColumn = []
pathsColumn = []
lemmaColumn = []
sentenceColumn = []
sameGlossLemma = []
vocab = {}
vocab2words = {}
#gloss2words = {}
# Gissella "C:\\Users\\Gissella_BejaranoNic\\Documents\\PeruvianSignLanguage\\Data\\PUCP_PSL_DGI156\\Videos\\SEGMENTED_SIGN"


# Collect all the glosses and simplified them in their lemma

for root, dirs, files in os.walk(path):
    for fileName in files:
        if fileName.endswith(".mp4") and "ORACION" in os.path.basename(root):
            print()
            print("#"*10)
            print(root)
        
            print(f"filename: {fileName}")
            
            # get rid of underscore with number of instance
            newFileName = fileName[:-4]
            print(f"newFileName {newFileName}")

            # posUnderScore = newFileName.find('_')
            
            posUnderScore = find_second_underscore(newFileName)
            
            # identify more than one word in a token (separated by hyphen, replacing it by blank)
            newFileName = newFileName[:posUnderScore]
            newFileName2 = newFileName.replace("_"," ")
            print(f"newFileName before underScore {newFileName}")
            fileTokens = nlp(newFileName2.replace("-"," ")) # Converts a sentence in a list of words of the file name (without extension)
            #ABURRIDO 1
            #ABURRIDO 2
            #ABRIR CAJON 1

            print("fileTokens, fileTokens[0], len(fileTokens)")
            print(fileTokens,fileTokens[0], len(fileTokens))
            gloss = fileTokens[0].text.lower()
            lemma = fileTokens[0].lemma_
            lemma = lemma.lower()
            print(f'gloss: {gloss}')
            print(f'lemma: {lemma}')
            # fix mispelling
            #lemma = spell.correction(lemma)

            # Get the lemma of the word and add it in the vocabulary. This is to group the signs annotated as different conjugations, number and gender.

            if newFileName in vocab:
                vocab[newFileName] +=1
            else:
                vocab[newFileName] = 1
                
            if newFileName == gloss:
                sameGlossLemma.append(1)
            else:
                sameGlossLemma.append(0)

            # Save lemma, original word, path
            lemmaColumn.append(lemma)
            glossColumn.append(newFileName)
            pathsColumn.append(os.path.join(os.path.basename(root),fileName))

            # get video of the sentence
            sentenceColumn.append(os.path.basename(root)+".mp4")



# Export an intermediate file with all isolated glosses, their lemmas and their paths
dictGloss = {"Original Raw Gloss":glossColumn ,"Lemma":lemmaColumn , "SameLemmaGloss": sameGlossLemma,"Path":pathsColumn, "Sentence Video": sentenceColumn}
df = pd.DataFrame(dictGloss)
df2words = pd.DataFrame.from_dict(vocab2words, orient='index', columns=['Frequence'])

df.to_csv("glossesPUCP305.csv", encoding='utf-8')
df2words.to_csv("gloss2wordsPUCP305.csv", encoding='utf-8')


# For each unique gloss, choose any video to represent it. It is recommended that is done after a cleaning to recognize what glosses can be mislabeled or wrongly annotated


#Instead of LEMMA is GLOSS (including the two word glosses)
listLemmasVideos = []
listLemmas = [] 
for gloss, freq in vocab.items():
    dfVideosOfLemma = df[df['Original Raw Gloss']==gloss]
    lemmaReal = dfVideosOfLemma['Lemma'].iloc[0]
    videoPath = dfVideosOfLemma['Path'].iloc[0]
    sentencePath = dfVideosOfLemma['Sentence Video'].iloc[0]
    listLemmas.append([lemmaReal, gloss,freq, videoPath,sentencePath])
    #listLemmasVideos.append(videoPath)

dfLemma = pd.DataFrame(listLemmas, columns=["Sign","GlossVar", "Frequence","Path","SentencePath"])
dfLemma.to_csv("lemmaPUCP305_v3.csv", encoding='utf-8')