# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 19:03:52 2019

@author: Alper
"""

import pandas as pd

hackerrank_csv = pd.read_csv('eleven_labels_updated_hackerrank.csv', delimiter=',')
leetcode_csv = pd.read_csv('updated_leetcode.csv', delimiter=',', header = None)

def append_to_file(label, other_labels, question):
    txt = question.encode('utf-8')
    question_decoded = txt.decode('utf-8')
    question_decoded = str(question_decoded).strip().replace('\n', ' ')
    f=open("{}/data.txt".format(label), "a",encoding="utf-8")
    pos_line = ["__label__pos", question_decoded]
    neg_line = ["__label__neg", question_decoded]
    f.write(' '.join(pos_line) + '\n')
    for i in other_labels:
        if i != label:
           f=open("{}/data.txt".format(i), "a",encoding="utf-8")
           f.write(' '.join(neg_line) + '\n') 
 
    
def anani_dagitim(cs_question_csv):
    for index, row  in cs_question_csv.iterrows():
        question = row[2]
        labels_of_hackerrank = row[3]
        if not pd.isnull(labels_of_hackerrank) and not pd.isnull(question):
            txt = question.encode('utf-8')
            question_decoded = txt.decode('utf-8')
            question_decoded = str(question_decoded).strip().replace('\n', ' ')
            labels_of_hackerrank = labels_of_hackerrank.split(",")
            labels_of_hackerrank = [i.replace(" ", "-") for i in labels_of_hackerrank]
            labels_underscored = ["__label__{}".format(i) for i in labels_of_hackerrank]
            compact_question_line = [" ".join(labels_underscored), question_decoded]
            f=open("datafinal_leetcode.txt", "a+",encoding="utf-8")
            f.write(' '.join(compact_question_line) + '\n') 
        print(index)        
anani_dagitim(leetcode_csv)