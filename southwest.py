from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from optparse import OptionParser
from datetime import datetime
from datetime import timedelta

import sched, time

# Command line flags to pass.  All are Required
parser = OptionParser()
parser.add_option("-c", "--confirmation_number",
                  action="store",
                  type="string",
                  dest="confirmation_number",
                  help="flight confirmation number")
parser.add_option("-f", "--first_name",
                  action="store",
                  type="string",
                  dest="first_name",
                  help="first name of passenger")
parser.add_option("-l", "--last_name",
                  action="store",
                  type="string",
                  dest="last_name",
                  help="last name of passenger")
parser.add_option("-p", "--phone_number",
                  action="store",
                  type="string",
                  dest="phone_number",
                  help="phone number (1234567890)")
parser.add_option("-t", "--time",
                  action="store",
                  type="string",
                  dest="time",
                  help="flight time")
(options, args) = parser.parse_args()

# scheduler to schedule when we check in
s = sched.scheduler(time.time, time.sleep)

driver = None

# browser is opened 20 seconds before check in time
def open_browser():
    global driver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1440,900")
    driver = webdriver.Chrome('/opt/southwest/chromedriver', chrome_options=chrome_options)

    wait = WebDriverWait(driver, 10)
    driver.get("https://www.southwest.com/flight/retrieveCheckinDoc.html")

    # find text boxes to input data
    first_name = driver.find_element_by_id("passengerFirstName")
    last_name = driver.find_element_by_id("passengerLastName")
    confirmation_number = driver.find_element_by_id("confirmationNumber")

    # input data
    first_name.send_keys(options.first_name)
    last_name.send_keys(options.last_name)
    confirmation_number.send_keys(options.confirmation_number)

def check_in():
    first_check_in = driver.find_element_by_id("form-mixin--submit-button")
    first_check_in.click()

    # while it is too early, keep retrying!
    tooEarly = True 
    while tooEarly:
        try:
	     time.sleep(5)
             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
             second_check_in = driver.find_element_by_class_name("air-check-in-review-results--check-in-button")
	     second_check_in.click()	
	     tooEarly = False
	except NoSuchElementException:
             time.sleep(5)
             first_check_in.click()
             continue
    time.sleep(0.5)

    textBoardingPass = driver.find_element_by_class_name("boarding-pass-options--button-text")
    time.sleep(1)

    phone_number = str(options.phone_number)
    textBoardingPass.click()

    phone = driver.find_element_by_id("textBoardingPass")
    phone.send_keys(phone_number[0:10])

    # submit the request
    driver.find_element_by_id("form-mixin--submit-button").click()

# calculate time to start checking in
flight_time = datetime.strptime(options.time, '%b %d %Y %I:%M%p')
check_in_time = flight_time - timedelta(days=1)
check_in_time_seconds = time.mktime(check_in_time.timetuple())

s.enterabs(check_in_time_seconds - 20, 1, open_browser, ())
s.enterabs(check_in_time_seconds, 1, check_in, ())
s.run()
