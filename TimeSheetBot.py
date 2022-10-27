from distutils.spawn import find_executable
from tkinter import CURRENT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import time
import datetime
import pandas as pd

WAIT_TIME = 120

daysDict = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday"
}

# Returns the start date for the work period
def getStartDate():
    current_day = pd.Timestamp(datetime.datetime.today()).day_name()

    if (current_day == daysDict[1]):
        return datetime.datetime.today() - datetime.timedelta(days=7)
    if (current_day == daysDict[2]):
        return datetime.datetime.today() - datetime.timedelta(days=8)
    if (current_day == daysDict[3]):
        return datetime.datetime.today() - datetime.timedelta(days=9)
    if (current_day == daysDict[4]):
        return datetime.datetime.today() - datetime.timedelta(days=10)
    if (current_day == daysDict[5]):
        return datetime.datetime.today() - datetime.timedelta(days=11)

# Formats the date so it can be inputted into the timesheet
def format_date(current_date):
    current_date = str(current_date)[:10]
    day = current_date[8:]
    month = current_date[5:7]
    year = current_date[:4]
    return month + '/' + day + '/' + year

START_DAY = getStartDate()

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
    
# Makes time data into lists
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

# Clicks the log in button
button = driver.find_element(By.XPATH, '/html/body/header/div[1]/a[7]')
button.click()

# Clicks the next log in button
button = driver.find_element(By.ID,'login-myumbc')
button.click()

# Keeps track of seconds
seconds = 0

#Gives the user 2 minutes to log into system else the program quits
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

    time.sleep(1)

# Closes program if the user doesn't log in
if seconds == WAIT_TIME:
    quit()

# Clicks "view profile"
button = driver.find_element(By.XPATH, "/html/body/header/div[1]/div[4]/aside/div[2]/div[5]/div[1]/div[2]/div[3]/a")
button.click()

# Clicks "timesheets"
button = driver.find_element(By.XPATH,'/html/body/header/div[4]/div[2]/div[3]/a[4]')
button.click()

# Keeps track of the different tabs and switches the main tab
tabs = driver.window_handles
current_tab = tabs[1]

# Switches to current tab
driver.switch_to.window(current_tab)

# Waits until the Time Sheet page loads before moving on
while (driver.title != "Employee Time Sheet WorkCenter"):
    time.sleep(1)

# Switches to the correct frame
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

# Selects options with boxes
select_work_1.select_by_visible_text("On-site")
select_sched_1.select_by_visible_text("Regular")
select_work_2.select_by_visible_text("On-site")
select_sched_2.select_by_visible_text("Regular")

# Adds rows for days/time
for i in range((times_to_add * 2) - 1):
    # adds new row to timesheet
    button = driver.find_element(By.XPATH, "/html/body/form/div[3]/table/tbody/tr[1]/td/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr[3]/td[10]/div/a")
    button.click()
    time.sleep(.5)

# Inputs data to timesheet
for i in range(times_to_add * 2):
    if (i < times_to_add):
        current_day = format_date(START_DAY + datetime.timedelta(days=int(data[i][2]) - 1))
    else:
        current_day = format_date(START_DAY + datetime.timedelta(days=int(data[i % times_to_add][2]) + 6))

    # Finds input boxes
    inputElementIN = driver.find_element(By.ID, "UM_TIME_IN$" + str(i))
    inputElementOUT = driver.find_element(By.ID, "UM_TIME_OUT$" + str(i))
    inputElementDATE = driver.find_element(By.ID, "UM_WORK_DATE$" + str(i))

    # Inserts date
    inputElementDATE.send_keys(current_day)
    time.sleep(.4)

    # Inserts time in data
    inputElementIN.send_keys(data[i % times_to_add][0])
    time.sleep(.4)

    # Inserts time out data
    inputElementOUT = driver.find_element(By.ID, "UM_TIME_OUT$" + str(i))
    time.sleep(.4)
    inputElementOUT.send_keys("Null")
    time.sleep(.3)
    inputElementOUT = driver.find_element(By.ID, "UM_TIME_OUT$" + str(i))
    inputElementOUT.send_keys(data[i % times_to_add][1])
    time.sleep(.5)