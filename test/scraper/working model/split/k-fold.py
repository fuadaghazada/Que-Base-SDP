from random import randrange


f = open('data_final_merged_shuffled.txt', 'r', encoding="utf8")
dataset = f.readlines()
f.close()
#exit(0)
# Split a dataset into k folds
def cross_validation_split(dataset, folds=3):
    dataset_split = list()
    dataset_copy = list(dataset)
    fold_size = int(len(dataset) / folds)
    for i in range(folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            fold.append(dataset_copy.pop(index))
        dataset_split.append(fold)
    return dataset_split

splitted_dataset = cross_validation_split(dataset,10)


