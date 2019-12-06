import csv
import time
import sys
import os
import re

import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
TIME_DELAY = 2
TIMEOUT = 100
FILENAME ='leetcode_dataset.csv'

'''
    Scraping the question information by parsing

    @param url: scraping from the given url
    @param driver: Browser driver for waiting for loading
'''

def scrape_question(url, driver = None):

    try:
        if driver is None:
            driver = webdriver.Chrome()

        # Go to URL
        driver.get(f"https://leetcode.com{url}")

        # Waiting for description fully loaded
        description = EC.presence_of_element_located((By.CLASS_NAME, "description__24sA"))
        WebDriverWait(driver, TIMEOUT).until(description)

        # Page source
        page_source = driver.page_source

        # Scraper
        soup = bs4.BeautifulSoup(page_source, 'html.parser')

        # Scraped data
        title = soup.select('.css-v3d350')[0].text.split('.')[-1].strip()
        difficulty = soup.select('.css-10o4wqw > div')[0].text.strip()
        question = soup.select('.content__u3I1.question-content__JfgR')[0].text.strip()
        related_topics = [link.text.strip() for link in soup.select('.css-1hky5w4 a.topic-tag__1jni')]
        similar_question_links = [link['href'].strip() for link in soup.select('a.title__1kvt[href]')]

        # Log
        print("\n********************************************")
        print(f"Title: {title}")
        print(f"Difficulty: {difficulty}")
        print(f"Question: {question}")
        print(f"Related topics: {related_topics}")
        print(f"Similar questions: {similar_question_links}")
        print("********************************************\n")

        # Return the data
        return {
            "title": title,
            "difficulty": difficulty,
            "question": question,
            "related_topics": related_topics,
            "similar_questions": similar_question_links
        }

    except Exception as e:
        raise e
        sys.exit()


'''
    Saving the components

    @param question_data - question data containing the components
'''

def save_question(question_data):

    # Components
    title = question_data['title']
    difficulty = question_data['difficulty']
    question = question_data['question']
    related_topics = ','.join(question_data['related_topics'])
    similar_questions = ','.join(question_data['similar_questions'])

    # Writing to CSV
    with open(FILENAME, 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([title, difficulty, question, related_topics, similar_questions])


'''
    Opens browser => selects 'all' questions => scraping the table of question all_links
                  => sending request to each link for getting question information
'''

def open_scrape_close():

    try:
        # Opening Chrome
        driver = webdriver.Chrome()

        # Opens algorithms page
        driver.get("https://leetcode.com/problemset/all/")

        # Using Implicitly Waits for find_elements
        driver.implicitly_wait(TIME_DELAY)

        # Clicking 'all' from combobox
        driver.find_element_by_xpath('//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span[1]/select/option[4]').click()

        # Page source
        page_source = driver.page_source

        # Scraper
        soup = bs4.BeautifulSoup(page_source, 'html.parser')

        # Opens every problem and then copies their data into a file
        rows = list(filter((lambda x: 'fa fa-lock' not in str(x)), soup.select('.reactable-data tr')))
        links = list(map((lambda x: re.findall('href=[\'"]?([^\'" >]+)', str(x))[0]), rows))
        links = list(filter((lambda x: 'problems' in x), links))

        # All links
        for href in links:
            question_data = scrape_question(href, driver)
            save_question(question_data)

        # Closing Chrome
        driver.close()

    except Exception as e:
        raise e


'''
    Sign in
'''

def sign_into_leetcode(driver):
    driver.implicitly_wait(TIME_DELAY)

    driver.get("https://leetcode.com/accounts/logout")

    username = raw_input("Enter your username: ")
    password = raw_input("Enter your password: ")

    driver.get("https://leetcode.com/accounts/login/")
    driver.find_element_by_xpath('// *[ @ id = "id_login"]').send_keys(username)
    driver.find_element_by_xpath('// *[ @ id = "id_password"]').send_keys(password)
    driver.find_element_by_xpath('// *[ @ id = "id_password"]').send_keys(Keys.ENTER)

    driver.implicitly_wait(0)


'''
    Main
'''

if __name__ == "__main__":

    # CSV Headers
    # with open(FILENAME, 'w') as writeFile:
    #     writer = csv.writer(writeFile)
    #     writer.writerow(["Title", "Difficulty", "Question", "Related topics", "Similar questions"])

    # Scrape-Save-Close
    open_scrape_close()
