import os

# Constants
labels = ['neg', 'pos']

try:
    with open('input.txt', 'w') as writeFile:
        for label in labels:

            filenames = os.listdir(f'all/{label}')

            for filename in filenames:
                with open(f'all/{label}/{filename}', 'rb') as readFile:
                    txt = str(readFile.read()).encode('utf-8')
                    txt = txt.decode('utf-8')
                    txt = str(txt).strip().replace('\n', ' ')
                    txt = txt[2:-1]                                 # Removes b
                    lbl = 0 if label is 'neg' else 1
                    writeFile.write(f"__label__{lbl} {txt}\n")

except Exception as e:
    print("Error")
    raise
