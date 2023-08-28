
# Time Sheet Bot UMBC

This bot will input your work hours and days based on user-specific data from a .txt file. This bot can ONLY be used on the week the timesheet is due.\
**YOU ARE RESPONSIBLE FOR CHECKING DAYS/HOURS ON THE TIME SHEET BEFORE TURNING THEM IN**

## How to use the bot
### Prerequisites:
* Ensure Python 3 is installed on your machine. If not, download it [here](https://www.python.org/downloads/). To see if python is on your machine, go to your terminal and type ``python --version``. If ``Python 3.xx.x`` does not appear, you do not have Python.
* Installing Git will make the installation process quicker (though it is not necessary). Install git [here](https://git-scm.com/downloads). To see if you have git, go to your terminal and type ``git --version``. If ``git version ...`` does not appear, you do not have Git.
* You must have chrome installed for this application to work. Install chrome [here](https://www.google.com/chrome/).

### Step 1: Install the Program
* **With Git**: Within your terminal, go to where you want your application to be stored and enter ``git clone https://github.com/Dylan-Wimoth/TimeSheetBot.git``
* **Without Git**: Click the green ``<> Code`` button on the top right of the repository. Click ``Download ZIP``. Once downloaded, extract the ZIP. 

### Step 2: Filling out timesheet.txt
timesheet.txt is used to fill in your weeky hours. Open the timesheet.txt file that you downloaded in Step 1. Inside, you will see an example of a schedule. The example goes as follows:\
``TIME_IN`` ``TIME_OUT`` ``DAY_OF_THE_WEEK``

Each entry is separated by a new line.   
Make sure TIME_IN and TIME_OUT contain AM or PM at the end of it.   
For the DAY_OF_THE_WEEK, input as follows:
* Monday = 1
* Tuesday = 2
* Wednesday = 3
* Thursday = 4
* Friday = 5

Example from included timesheet.txt file:   
* Monday: 11:30AM -> 2:15PM becomes ``11:30AM 2:15PM 1``
* Monday: 4:00PM -> 5:15PM becomes ``4:00PM 5:15PM 1``
* Tuesday: 12:00PM -> 5:45PM becomes ``12:00PM 5:45PM 2``
* Wednesday: 11:30AM -> 2:15PM becomes ``11:30AM 2:15PM 3``
* Wednesday: 4:00PM -> 5:15PM becomes ``4:00PM 5:15PM 3``
* Thursday: 12:00PM -> 6:00pm becomes ``12:00PM 6:00pm 4``

**Once finished, save the .txt file**

## Step 3: Installing Requirements
From your terminal, go inside the TimeSheetBot folder. To confirm you're in the correct place:
* Mac: type ``ls`` into the terminal. You should see ``requirements.txt``, ``timesheet.txt``, and ``TimeSheetBot.py``
* Windows: type ``dir`` into the terminal. You should see ``requirements.txt``, ``timesheet.txt``, and ``TimeSheetBot.py``

Once in the correct folder, type ``python3 -m pip install -r requirements.txt`` into the terminal. This will install any dependencies the program needs to run.

## Step 4: Running the Program
Once the dependencies are installed, enter ``python3 TimeSheetBot.py`` into the terminal. The bot should start working. To ensure the bot is working correctly, these events should happen (in order):
* A chrome window opens (this may take awhile when running for the first time)
* A myUMBC login page opens (you must log in manually)
* The timesheet webpage will open and data from timesheet.txt will start to be inserted

## Errors
If any errors occur with the bot, message ``Dylan Wilmoth`` on Webex. Include a description of what happen and the events that lead up to the crash. If possible, include the error message as well. 
