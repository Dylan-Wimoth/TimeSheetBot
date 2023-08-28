from distutils.spawn import find_executable
from tkinter import CURRENT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pandas as pd

TIME_OUT_SECONDS = 120 # Seconds until the program times out
DAYSDICT = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday"
}

# Returns the start date for the work period
def getStartDate():
    """Determines which day was the start of the pay period
    This function will only work if the user uses the program on the second week of the pay period

    Returns:
        The first monday of the pay period
    """
    current_day = pd.Timestamp(datetime.datetime.today()).day_name()

    if (current_day == DAYSDICT[1]):
        return datetime.datetime.today() - datetime.timedelta(days=7)
    if (current_day == DAYSDICT[2]):
        return datetime.datetime.today() - datetime.timedelta(days=8)
    if (current_day == DAYSDICT[3]):
        return datetime.datetime.today() - datetime.timedelta(days=9)
    if (current_day == DAYSDICT[4]):
        return datetime.datetime.today() - datetime.timedelta(days=10)
    if (current_day == DAYSDICT[5]):
        return datetime.datetime.today() - datetime.timedelta(days=11)

# Formats the date so it can be inputted into the timesheet
def format_date(date):
    """Formats a timedelta object so it can be entered into timesheet

    Args:
        date: timedelta object that needs to be formatted

    Returns:
        Formatted timedelta object string in mm/dd/yy format
    """
    date = str(date)[:10]
    day = date[8:]
    month = date[5:7]
    year = date[:4]
    return month + '/' + day + '/' + year

def read_times():
    """Reads in timesheet.txt and formats it into a list

    Returns:
        List of worktimes formatted as [[{START}, {END}, {DAY}], ['4:00PM', '5:15PM', '1'], ...]
    """

    # Opens text file and reads in data
    try:
        file = open('timesheet.txt', 'r')
        f = file.readlines()
    except FileNotFoundError as err:
        print("Chrome did not open. Error:", err)
        quit()

    # Stores information from text file
    data = []

    # Gets rid of new lines characters
    # Adds informatin to data list
    for i in range(len(f)):
        f[i] = f[i].replace('\n','')
        data.append(f[i])
        
    # Makes time data into lists
    for i in range(len(data)):
        data[i] = data[i].split()
    
    return data
    
def start_driver():
    """Starts the driver, goes to my.umbc.edu and full screens it. Creates timeout object.

    Returns:
        Driver and timeout object
    """

    try:
        # Initiate the driver and go to my umbc
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://my.umbc.edu/')
    except NameError as err:
        print("Cannot open chrome. Error:", err)
        quit()
    
    # Allows the program to timeout after a certain amount of time passes
    time_out = WebDriverWait(driver, TIME_OUT_SECONDS)

    return driver, time_out

def user_login(wait):
    """Goes through login process. 

    Args:
        wait: timeout object
    """

    # Clicks the log in button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/header/div[1]/a[7]')))
    button.click()

    # Clicks "log in with UMBC" button
    button = wait.until(EC.element_to_be_clickable((By.ID,'login-umbc')))
    button.click()

    # Clicks "Do not remember" button in duo
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/div[2]/div[4]/button")))
    button.click()


def open_timesheet(driver, wait):
    """Goes through login process. 

    Args:
        driver: driver object
        wait: timeout object
    """

    # Clicks the user icon on the top right of myumbc
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div[1]/div[4]/aside/div[1]/div[7]")))
    button.click()

    # Clicks "view profile"
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/div[1]/div[4]/aside/div[2]/div[5]/div[1]/div[2]/div[3]/a")))
    button.click()

    # Clicks "timesheets"
    button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/header/div[4]/div[2]/div[3]/a[4]')))
    button.click()

    # Keeps track of the different tabs and switches the main tab
    tabs = driver.window_handles
    current_tab = tabs[1]

    # Switches to current tab
    driver.switch_to.window(current_tab)

    # TODO: This is a bit janky. Would prefer to use a built in method similar to .until
    while (driver.title != "Employee Time Sheet WorkCenter"):
        time.sleep(1)

    # Switches to the correct frame
    driver.switch_to.frame(driver.find_element(By.NAME, "TargetContent"))

    # Clicks on the timesheet if there is one
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[5]/div/span/a")))
        button.click()
    except Exception as err:
        print("No timesheet to click. Error:", err)
        quit()

    # Goes back to the main frame
    driver.switch_to.parent_frame()

    # Waits for page to update
    time.sleep(1)

    # Switches to frame
    driver.switch_to.frame(wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div[2]/div/div[2]/iframe"))))


def insert_times(wait, data):
    """Inserts worktimes into timesheet

    Args:
        wait: timeout object
        data: Formatted time the user works
    """

    # Finds boxes to select location and schedule
    select_work_1 = Select(wait.until(EC.element_to_be_clickable((By.ID,"UM_ETS_UM_WEEK1_LOC"))))
    select_sched_1 = Select(wait.until(EC.element_to_be_clickable((By.ID,"UM_ETS_UM_WEEK1_SCHED"))))
    select_work_2 = Select(wait.until(EC.element_to_be_clickable((By.ID,"UM_ETS_UM_WEEK2_LOC"))))
    select_sched_2 = Select(wait.until(EC.element_to_be_clickable((By.ID,"UM_ETS_UM_WEEK2_SCHED"))))

    # Selects options with boxes
    select_work_1.select_by_visible_text("On-site")
    select_sched_1.select_by_visible_text("Regular")
    select_work_2.select_by_visible_text("On-site")
    select_sched_2.select_by_visible_text("Regular")

    # Adds rows for days/time
    for i in range((len(data) * 2) - 1):
        # adds new row to timesheet
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/table/tbody/tr[1]/td/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr[3]/td[10]/div/a")))
        button.click()
        time.sleep(.3)

    # Inputs data to timesheet
    for i in range(len(data) * 2):
        # Don't ask me about this math. It works. Idk how
        if (i < len(data)):
            current_day = format_date(start_day + datetime.timedelta(days=int(data[i][2]) - 1))
        else:
            current_day = format_date(start_day + datetime.timedelta(days=int(data[i % len(data)][2]) + 6))

        # Finds input boxes
        inputElementDATE = wait.until(EC.element_to_be_clickable((By.ID, "UM_WORK_DATE$" + str(i))))
        inputElementIN = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_IN$" + str(i))))
        inputElementOUT = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_OUT$" + str(i))))

        # Inserts date
        inputElementDATE.send_keys(current_day)
        time.sleep(.3)

        # Inserts time in data
        inputElementIN.send_keys(data[i % len(data)][0])
        time.sleep(.3)

        # Inserts time out data
        inputElementOUT.send_keys(data[i % len(data)][1])
        time.sleep(.3)

def close_program(keep_alive):
    """Keeps program open for a specific amount of time

    Args:
        keep_alive: seconds that the program should stay open after all instructions complete
    """
    temp = 0

    while (temp < keep_alive):
        temp += 1
        time.sleep(1)

if __name__ == "__main__":
    start_day = getStartDate()
    work_times = read_times()
    driver, wait = start_driver()
    user_login(wait)
    open_timesheet(driver, wait)
    insert_times(wait, work_times)

    close_program(300)