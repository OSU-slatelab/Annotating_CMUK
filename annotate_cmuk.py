import pandas as pd
import numpy as np
import io
import os
import regex as re
from re import split
from numpy.ma.core import append
from re import findall


def read_dirs():
    # Getting the file names of the corpus
    file_names = []
    path = "/path/to/cmu/kids/corpus/directory"
    if os.path.exists(path):
        for subdir, dire, files in os.walk(path):
            for fil in files:
                if "sph" in fil:
                    file_names.append(subdir + "/" + fil)
    dict_files = {'file_name': file_names}
    file_names_df = pd.DataFrame(dict_files)

    # Getting the sentences
    sentence_df = pd.read_csv('sentence.tbl', names=['sent_code', 'spkr_code', 'sentence'], sep='\t')
    sentence_df.drop(columns=['spkr_code'], inplace=True)

    # Getting the remarks
    point_df = pd.read_csv('point.tbl', names=['file_name', 'start', 'end', 'remarks'], sep='\t')
    point_df.drop(columns=['start', 'end'], inplace=True)
    for index, row in point_df.iterrows():
        row['remarks'] = str(row["remarks"]).replace("*", ";")
        print(row['remarks'])
        row['remarks'] = str(row["remarks"]).replace("(", ";")
    point_df = point_df.assign(remarks=point_df["remarks"].str.split(";")).explode("remarks")
    words = []
    phrases = []
    for index, row in point_df.iterrows():
        cell_name = row["remarks"]
        if re.findall(r'\".+?\"', cell_name):
            words.append(re.findall(r'\".+?\"', cell_name)[0])
            phrases.append(cell_name.replace(wrd, "").strip().split(" "))
        else:
            words.append("")
            phrases.append(cell_name)
    point_df["words"] = words
    point_df["phrases"] = phrases

    # Getting the transcripts
    transcript_df = pd.read_csv("transcrip.tbl", names=['all'], sep="\t")
    temp_files = []
    temp_transcripts = []
    for index, row in transcript_df.iterrows():
        temp_files.append(row[0])
        temp_transcripts.append(row[1:])
    transcript_df['files_names'] = temp_files
    transcript_df['transcripts'] = temp_transcripts
    transcript_df.drop(columns=['all'], inplace=True)

    return file_names_df, sentence_df, point_df, transcript_df


def map_data(file_names, sentences, remarks, transcripts):
    # Mapping sentences and remarks
    sent = []
    for index, row in remarks.iterrows():
        file_name = row["file_names"]
        sent_code = file_name[4: 7]
        sent.append(sentences[sentences['sent_code'] == sent_code].values[0][1])
    remarks["sentence"] = sent

    # Mapping transcripts and remarks
    tran = []
    for index, row in transcripts.iterrows():
        file_name = row["file_names"]
        temp_tran = transcripts[transcripts['file_names'] == file_name]['transcripts'].values[0]
        tran_list = []
        for tran_elt in temp_tran:
            if ('[' in tran_elt) | (']' in tran_elt):
                continue
            else:
                nname.append(wt)
        ss.append(" ".join(nname))

    remarks["transcripts"] = tran

    return remarks


def data2labels(data):
    # Adding labels based on remarks
    labels = []
    for index, row in data.iterrows():
        tran_list = row["transcripts"].split(" ")
        sent_list = row["sentence"].lower().split(" ")
        labels_element = []
        if row["file_names"][7] == '1':
            for sent_elt in sent_list:
                lables_element.append("correct")
        else:
            if 'repeat' in row["phrases"]:
                for sent_element in sent_list:
                    if sent_element == row["words"]:
                        labels_element.append("repeat")
                        break
                    else:
                        labels_element.append("correct")
            elif 'replacement' in row['phrases']:
                for sent_element in sent_list:
                    if sent_element == row["words"]:
                        labels_element.append("incorrect")
                        break
                    else:
                        labels_element.append("correct")
            elif 'del w' in row['phrase']:
                for sent_element in sent_list:
                    if sent_element == row["words"]:
                        labels_element.append("skip")
                        break
                    else:
                        labels_element.append("correct")
            elif 'restart' in row['phrases']:
                for sent_element in sent_list:
                    if sent_element == row["words"]:
                        labels_element.append("skip")
                        break
                    else:
                        labels_element.append("correct")
            elif ('false start' in row["phrases"]) | (' p ' in row['phrases']):
                for sent_element in sent_list:
                    if sent_element == row["words"]:
                        labels_element.append("stutter")
                        break
                    else:
                        labels_element.append("correct")
        labels.append(labels_element)
    data["labels"] = labels


if __name__ == '__main__':
    files_names, sentences, remarks, transcripts = read_dirs()
    cmu_kids_data = map_data(files_names, sentences, remarks, transcripts)
    data2labels(cmu_kids_data).to_csv('cmu_kids_labels.csv')
