import sys
import requests
import bs4

from pprint import pprint

# URL of the site
URL = 'https://www.sociologyguide.com/questions/'


'''
    Sending request to the given url
'''
def send_request(url):
    req = requests.get(url, verify=False)

    try:
        req.raise_for_status()
    except Exception as e:
        print(e)
        sys.exit()

    print('Request is successful!')
    return req


'''
    List of Sociology topics
'''
def _fetchList():
    # Sending request
    req = send_request(URL)

    # Scraper
    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    # List
    div = soup.find('div', {'class': 'col-lg-9 col-md-9 col-sm-9 text'})
    links = [li.find('a')['href'] for li in div.find_all('li')]

    return links


'''
    Fetch questions from given link to the page
'''
def _fetchQuestions(uri):
    # Sending request
    req = send_request(URL + uri)

    # Scraper
    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    div = soup.find('div', {'class': 'col-lg-9 col-md-9 col-sm-9 text'})
    question_titles = [title.text for title in div.find_all('h3')]

    return question_titles


'''
    Fetching all questions from all topics
'''
def fetchAll():

    all_questions = []

    list = _fetchList()

    for uri in list:
        questions = _fetchQuestions(uri)
        all_questions += questions

    return all_questions


# Test
questions = fetchAll()
print(f"Number of questions: {len(questions)}")


# DB insertion
from operateDb import insertQuestion

for question in questions:
    insertQuestion({"body": question}, True)
