'''
A simple script to make payments on a student loan

This script can run in the background so I do not have to look at
how slow and infuriating the process is. 
'''



import getpass
import sys
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

#log in to the site. It is very slow
def login(driver, username, password):
    logging.info('Attempting to log in with entered username and password')
    uname = driver.find_element_by_id('username')
    uname.send_keys(username)
    pword = driver.find_element_by_id('password')
    pword.send_keys(password)
    pword.send_keys(Keys.RETURN)
    wait = WebDriverWait(driver, 60)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/section[2]/div/div/div[2]/a')))
    except:
        logging.error('Timeout exceded for login')
        driver.quit()
        sys.exit()

    logging.info('login successful')

#checks to see if there is any amount that is due, if not, we can stop
def amount_due(driver):
    amnt = driver.find_element_by_xpath('/html/body/div[3]/div[3]/section[3]/div/div/div[3]/div/div/p')
    if(amnt.text == '$0.00'):
        logging.info(amnt.text + ' is due this month')
        return False
    else:
        logging.info(amnt.text + ' is due this month')
        return True

#submits payment for total amount that is due
def submit_payment(driver):

    if(amount_due(driver)):
        make_payment = driver.find_element_by_xpath('/html/body/div[3]/div[3]/section[2]/div/div/div[2]/a')
        make_payment.click()

        try:
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/form/fieldset/div[3]/div[4]/div[2]/div/div[3]/input')))
        except:
            logging.error('Timeout exceeded to make payment')
            driver.quit()
            sys.exit()
        
        total_due = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/form/fieldset/div[3]/div[4]/div[2]/div/div[3]/input')
        total_due.click()
        submit = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/form/div/div[4]/button')
        submit.click()

        try:
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[2]/form/div/div[3]/button')))
        except:
            logging.error('Timeout exceeded to confirm')
            driver.quit()
            sys.exit()

        confirm = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/form/div/div[3]/button')
        confirm.click()

    else:
        logging.info('There is no amount due. No payment made')

def main():
  
    username = getpass.getpass('Enter your username: ')
    password = getpass.getpass('Enter your password: ')

    logging.basicConfig(level=logging.INFO)
    
    #setup selenium ChromeDriver, I do not need to see the window or logging
    logging.info('Setting up selenium') 
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('--silent')
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=op)
    type(driver)

    driver.get('https://www.collegeaveservicing.com/auth/login')

    login(driver, username, password)
    submit_payment(driver)

main()