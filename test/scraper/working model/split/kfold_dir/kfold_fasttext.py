# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:08:04 2019

@author: ALPER KAGAN KAYALI THE BEST PYTHON CODER ON THE WORLD 
"""

import fasttext as ft
def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))
#print(model.labels)
for i in range(0,10):
    print('i',i)    
    model = ft.train_supervised('datafinal_train{}.txt'.format(i), epoch = 1)
    print_results(*model.test('datafinal_test{}.txt'.format(i)))
    model.save_model("kfold_trained_model{}.bin".format(i))