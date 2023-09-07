
# Time Sheet Bot UMBC

This bot will input your work hours and days based on the DoIT Student Desktop Work Calendar.   

**YOU ARE RESPONSIBLE FOR CHECKING DAYS/HOURS ON THE TIME SHEET BEFORE TURNING IN YOUR TIMESHEET**  

[See a video on how the bot works!](https://www.youtube.com/watch?v=OBOn-c57OLM)

## How to use the bot
### Prerequisites:
* Ensure **Python 3** is installed on your machine. If not, download it [here](https://www.python.org/downloads/). To see if python is on your machine, go to your terminal and type ``python --version``. If ``Python 3.xx.x`` does not appear, you do not have Python or you do not have the correct version of Python.
* Installing **Git** will make the installation process quicker (though it is not necessary). Install git [here](https://git-scm.com/downloads). To see if you have git, go to your terminal and type ``git --version``. If ``git version ...`` does not appear, you do not have Git.
* You must have **Google Chrome** installed for this application to work. Install chrome [here](https://www.google.com/chrome/).

### Step 1: Install the Program
* **With Git**: Within your terminal, go to where you want your application to be stored and enter ``git clone https://github.com/Dylan-Wimoth/TimeSheetBot.git``
* **Without Git**: Click the green ``<> Code`` button on the top right of the repository. Click ``Download ZIP``. Once downloaded, extract the ZIP. 

### Step 2: Installing Requirements
From your terminal, go inside the TimeSheetBot folder. To confirm you're in the correct directory:
* **Mac**: type ``ls`` into the terminal. You should see ``.gitignore``, ``calendar_integration.py``, ``main.py``, ``README.md``, ``requirements.txt``, and ``TimeSheetBot.py``
* **Windows**: type ``dir`` into the terminal. You should see ``.gitignore``, ``calendar_integration.py``, ``main.py``, ``README.md``, ``requirements.txt``, and ``TimeSheetBot.py``

Once in the correct folder, type ``python3 -m pip install -r requirements.txt`` into the terminal. This will install any dependencies the program needs to run.

### Step 3: Credentials
In order to use Google's API (which is required with this application), you must request a .json credential file from a person who has it. Until more students use the application and have the .json on their computer, ask Dylan Wilmoth for it.   

**DO NOT SHARE THE CREDENTIALS WITH ANYONE OUTSIDE OF DESKTOP SUPPORT.**

Once you have the ``credentials.json`` file, move the file into the TimeSheetBot directory with the other files mentioned above.

### Step 4: Running the Program
Once the dependencies are installed and ``credentials.json`` is in the file directory, enter ``python3 main.py`` into the terminal. The bot should start working. The first startup for the bot may take a little bit of a time to open. In addition, for the first time set up, you will be asked to log into your Google Account. Make sure you use your UMBC account. See video above for instructions on how to use the bot. 

## Errors
If any errors occur with the bot, message ``Dylan Wilmoth`` on Webex. Include a description of what happen and the events that lead up to the crash. If possible, include the error message as well. 

## Owner's Guide
Learn how to maintain the bot [here](https://docs.google.com/document/d/149sX6eMVgpynhd_m3gGFE3ysSs7btKHZtgD0V1w3xsM/edit?usp=sharing)