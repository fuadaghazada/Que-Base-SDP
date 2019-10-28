import sys
from operateDb import insertQuestion

SPLITTER = "!!!"

try:
    if len(sys.argv) < 3:
        raise Exception("Please provide a file name in the arguments or check the directory")

    # Name of the file
    filename = sys.argv[2]

    # Reading the file
    with open(filename, 'r') as readFile:
        txt = str(readFile.read()).strip()
        questions = [question.replace('\n', ' ').strip() for question in txt.split(SPLITTER)]

        print(f"Number of questions: {len(questions)}\n")
        print(questions)

        # TODO: Add questions to the db
        # for question in questions:
        #     insertQuestion({'body': question})


except Exception as e:
    raise
