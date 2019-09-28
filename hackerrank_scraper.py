import re
import time
import requests
import json
import csv

import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pprint import pprint

# Constants
TIMEOUT = 5
FILENAME = 'hackerrank_dataset.csv'

'''
    Returning the URL given offset and limit
'''

def URL(domain, limit, offset):
    return f"https://www.hackerrank.com/rest/contests/master/tracks/{domain}/challenges?offset={offset}&limit={limit}&track_login=true"


'''
    Problem URL
'''

def PROBLEM_URL(uri):
    return f"https://www.hackerrank.com/challenges/{uri}/problem"



'''
    Getting all the problems
'''

def getAllProblems(domain = 'algorithms', offset = 450):

    all_problems = []
    LIMIT = 10

    try:

        for i in range(0, offset, LIMIT):

            url = URL(domain, LIMIT, i)
            r = requests.get(url, headers = {'Content-type' : 'application/json'})
            contentJson = json.loads(r.text)

            # Models
            models = contentJson['models']

            # Extracting necessary data
            problem_data = list(map((lambda x: {'id': x['id'], \
                                                'title': x['name'], \
                                                'difficulty': x['difficulty_name'], \
                                                'tags': x['tag_names'], \
                                                'uri': x['slug'], \
                                                }), models))

            # Extending the whole list
            all_problems.extend(problem_data)

            # Log
            print(f"***\nObtained: \nDomain: {domain}\nOffset: {i} \nLimit: {LIMIT}\n***\n")

            # Waiting for avoiding IP blocking  :D
            time.sleep(1)

        # Writing to JSON
        with open(f'hackerrank_problems({domain}).json', 'w', encoding = 'utf-8') as f:
            json.dump(all_problems, f, ensure_ascii = False, indent = 4)

    except Exception as e:
        raise e


'''
    Scrape the question from the given url
'''

def scrape_question(question_data, driver = None):

    # div challenge-body-html
    # div hackdown-content

    if driver is None:
        driver = webdriver.Chrome()

    # Go to URL
    driver.get(PROBLEM_URL(question_data['uri']))

    # Waiting for autbox loaded
    authbox = EC.presence_of_element_located((By.CLASS_NAME, "auth-box"))
    WebDriverWait(driver, TIMEOUT).until(authbox)

    # # Clicking the 'cross'
    # driver.find_element_by_class_name('ui-icon-cross').click()
    # -OR- Pressing ESC
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # Page source
    page_source = driver.page_source

    # Scraper
    soup = bs4.BeautifulSoup(page_source, 'html.parser')

    raw_paragraphs = soup.select('.challenge-body-html p, .challenge-body-html code, .challenge-body-html li')

    for p in raw_paragraphs:
        # Cleaning spans
        for match in p.findAll('span'):
            match.unwrap()

        # Cleaning style
        for match in p.findAll('style'):
            match.unwrap()

        # Cleaning svg
        for match in p.findAll('svg'):
            match.unwrap()

        # Cleaning g
        for match in p.findAll('g'):
            match.unwrap()

        # Cleaning p
        for match in p.findAll('path'):
            match.unwrap()


    paragraphs = list(map((lambda x: x.text), raw_paragraphs))
    question = '\n'.join(paragraphs)

    # Adding the question
    question_data['question'] = question

    # Log
    print("\n********************************************")
    print(f"Title: {question_data['title']}")
    print(f"Difficulty: {question_data['difficulty']}")
    print(f"Question: {question_data['question']}")
    print(f"Tags {question_data['tags']}")
    print("********************************************\n")

    # Return
    return question_data


'''
    Saving the components

    @param question_data - question data containing the components
'''

def save_question(question_data):

    # Components
    title = question_data['title']
    difficulty = question_data['difficulty']
    question = question_data['question']
    tags = ','.join(question_data['tags'])

    # Writing to CSV
    with open(FILENAME, 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([title, difficulty, question, tags])


'''
    Opens browser => selects 'all' questions => scraping the table of question all_links
                  => sending request to each link for getting question information
'''

def open_scrape_close():

    try:
        # Opening Chrome
        driver = webdriver.Chrome()

        questions = []
        with open('hackerrank_problems(algorithms).json') as f:
            questions = json.load(f)

        with open('hackerrank_problems(data-structures).json') as f:
            questions.extend(json.load(f))

        # All links
        for datom in questions:
            question_data = scrape_question(datom, driver)
            save_question(question_data)

        # Closing Chrome
        driver.close()

    except Exception as e:
        raise e


'''
    Main
'''

if __name__ == "__main__":

    # CSV Headers
    with open(FILENAME, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(["Title", "Difficulty", "Question", "Tags"])

    # Scrape-Save-Close
    open_scrape_close()


# # Test

# # Getting the question list
# getAllProblems()                            # Algorithms
# getAllProblems('data-structures', 130)      # Data Structures
