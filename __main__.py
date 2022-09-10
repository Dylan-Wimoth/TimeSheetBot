from distutils.spawn import find_executable
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

WAIT_TIME = 120

#Opens text file and reads in data
try:
    file = open('timesheet.txt', 'r')
    f = file.readlines()
except FileNotFoundError:
    print("timesheet.txt is not in the correct spot or is named incorrectly")
    quit()

data = []

#Gets rid of new lines characters
#Adds informatin to data list
for i in range(len(f)):
    if (i != len(f) - 1):
        item = f[i][:-1]
        data.append(item)

#adjusts the first piece of data so it can be used as a file path
data[0] = data[0].replace('\\', '/')
data[0] = data[0] + '/chromedriver'

try:
    # Initiate the driver and go to my umbc
    driver = webdriver.Chrome(data[0])
    driver.get('https://my.umbc.edu/')
except NameError:
    print("File path was not correct. Look at first line of text file")
    driver.quit()

#clicks the log in button
button = driver.find_element(By.XPATH, '/html/body/header/div[1]/a[7]')
button.click()

# Clicks the next log in button
button = driver.find_element(By.ID,'login-myumbc')
button.click()

# Keeps track of seconds
seconds = 0

print("Please log into your account within 2 minutes or the program will close")
while seconds != WAIT_TIME:
    #Determines if user has logged in
    try:
        #Clicks the user icon on the top left of myumbc
        button = driver.find_element(By.XPATH, "/html/body/header/div[1]/div[4]/aside/div[1]/div[7]")
        button.click()
        break

    #Keeps track of seconds.
    #Seconds increase if the program can't click time sheet button
    except:
        seconds += 1
    print(seconds)

    time.sleep(1)

#closes program if the user doesn't log in
if seconds == WAIT_TIME:
    driver.quit()

# clicks "view profile"
button = driver.find_element(By.XPATH, "/html/body/header/div[1]/div[4]/aside/div[2]/div[5]/div[1]/div[2]/div[3]/a")
button.click()

# Clicks "timesheets"
button = driver.find_element(By.XPATH,'/html/body/header/div[4]/div[2]/div[3]/a[4]')
button.click()

#Keeps track of the different tabs and switches the main tab
tabs = driver.window_handles
current_tab = tabs[1]

#switches to current tab
driver.switch_to.window(current_tab)

#Waits until the Time Sheet page loads before moving on
while (driver.title != "Employee Time Sheet WorkCenter"):
    time.sleep(1)

#switches to the correct frame
driver.switch_to.frame(driver.find_element(By.NAME, "TargetContent"))

#Clicks on the timesheet if there is one
try:
    button = driver.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[5]/div/span/a")
    button.click()
except:
    print("No timesheet to click")
    driver.quit()

