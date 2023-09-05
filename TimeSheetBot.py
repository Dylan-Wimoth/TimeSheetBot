from distutils.spawn import find_executable
from tkinter import CURRENT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PySimpleGUI as sg
import time

TIME_OUT_SECONDS = 120 # Seconds until the program times out

def getName():
    """Gets the users name that can be used to parse the google calendar

    Returns:
        User's name as seen on calendar
    """

    layout = [
        [sg.Text("Please enter your name as seen on Google Calendar")],
        [sg.InputText(key="-NAME-")],
        [sg.Button("Submit", bind_return_key=True)]
    ]
    window = sg.Window("Name Input", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        # Ensures that the user types a name into the box before submitting
        elif event == "Submit" and values["-NAME-"]:
            user_name = values["-NAME-"]
            break

    window.close()

    # Attempt to return the user's name. If unable to do so, quit program
    try:
        return user_name
    except Exception:
        print("Please enter your name before closing the window.")
        quit()
    
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
    
    # Forces the program to timeout after a certain amount of time passes
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
    
    Returns:
        The start and end date of the most recent timesheet.
        Used to retrieve events in-between start and end date
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
        start_date = driver.find_element(By.ID, "UM_ETS_EMSUM_VW_PAY_BEGIN_DT$0")
        end_date = driver.find_element(By.ID, "UM_ETS_EMSUM_VW_PAY_END_DT$0")
        start_date_text = start_date.text
        end_date_textprint = end_date.text
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

    return start_date_text, end_date_textprint


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
    for i in range(len(data) - 1):
        # adds new row to timesheet
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/table/tbody/tr[1]/td/div/table/tbody/tr[6]/td[2]/div/table/tbody/tr[3]/td[10]/div/a")))
        button.click()
        time.sleep(.3)

    # Inputs data to timesheet
    for i in range(len(data)):
        # Finds input boxes
        inputElementDATE = wait.until(EC.element_to_be_clickable((By.ID, "UM_WORK_DATE$" + str(i))))
        inputElementIN = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_IN$" + str(i))))
        inputElementOUT = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_OUT$" + str(i))))

        # Inserts date
        inputElementDATE.send_keys(data[i][0])
        time.sleep(.1)

        # Inserts time in data
        inputElementIN.send_keys(data[i][1])
        time.sleep(.1)

        # Inserts time out data
        inputElementOUT = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_OUT$" + str(i))))
        time.sleep(.1)
        inputElementOUT.send_keys("null")
        time.sleep(.1)
        inputElementOUT = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_OUT$" + str(i))))
        inputElementOUT.send_keys(data[i][2])
        time.sleep(.1)


def close_program(keep_alive):
    """Keeps program open for a specific amount of time

    Args:
        keep_alive: seconds that the program should stay open after all instructions complete
    """
    
    temp = 0

    while (temp < keep_alive):
        temp += 1
        time.sleep(1)