import sys

SPLITTER = "!!!"

'''
    Read the questions from the given filename

    :param: (str) filename: the given filename
'''
def readQuestions(filename):

    try:
        # Reading the file
        with open(f'../questions_from_books/{filename}', 'r') as readFile:
            txt = str(readFile.read()).strip()
            questions = [question.replace('\n', ' ').strip() for question in txt.split(SPLITTER)]

        return questions

    except Exception as e:
        raise
        return []
