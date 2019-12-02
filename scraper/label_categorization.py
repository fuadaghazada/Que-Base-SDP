# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 19:03:52 2019

@author: Alper
"""

import pandas as pd
import numpy as np
import os
import csv
hackerrank_csv = pd.read_csv('hackerrank_dataset.csv', delimiter=',')
leetcode_csv = pd.read_csv('leetcode_dataset.csv', delimiter=',', header = None)
leetcode_labels = leetcode_csv[3]
hackerrank_labels = hackerrank_csv["Tags"]

def klasoru_dagittim(labels):
    import shutil
    for i in labels:
        if os.path.isdir(i):
            shutil.rmtree(i)
        os.mkdir(i)
def append_to_file(label, other_labels, question):
    txt = question.encode('utf-8')
    #question_decoded = txt.decode('utf-8')
    f=open("{}/data.txt".format(label), "a+",encoding="utf-8")
    f.write(f"__label__pos {question}\n")
    for i in other_labels:
        if i != label:
           f=open("{}/data.txt".format(i), "a+",encoding="utf-8")
           f.write(f"__label__neg {question}\n") 
 
def switcher_for_leetcode(argument):
    switcher = {
        "Binary Search Tree" : "Binary Search",
    }
    return switcher.get(argument,argument)               
                
def switcher_for_hackerrank(argument): 
    switcher = { 
        "adhoc": "ad-hoc",
        "Algorithmic Puzzle": "Algorithms",
        "binary search tree": "Binary Search",
        "Bit Manipulation": "Bit",
        "bit operations": "Bit",
        "Bitmask": "Bit",
        "Bitmasks": "Bit",
        "Bitwise Manipulation":"Bit",
        "Brute Force": "brute",
        "bruteforce": "brute",
        "Constructive" : "Constructive Algorithms",
        "CoreCS" : "Core CS",
        "data structure": "Data Structures",
        "DataStructures": "Data Structures",
        "Depth First Search": "DFS",
        "Dynamic Progamming" : "Dynamic Programming",
        "Game" : "Game Theory",
        "games" : "Game Theory",
        "Graph" : "Graph Algorithms",
        "Graph connectivity" : "Graph Algorithms",
        "Graph Construction" : "Graph Algorithms", 
        "Graph Theory" : "Graph Algorithms",
        "Graphs" : "Graph Algorithms",
        "greatest common divisor" : "gcd",
        "Hashing": "Hash",
        "Heaps" : "Heap",
        "heavy light decomposition" : "HLD",
        "implemention" : "Implementation",
        "Implementation Bugs" : "Implementation",
        "kmp" : "Knuth Morris Prat Algorithm",
        "LCM" : "Least Common Multiple",
        "looping" : "Loops",
        "Math" : "Mathematics",
        "MaxFlow" : "Max Flow",
        "Meeting in the middle" : "Meet in the Middle Algorithm",
        "Memoization and Dynamic Programming" : "Memoization",
        "nim-sum" : "Nim",
        "NP Complete problems" : "NP Complete",
        "or" : "Or Operation",
        "Prime" : "Primes",
        "prime number" : "Primes",
        "range-query" : "RangeQuery",
        "simple" : "Simple Maths",
        "sortings" : "Sorting",
        "sprague_grundy" : "Sparaj-Grundy Theory",
        "Sprague Grundy Theorm" : "Sparaj-Grundy Theory",
        "stack" : "Stacks",
        "SuffixArray" : "Suffix Array",
        "Trees" : "Tree",
        "trie" : "Tries",
        "Two pointers" : "Two Pointer",
        "veryunlikelytag2" : "veryunlikelytag",
    }
    return switcher.get(argument, argument) 

def fix_hackerrank_labels():
    r = csv.reader(open('hackerrank_dataset.csv', encoding="utf8")) # Here your csv file
    lines = list(r)
    for i in lines:
        labels_of_hackerrank = i[3].split(",")
        labels_of_hackerrank = [w.replace(w, switcher_for_hackerrank(w)) for w in labels_of_hackerrank]
        i[3] = ','.join(labels_of_hackerrank)
    writer = csv.writer(open('hackerrank_dataset.csv', 'w', encoding="utf8", newline=''))
    writer.writerows(lines)

def fix_hackerrank_labels():
    
def anani_dagitim(cs_question_csv):
    hack_labels = []
    for index, row  in cs_question_csv.iterrows():
        print(index)
        labels_of_hackerrank = row[3]
        if not pd.isnull(labels_of_hackerrank):
            labels_of_hackerrank = labels_of_hackerrank.split(",")
        
            hack_labels += [i for i in labels_of_hackerrank if i not in hack_labels]
    
    print(hack_labels)
    klasoru_dagittim(hack_labels)
    for index, row  in cs_question_csv.iterrows():
        question = row[2]
        labels_of_hackerrank = row[3]
        
        if not pd.isnull(labels_of_hackerrank) and not pd.isnull(question):
            labels_of_hackerrank = labels_of_hackerrank.split(",")
            
            for i in labels_of_hackerrank:
                append_to_file(i, list(set(hack_labels) - set(labels_of_hackerrank)), question)
        print(index)
        
        """
        question = data[2]
        if not pd.isnull(question):
            print(labels) 
            
            
            line_array = line.split(",")
            for elem in line_array:
                if elem not in labels:
                    labels[elem] = 1
                else:
                    labels[elem] += 1
    for line in hackerrank_labels:
        if not pd.isnull(line):
            line_array = line.split(",")
            for elem in line_array:
                if elem not in labels:
                    labels[elem] = 1
                else:
                    labels[elem] += 1
                    """
                    
    """
    for index, row in leetcode_csv.iterrows():
        question = row[2]
        labels_anan = row[3]
        if not pd.isnull(labels_anan):

            cat_arr = labels_anan.split(",")
            labels_dict = dict((v, labels[v]) for v in cat_arr)
            import operator
            max_label = max(labels_dict.items(), key=operator.itemgetter(1))[0]
            cat_arr = ["_label_" + i.replace(' ', '-') for i in cat_arr]
            cat_arr.append(row[2])
            with open("data.txt", 'a+') as f:
                for element in cat_arr:
                    element = str(element.encode('utf-8'))
                    f.write(element[2:-1] + ' ')
                #f.write("{} {}".format([str(i.encode('utf-8')) for i in cat_arr[:-1]], str(cat_arr[-1].encode('utf-8'))))
                #f.write('\n')
                f.write('\n')
            print(cat_arr)

           
        """
        
anani_dagitim(hackerrank_csv)
#fix_hackerrank_labels()
print('')