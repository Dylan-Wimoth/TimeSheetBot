import subprocess
import json

def setUp():
    """Installs the prerequisit python modules needed to run the TimeSheetBot
    """
    # Opens the json files where all of the modules are stored to read in and download them
    with open('requirements.json' , 'r') as json_file:
        dependencies = json.load(json_file)
    modules = dependencies['modules'] # Gets the module object from the json file
    if not dependencies['setUp']: # If flag is false then install modules from the json file
        try:
            for module in modules:
                subprocess.check_call(['pip', 'install', module])
            dependencies['setUp'] = True # Mark json file as run to prevent modules from installing on every run
            with open('requirements.json', 'w') as json_file:
                json.dump(dependencies, json_file, indent=2) # Update json file with Boolean flag as true
        except Exception as err:
            print(f"Error installing modules. Error: {err}")
    else:
        print('\033[92m' + "Requirements Downloaded Continuing to Bot" + '\033[0m') # Else print going to bot in green

if __name__ == "__main__":
    setUp()
