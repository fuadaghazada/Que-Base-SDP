import nltk

MAX_TITLE_LENGTH = 50

'''
    Generating title from a given text

    :param: (str) text: the given text
    :return: (str) title: generated title
'''

def generateTitleFromText(text):
    # Splitting into the sentences
    sentences = nltk.sent_tokenize(text)

    # TODO: Later it can be updated into more advanced form

    title = sentences[0] if len(sentences) > 0 else "..."

    # Limiting
    if len(title) > MAX_TITLE_LENGTH:
        title = title[:MAX_TITLE_LENGTH]
        title += "..."

    return title
