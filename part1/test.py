from operateDb import insertQuestion, analyzeQuestion, findSimilarQuestions
from PdfExtract import convert_pdf_to_txt

# insertQuestion({"body": "When a process is created using the classical fork() system call, which of the following is not inherited by the child process?"}, True)
# insertQuestion({"body": ""}, True)
# insertQuestion({"body": ""}, True)
# insertQuestion({"body": ""}, True)
# insertQuestion({"body": ""}, True)

# findSimilarQuestions("Which of the following is a function of the nucleus? A. controls most of the cell’s processes B. contains the information needed to make proteins # C. stores DNA D. all of the above")

txt = convert_pdf_to_txt('../test_pdfs/empty.pdf')
