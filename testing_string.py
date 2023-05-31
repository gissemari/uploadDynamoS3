import os
import pympi
import pandas as pd


def extract_word(string):
    separator = '_'
    words = string.split(separator)
    if len(words) < 3:
        separator = '-'
        words = string.split(separator)

    output = ""
    for word in words:
        if word != 'ORACION':
            output += word + separator  # Append the word and the separator
        else:
            break

    # Remove the trailing separator
    output = output.rstrip(separator)

    return output


def extract_substring(path):
    # Find the index of "_ORACION_" or "-ORACION"
    index = path.find("ORACION_")
    # if index == -1:
    #     index = path.find("-ORACION")

    if index != -1:
        return path[:index-1]
    else:
        return None


# Load the lemmaPUCP305.csv file
csv_path = "lemmaPUCP305.csv"
base_folder = "/home/ubuntu/repositories/datasets/PUCP_305"

df = pd.read_csv(csv_path, index_col=False)
print(df)

# Create an empty list to store the TextSentence values
text_sentences = []
error_log = []
eaf_paths = []
# Iterate over the "Path" column
for index, row in df.iterrows():

    path = row["Path"]
    print("path:", path)
    parts = path.split('/')
    glosa = parts[0]
    extracted_word = extract_substring(glosa)
    print("extracted word:", extracted_word)
    eaf_folder = extracted_word
    eaf_filename = glosa + ".eaf"
    print(f'base folder {base_folder} eaf folder {eaf_folder} eaf_filename {eaf_filename}')
    eaf_path = os.path.join(base_folder, eaf_folder, eaf_filename)
    print(eaf_path)
    checking_folder = os.path.exists(eaf_path)
    print("checking folder: ", checking_folder)
    if extracted_word is not None and checking_folder:
        # Load the ELAN file
        aEAFfile = pympi.Elan.Eaf(eaf_path)
        print(f"Examining {eaf_path}: ",aEAFfile.tiers.keys())
        # Check if the "TRADUCCION" tier exists

        if 'TRADUCCION' in aEAFfile.tiers.keys():
            annotation = aEAFfile.tiers['TRADUCCION']
        elif  'TRADUCCIÓN' in aEAFfile.tiers.keys():
            annotation = aEAFfile.tiers['TRADUCCIÓN']
        elif 'Traducción' in aEAFfile.tiers.keys():
            annotation = aEAFfile.tiers['Traducción']
        elif 'Traduccion' in aEAFfile.tiers.keys():
            annotation = aEAFfile.tiers['Traduccion']
        elif 'TRADUCION' in aEAFfile.tiers.keys():
            annotation = aEAFfile.tiers['TRADUCION']
        elif 'Traducion' in aEAFfile.tiers.keys():
            annotation = aEAFfile.tiers['Traducion']

        main_sentence = ""

        for n, key in enumerate(annotation[0]):
            sentence = annotation[0][key][2]
            print(len(annotation[0]),n, key, sentence, eaf_path)
            if len(annotation[0])<=1:
                text_sentences.append(sentence)
                eaf_paths.append(eaf_path)
            else:
                main_sentence = main_sentence + sentence
                if n==(len(annotation[0])-1):
                    text_sentences.append(main_sentence)
                    eaf_paths.append(eaf_path)
    else:
        df = df.drop(index)
        error_message = f"Error processing path: {eaf_path}"
        error_log.append(error_message)
        print(f"Dropped Df at {index}")
        print(df.shape)
    # else:
    #     raise ValueError("Substring extraction failed")
    # except Exception as e:
    #     error_message = f"Error processing path: {eaf_path} - {str(e)}"
    #     error_log.append(error_message)
    #     continue

print(df)
print(text_sentences)
# # Add the "TextSentence" column to the existing dataframe

# Create a new DataFrame to store the TextSentence values
new_df = pd.DataFrame()
new_df["TextSentence"] = text_sentences
new_df["EAFPath"] = eaf_paths

new_csv_path = "lemmaPUCP305-sentences.csv"
new_df.to_csv(new_csv_path, index=False)

df["TextSentence"] = text_sentences

# # Save the updated dataframe to a new CSV file
new_csv_path = "lemmaPUCP305-reviewed.csv"
df.to_csv(new_csv_path, index=False)



# Save the error log to a log file
log_file = "error_log.txt"
with open(log_file, "w") as f:
    f.write("\n".join(error_log))
