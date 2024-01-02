from distutils.spawn import find_executable
from tkinter import CURRENT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PySimpleGUI as sg
import time
import json

TIME_OUT_SECONDS = 120 # Seconds until the program times out

def getNameGui():
    """Gets the users name that can be used to parse the google calendar
       Updates the config.json with the users input for being remembered for next time
    """

    nameLayout = [
        [sg.Text("Please enter your name as seen on Google Calendar")],
        [sg.InputText(key="-NAME-")],
        [sg.Button("Submit", bind_return_key=True)]
    ]
    nameWindow = sg.Window("Name Input", nameLayout)

    while True:
        event, values = nameWindow.read()
        if event == sg.WINDOW_CLOSED:
            break
        # Ensures that the user types a name into the box before submitting
        elif event == "Submit" and values["-NAME-"]:
            user_name = values["-NAME-"]
            break

    nameWindow.close()

    # Attempt to return the user's name. If unable to do so, quit program
    try:
        #Updates the json file with the users name inputted into the gui
        with open('config.json', 'r') as json_file:
            config = json.load(json_file)
        config['user'] = user_name #Sets the user name object in config file
        with open('config.json', 'w') as json_file:
            json.dump(config, json_file, indent = 2) #Update json file with name
    except Exception as err:
        print("Please enter your name before closing the window.")
        print(err)
        quit()

def getName():
    """Gets user name from config.json file

    Returns:
        str: Users name from the json file
    """
    try:
        with open('config.json', 'r') as json_file:
            config = json.load(json_file)
    except Exception as err:
        print(f"Error has occured in getName block 1: {err}")
    try:
        name = config['user'] #Gets users name
        return name
    except Exception as err:
        print(f"Error has occured in getName block 2: {err}")
        return "" #Return empty string other wise

def getRememberMeGui():
    """Asks the user if they want their name to be remembered
    """
    rememberMeLayout = [
        [sg.Text("Would you like to remember your name on this PC?")],
        [sg.Text("DISCLAIMER: If you want to change your decision edit the config.json rememberMe object")],
        [sg.Button("Yes", bind_return_key = True),
         sg.Button("No", bind_return_key = False)],
        ]
    
    window = sg.Window("Remember Me?", rememberMeLayout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        # Ensures that the user presses a button
        elif event == "Yes":
            choice = True
            break
        elif event == "No":
            choice = False
            break
        
    window.close()
    
    try:
        #Updates the users rememberMe choices
        with open('config.json', 'r') as json_file:
            config = json.load(json_file)
        choicesArray = config['rememberMe']
        choicesArray[0] = True
        choicesArray[1] = choice
        config['rememberMe'] = choicesArray
        with open('config.json', 'w') as json_file:
            json.dump(config, json_file, indent = 2)
    except Exception as err:
        print(f"Error has occured in rememberMe: {err}")   
    

def getRememberMe():
    """Gets the users decision on how they want their bot to be run on their PC

    Returns:
        bool: If they wanted the bot to remember their name
    """
    try:
        with open('config.json', 'r') as json_file:
            config = json.load(json_file)
    except Exception as err:
        print(f"Error has occured in getRememberMe block 1: {err}")

    try:
        choice = config['rememberMe']
        return choice
    except Exception as Err:
        print(f"Error has occured in getRememberMe block 3: {err}")
        
def nameInitalizer():
    """Initalizes how the user wants the bot to operate on their machine
        Version 1: The bot remembers the name
        Version 2: The bot takes in the name on every start up
    """
    try:
        if not getRememberMe()[0]: #Checks if the remember user pop up has shown for the user
            getNameGui()
            getRememberMeGui() 
        elif getRememberMe()[0] and not getRememberMe()[1]:
            getNameGui()
    except Exception as err:
        print(f"Error has occured in nameInitializer: {err}")

def start_driver():
    """Starts the driver, goes to my.umbc.edu and full screens it. Creates timeout object.

    Returns:
        Driver and timeout object
    """

    try:
        # Initiate the driver and go to my umbc
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        driver.maximize_window()
        driver.get('https://my.umbc.edu/')
    except Exception as err:
        print("Cannot open Edge. Error:", err)
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
        time.sleep(.2)

        # Inserts time in data
        inputElementIN.send_keys(data[i][1])
        time.sleep(.2)

        # Inserts time out data
        inputElementOUT = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_OUT$" + str(i))))
        time.sleep(.2)
        inputElementOUT.send_keys("null")
        time.sleep(.2)
        inputElementOUT = wait.until(EC.element_to_be_clickable((By.ID, "UM_TIME_OUT$" + str(i))))
        inputElementOUT.send_keys(data[i][2])
        time.sleep(.2)


def close_program(keep_alive):
    """Keeps program open for a specific amount of time

    Args:
        keep_alive: seconds that the program should stay open after all instructions complete
    """

    temp = 0

    while (temp < keep_alive):
        temp += 1
        time.sleep(1)