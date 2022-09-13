from distutils.spawn import find_executable
from re import T
from tkinter import CURRENT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import time
import threading

WAIT_TIME = 120
 
# Opens text file and reads in data
try:
    file = open('timesheet.txt', 'r')
    f = file.readlines()
except FileNotFoundError:
    print("timesheet.txt is not in the correct spot or is named incorrectly")
    quit()

# Stores information from text file
data = []

# Gets and Formats current working location to find chrome driver
cwd = os.getcwd()
cwd = cwd.replace('\\', '/')
cwd += '/chromeDriver'

# Gets rid of new lines characters
# Adds informatin to data list
for i in range(len(f)):
    f[i] = f[i].replace('\n','')
    data.append(f[i])
    
# makes time data into lists
times_to_add = 0
for i in range(len(data)):
    times_to_add += 1
    data[i] = data[i].split()

try:
    # Initiate the driver and go to my umbc
    driver = webdriver.Chrome(cwd)
    driver.get('https://my.umbc.edu/')
except NameError:
    print("File path was not correct. Look at first line of text file")
    quit()

# Makes driver full screen
driver.maximize_window()

# clicks the log in button
button = driver.find_element(By.XPATH, '/html/body/header/div[1]/a[7]')
button.click()

# Clicks the next log in button
button = driver.find_element(By.ID,'login-myumbc')
button.click()

# Keeps track of seconds
seconds = 0

print("Please log into your account within 2 minutes or the program will close")
while seconds != WAIT_TIME:
    # Determines if user has logged in
    try:
        # Clicks the user icon on the top left of myumbc
        button = driver.find_element(By.XPATH, "/html/body/header/div[1]/div[4]/aside/div[1]/div[7]")
        button.click()
        break

    # Keeps track of seconds.
    # Seconds increase if the program can't click time sheet button
    except:
        seconds += 1
    # print(seconds)

    time.sleep(1)

# closes program if the user doesn't log in
if seconds == WAIT_TIME:
    quit()

# clicks "view profile"
button = driver.find_element(By.XPATH, "/html/body/header/div[1]/div[4]/aside/div[2]/div[5]/div[1]/div[2]/div[3]/a")
button.click()

# Clicks "timesheets"
button = driver.find_element(By.XPATH,'/html/body/header/div[4]/div[2]/div[3]/a[4]')
button.click()

# Keeps track of the different tabs and switches the main tab
tabs = driver.window_handles
current_tab = tabs[1]

# switches to current tab
driver.switch_to.window(current_tab)

# Waits until the Time Sheet page loads before moving on
while (driver.title != "Employee Time Sheet WorkCenter"):
    time.sleep(1)

# switches to the correct frame
driver.switch_to.frame(driver.find_element(By.NAME, "TargetContent"))

# Clicks on the timesheet if there is one
try:
    button = driver.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[5]/div/span/a")
    button.click()
except:
    print("No timesheet to click")
    quit()

# Goes back to the main frame
driver.switch_to.parent_frame()
# Waits for page to update
time.sleep(1)

driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/iframe"))

# Finds boxes to select location and schedule
select_work_1 = Select(driver.find_element(By.ID,"UM_ETS_UM_WEEK1_LOC"))
select_sched_1 = Select(driver.find_element(By.ID,"UM_ETS_UM_WEEK1_SCHED"))
select_work_2 = Select(driver.find_element(By.ID,"UM_ETS_UM_WEEK2_LOC"))
select_sched_2 = Select(driver.find_element(By.ID,"UM_ETS_UM_WEEK2_SCHED"))

# selects options with boxes
select_work_1.select_by_visible_text("On-site")
select_sched_1.select_by_visible_text("Regular")
select_work_2.select_by_visible_text("On-site")
select_sched_2.select_by_visible_text("Regular")

# adds boxes and times into boxes
for i in range((times_to_add * 2) - 1):
    # adds new row to timesheet
    button = driver.find_element(By.XPATH, "/html/body/form/div[3]/table/tbody/tr[1]/td/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr[3]/td[10]/div/a")
    button.click()
    time.sleep(.5)

# inputs data to timesheet
for i in range(times_to_add * 2):
    # finds input boxes
    inputElementIN = driver.find_element(By.ID, "UM_TIME_IN$" + str(i))
    inputElementOUT = driver.find_element(By.ID, "UM_TIME_OUT$" + str(i))

    # inserts time in data
    inputElementIN.send_keys(data[i % times_to_add][0])
    time.sleep(.2)

    # insertstemp data to get past page refresh
    inputElementOUT.send_keys("null")
    time.sleep(.5)

    # inserts time out data
    inputElementOUT = driver.find_element(By.ID, "UM_TIME_OUT$" + str(i))
    time.sleep(.2)
    inputElementOUT.send_keys(data[i % times_to_add][1])
    time.sleep(.5)