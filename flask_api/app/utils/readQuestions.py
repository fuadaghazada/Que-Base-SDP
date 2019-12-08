import sys
import pandas as pd

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


'''
    Read the programming questions from csv file

    :param: (str) filename: the given csv file
'''
def readProgrammingQuestions(filename):

    try:
        # Loading
        df = pd.read_csv(f'../algo_questions/{filename}', header = None)
        if len(df.columns) > 4:
            df.drop(df.columns[4], axis = 1, inplace = True)
        df.columns = ["title", "level", "body", "labels"]

        questions = list(map(lambda res: {'title': res[1]['title'],
                                          'body': res[1]['body'],
                                          'level': res[1]['level'],
                                          'labels': res[1]['labels'].split(',')
                                         }, df.iterrows()))
        return questions
        
    except Exception as e:
        raise
        return []
