# Load the Pandas libraries with alias 'pd'
import pandas as pd
import os
# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
df = pd.read_csv('hackerrank_dataset.csv')
#df.columns = ['question_name','level','question', 'labels','path']
df_new = pd.DataFrame(columns=['Title','Difficulty','Question', 'Tags'])
df = df.dropna(subset = ['Tags'])
df.reset_index(drop=True, inplace=True)
'''
label_dict = {
    'Array': 0,
    'Hash Table': 0,
    'Linked List': 0,
    'Math': 0,
    'Two Pointers': 0,
    'String': 0,
    'Sliding': 0,
    'Binary Search': 0,
    'Divide and Conquer': 0,
    'Dynamic Programming': 0,
    'Backtracking': 0,
}
'''
label_list = []
for index, row in df.iterrows():
    labels = row['Tags'].split(',')
    for l in labels:
        if l not in label_list:
            label_list.append(l)
label_dict = { i : 0 for i in label_list}
for index, row in df.iterrows():
    labels = row['Tags'].split(',')
    for l in labels:
        label_dict[l]+=1

for index, row in df.iterrows():
    labels = row['Tags'].split(',')
    to_be_added_labels = []
    for l in labels:
        if label_dict[l] > 10:
            to_be_added_labels.append(l)

    if len(to_be_added_labels) > 0:
        df_new =  df_new.append({'Title': row['Title'], 'Difficulty': row['Difficulty'],
                             'Question': row['Question'], 'Tags': ','.join(to_be_added_labels)}, ignore_index=True)

df_new.to_csv('updated_hackerrank.csv',  encoding='utf-8', index=False, sep=',')

new_label_list = []
for index, row in df_new.iterrows():
    labels = row['Tags'].split(',')
    for l in labels:
        if l not in new_label_list:
            new_label_list.append(l)
print(label_list)