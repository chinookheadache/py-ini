"""
Reading INI file to customize administative returns
Nov 26 2021
by Zac Fawcett

This script is designed to present a user controllable menu
that  shows useful admin information. Furthermore it is coded to get
variable values and formatting cues from an INI file.
The menu gives the option to:

    1.prints to screen all accounts and their group associations
      sorted alphabetically by account name (variable through INI)

    2.prints to screen system logs from /var/log/
      based on the criteria specified in the projectini file

    3 Generate a report containing: Computername, Formatted date/time,
      Results from option 1 and results from option 2, all written to
      a file path specified in the INI file.

Pseudo Code
import needed modules
create constant variable for ini file path

create  first function that reads ini using configobj seperating out variables
by name and returning a dictionary

Function 2 will call the dictonary from function one
then using the .get('variable') will call and assign the variables needed to
display accounts and groups
Compare the variables against the accounts and groups list to achieve
desired customization

Function 3 will call the dictonary from function one
then using the .get('variable') method will call and assign the variables needed to
display log file entries containing keywords and within a date range from the ini

function 4 will stamp a header with date, machine name and time into the output path
specified in the ini then call functions 2 and 3 redirecting their outputs to the file

A menu will coninually loop with a while True loop. It will ask for user input and have error
handling for incorrect inputs. Upon the enter key being struck the program will terminate
"""
# import required modules
import sys
import os
import pwd
import grp
import datetime
import tkinter
from tkinter import messagebox # this module displays a custom pop up message

 
# Constant Variable for the path to the INI file holding configuration info
INFILE = "projectini"


# Function that reads INI file and returns an callable dictionary for
# assigning the variables needed to customize the other functions returns
# Learned about the configobj module from Instructor in class and found how to use it here:
# https://configobj.readthedocs.io/en/stable/configobj.html#the-config-file-format
# specifically sections 1.1.4.1 and 1.1.4.3
def ReadIni(filename):
    from configobj import ConfigObj
    config = ConfigObj(filename)
    configDict = {
        "outfile": (config['BASIC']['outFile']),
        "sortAccRev": (config['FILTER_ACCOUNTS']['sortAccountsReverse']),
        "sortAccCri": (config['FILTER_ACCOUNTS']['sortAccountsCriteria']),
        "linesAccDat": (config['FILTER_ACCOUNTS']['linesOfAccountsData']),
        
        "sortLogRev": (config['FILTER_LOGS']['sortLogsReverse']),
        "logTimeFrom": (config['FILTER_LOGS']['logTimeFrom']),
        "logTimeto": (config['FILTER_LOGS']['logTimeTo']),
        "logCriteria": (config['FILTER_LOGS']['logCriteria'])
        }
    return configDict

# Found the idea of using the get feature with a dictionary to define my
# variables from the INI file
# https://tutorialdeep.com/knowhow/get-dictionary-value-key-python/
# Menu function prints the menu that is looped giving the 3 function options
# as well as the option to press enter to exit
def Menu():
    print("1. System Accounts" + "\n")
    print("2. System Logs" + "\n")
    print("3. Generate Report" + "\n")
    print("Press Enter to Exit" + "\n")

# This function uses the dictionary created using the ReadIni function to
# assign variables from the INI. Then these variables are used to customize the printing of
# System accounts and the groups those accounts belong to
def Option1():
    
    try:
        # call the dictionary outputted from ReadIni function
        accountsDict = ReadIni(INFILE)
    except:
        print("Can't read INI config file, please check path")
    # assign variables related to the sorting of accounts from the INI
    sortAccountsReverse = accountsDict.get("sortAccRev")
    sortAccountsCriteria = accountsDict.get("sortAccCri")
    linesOfAccountsData = (accountsDict.get("linesAccDat"))
    try:
        accountInfo = pwd.getpwall()
    except:
        print("Error Reading pwd file")
    try:
        grpInfo = grp.getgrall()
    except:
        print("Error Reading Groups")
    try:
        print("System Accounts List" + "\n")
        print("--------------------" + "\n")
        print("Account Name".ljust(25) + "Groups".rjust(35) + "\n")
        singles = []
        multiples = []
        # Iterate through accounts and groups creating lists of accounts that
        # belong to single groups and ones that belong to multiple groups
        # then adding them together to be iterates through and printed
        for account in accountInfo:
            accountName = account.pw_name
            # get default group name
            groupID = account.pw_gid
            groupRecord = grp.getgrgid(groupID)
            singles.append(str(accountName.ljust(25)) + "          " + str(groupRecord.gr_name.rjust(25)))
            if (groupRecord.gr_name == ""):
                print("no group")
            # get other group membership
            for group in grpInfo:
                if accountName in group.gr_mem:
                    multiples.append(str(accountName.ljust(25)) + "          " + str(group.gr_name.rjust(25)))
    except:
         print("Error reading groups and accounts")
    combined = singles + multiples
    # Handling the sorting of the final list, whether it is reversed or not
    # This is designated in the INI
    if (sortAccountsReverse == ("True")):
        combined.sort(reverse = True)
    if (sortAccountsReverse == ("False")):
        combined.sort()
    # Handling if the INI wants a certain number of lines only printed or all available
    if (linesOfAccountsData == "All" and sortAccountsCriteria == "None"):
        for line in combined:
                print(line)
    if (linesOfAccountsData == "All"):
        for line in combined:
            if (sortAccountsCriteria in line):
                print(line)
    i = 0
    if (linesOfAccountsData != "All" and sortAccountsCriteria == "None"):
        for line in combined:
            print(line)
            i = i + 1
            if (i >= (int(linesOfAccountsData))):
                break
    if (linesOfAccountsData != "All"):
        for line in combined:
            if (sortAccountsCriteria in line):
                print(line)
                i = i + 1
                if (i >= (int(linesOfAccountsData))):
                    break
    print("\n")

# This function uses the dictionary created using the ReadIni function to
# assign variables from the INI. Then these variables are used to customize the printing of
# syslog files, based on things like a range of dates/times and keywords
def Option2():
    try:
        logsDict = ReadIni(INFILE)
    except:
        print("Can't read INI config file, please check path")
    sortLogsReverse = logsDict.get("sortAccRev")
    logTimeFrom = logsDict.get("logTimeFrom")
    logTimeTo = logsDict.get("logTimeto")
    logCriteria = logsDict.get("logCriteria")
    from datetime import datetime
    # Append the command that calls the log file with the criteria specified in INI
    # Then create an object that hold the output
    try:
        syslog = os.popen("cat /var/log/syslog | grep " + logCriteria)
    except:
        print("Error reading syslog, check for file corruption or path spelling.")
    # Split the log output object by line into a list
    splitlog = syslog.read().splitlines()   
    logFinal = []
    # Converting the dates from the Ini into datetime objects for comparing a range against logfile
    # These skills were learned from these sites:
    # https://stackoverflow.com/posts/466376/revisions  (by user Ismail.H)
    # The format of the datetime objects from: https://strftime.org/
    timeFrom = datetime.strptime(logTimeFrom, '%b %d %H:%M:%S')
    timeTo = datetime.strptime(logTimeTo, '%b %d %H:%M:%S')
    print("Log files for: " + logCriteria + " from " + logTimeFrom + " to " + logTimeTo + "\n")
    # To convert the splitlog list into a string usable by datetime
    # I used methods from the site:
    # https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
    # Specifically method 4
    for lines in splitlog:
        lines = lines.rstrip()
        split = lines.split()[:3]
    # Had to split the original variable through multiple ways in order
    # to get it usable for the range comparison. More list to string methods were found at
    # https://www.jquery-az.com/3-ways-convert-python-list-string-join-map-str/
    # Specifically the section "Another way: using the map function"
        moresplit = ' '.join(map(str, split))
        mostsplit = datetime.strptime(moresplit, '%b %d %H:%M:%S')
        # If a line in the log entry has a date object between the values from
        # the ini then it is added into the final log line list
        if (mostsplit >= timeFrom and mostsplit <= timeTo):
            logFinal.append(lines)
    if (sortLogsReverse == ("True")):
        logFinal.sort(reverse = True)
    if (sortLogsReverse == ("False")):
        logFinal.sort()
    for line in logFinal:
        print(line + "\n")
       
# Function that executes the Accounts and Log functions before it but redirects the outputs
# to a file specified in the INI. Also adds a header with machine name, date and time.
def Option3():
    outDict = ReadIni(INFILE)
    OUTFILE = outDict.get('outfile')
    machName = os.popen("hostname")
    machNameForm = machName.read()
    # Using the datetime module I am able to call the current time formatted
    # in the way i wanted, These skills were learned from:
    # https://www.tutorialspoint.com/How-to-get-formatted-date-and-time-in-Python
    currently = datetime.datetime.now()
    formDate = currently.strftime('%b-%d-%Y')
    try:
        # This code redirects the output from then the other two options are called
        # Normally they would print to screen but this code directs them to print to
        # the outfile specified in the INI. These methods are gone over at:
        # https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
        # Specifically post #231 in the answers section by user jfs
        from contextlib import redirect_stdout
        with open(OUTFILE, "w") as writer:
            with redirect_stdout(writer):
                
                formTime = currently.strftime('%H:%M:%S')
                print("Machine Name: " + machNameForm)
                print("Recorded on: " + formDate + " at " + formTime + "\n")
                Option1()
                Option2()
                
    except:
        print("Cant Print Log File")
    
        
    

while True:
# Here the menu function is looped as it asks for the users input
# Error handling is implemented for if the user enters a useless input
    Menu()
    choice = input("Enter choice or press enter to exit: ")
    print("\n")
    if (choice != "1" and choice != "2" and choice != "3" and choice != ""):
        print("***INVALID CHOICE ENTRY***")
        print("Enter a choice from the menu or press enter to exit" + "\n")
    if choice == "1":
        try:
            Option1()
        except:
            # when a user entered option fails a popup will display
            # more detailed error messages will also show on the terminal line
            # Learned about tkinter in class from instructor Marcel Tozser and from this resource:
            # https://pythonguides.com/python-tkinter-messagebox/
            messagebox.showerror("error", "Can't print accounts, please check paths")
    if choice == "2":
        try:
            Option2()
        except:
            messagebox.showerror("error", "Can't print logs, please check path or logs for corruption")
    if choice == "3":
        try:
            Option3()
        except:
            messagebox.showerror("error", "Failed to write output")
            
    if choice == "":
        print("User chose to exit program.... Goodbye!")
        break
sys.exit()












































































