import os
import random
from shutil import copyfile, rmtree

# Constants
TRAIN_SIZE = 0.8
labels = ['neg', 'pos']

# Resetting
rmtree('train')
rmtree('test')
os.mkdir('train')
os.mkdir('test')

for label in labels:

    os.mkdir(f"train/{label}")
    os.mkdir(f"test/{label}")

    # Listing the files in the
    files = os.listdir(f'all/{label}')

    # Shuffle
    random.shuffle(files)

    # Splitting
    length = len(files)
    train_part = files[:int(length * TRAIN_SIZE)]
    test_part = files[int(length * TRAIN_SIZE):]

    print(f"Train size for {label}:", len(train_part))
    print(f"Test size for {label}:", len(test_part))

    # Copying the shuffled and splitted files to corresponding directories
    try:
        for file in train_part:
            copyfile(f'all/{label}/{file}', f'train/{label}/{file}')

        for file in test_part:
            copyfile(f'all/{label}/{file}', f'test/{label}/{file}')

    except Exception as e:
        print(e)
