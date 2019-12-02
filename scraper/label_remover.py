# Load the Pandas libraries with alias 'pd'
import pandas as pd
import os
# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
df = pd.read_csv('leetcode_dataset.csv', header=None)
df.columns = ['question_name','level','question', 'labels','path']
df_new = pd.DataFrame(columns=['question_name','level','question', 'label','path'])
df = df.dropna(subset = ['labels'])
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
    labels = row['labels'].split(',')
    for l in labels:
        if l not in label_list:
            label_list.append(l)
label_dict = { i : 0 for i in label_list}
for index, row in df.iterrows():
    labels = row['labels'].split(',')
    for l in labels:
        label_dict[l]+=1

for index, row in df.iterrows():
    labels = row['labels'].split(',')
    to_be_added_labels = []
    for l in labels:
        if label_dict[l] > 10:
            to_be_added_labels.append(l)

    if len(to_be_added_labels) > 0:
        df_new =  df_new.append({'question_name': row['question_name'], 'level': row['level'],
                             'question': row['question'], 'label': ','.join(to_be_added_labels), 'path': row['path']}, ignore_index=True)

df_new.to_csv('updated_leetcode.csv',  encoding='utf-8', index=False, header=False, sep=',')

print(label_list)