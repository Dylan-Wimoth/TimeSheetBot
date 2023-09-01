from TimeSheetBot import close_program, getStartDate, insert_times, open_timesheet, read_times, start_driver, user_login


def main():
    start_day = getStartDate()
    work_times = read_times()
    driver, wait = start_driver()
    user_login(wait)
    open_timesheet(driver, wait)
    insert_times(wait, work_times)

    close_program(300)

if __name__ == "__main__":
    main()