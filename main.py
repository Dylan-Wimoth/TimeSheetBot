from TimeSheetBot import close_program, insert_times, open_timesheet, start_driver, user_login, getName, nameInitalizer
from calendar_integration import generateToken, getEvents


def main():
    creds = generateToken()
    nameInitalizer()
    name = getName()
    driver, wait = start_driver()
    user_login(wait)
    start_date, end_date = open_timesheet(driver, wait)
    data = getEvents(start_date, end_date, name, creds)
    insert_times(wait, data)

    close_program(300)


if __name__ == "__main__":
    main()