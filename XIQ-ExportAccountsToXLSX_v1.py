#!/usr/bin/env python3
import getpass  ## import getpass is required if prompting for XIQ crednetials
import json
import requests
from colored import fg
import os
import pandas as pd
from pprint import pprint as pp
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl') # Suppress specific warnings


########################################################################################################################
## written by:       Mike Rieben
## e-mail:           mrieben@extremenetworks.com
## date:             November, 2024
## version:          1.0
## tested versions:  Python 3.11.4, XIQ 24r6 (November 2024)
########################################################################################################################
## This script ...  See README.md file for full description 
########################################################################################################################
## ACTION ITEMS / PREREQUISITES
## Please read the README.md file in the package to ensure you've completed the required and optional settings below
## Also as a reminder, do not forget to install required modules:  pip install -r requirements.txt
########################################################################################################################
## - ## two pound chars represents a note about that code block or a title
## - # one pound char represents a note regarding the line and may provide info about what it is or used for
## - There are single # pound char so the VScode will allow for collapsing code blocks e.g. #regsion - note about begin or end code block
########################################################################################################################


#region - Begin user settings section
## AUTHENTICATION Options:  Uncomment the section you wish to use whie other sections remain commented out
## 1) Static Username and password, must have empty token variable (Uncomment 3 total lines below). Enter values for username and password after uncommenting.
# XIQ_Token = ""
# XIQ_username = "name@contoso.com"  # Enter your ExtremeCloudIQ Username "xxxx"
# XIQ_password = "<password>"  # Enter your ExtremeCLoudIQ password "xxxx"

## 2) Prompt user to enter credentials, must have empty token variable (Uncomment 4 total lines below), simply uncomment - no entries required
XIQ_Token = ""
print(f'{fg(6)}\nEnter your XIQ login credentials ')
XIQ_username = input(f'{fg(6)}Email: ')
XIQ_password = getpass.getpass(f'{fg(6)}Password: ')

## 3) TOKEN generation from api.extremecloudiq.com (Swagger). Must have empty username and password variables (Uncomment 3 total lines below).  Enter XIQ Token within "" only.
# XIQ_Token = "XXXXXXXXXXXX"
# XIQ_username = ""
# XIQ_password = ""
##Authentication Options END

##User defined variables as outlined in README documentation
filename = 'XIQ-AccountExport.xlsx' #<-- If you change it here, remember to also change the template file name.
#endregion ##end user settings section

#region #************************* No user edits below this line required ************************************************************************************
##Global Variables-------------------------------------------------------------------------------------------------------------------------------------
URL = "https://api.extremecloudiq.com"  ##XIQ's API portal
headers = {"Accept": "application/json", "Content-Type": "application/json"}
PATH = os.path.dirname(os.path.abspath(__file__))  #Stores the current Python script directory to write the file to
colorWhite = fg(255) ##DEFAULT Color: color pallete here: https://dslackw.gitlab.io/colored/tables/colors/
colorRed = fg(1) ##RED
colorGreen = fg(2) ##GREEN
colorPurple = fg(54) ##PURPLE
colorCyan = fg(6) ##CYAN
colorOrange = fg(94) ##ORANGE
colorGrey = fg(8)  ##GREY
#endregion #end Global Variables---------------------------------------------------------------------------------------------------------------------------------

##Use provided credentials to acquire the access token if none was provided-------------------------
def GetaccessToken(XIQ_username, XIQ_password):
    url = f'{URL}/login'
    payload = json.dumps({"username": XIQ_username, "password": XIQ_password})
    response = requests.post(url, headers=headers, data=payload)
    if response is None:
        log_msg = "ERROR: Not able to login into ExtremeCloudIQ - no response!"
        raise TypeError(log_msg)
    if response.status_code != 200:
        log_msg = f"Error getting access token - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        raise TypeError(log_msg)
    data = response.json()
    if "access_token" in data:
        headers["Authorization"] = "Bearer " + data["access_token"]
        return 0
    else:
        log_msg = "Unknown Error: Unable to gain access token"
        raise TypeError(log_msg)
##end Use provided credentials....--------------------------------------------------------------

##Get and Store All Account Users
def GetAllAccountUsers():
    url = URL + "/account/viq"
    try:
        rawList = requests.get(url, headers=headers, verify = True)
    except ValueError as e:
        print('script is exiting...')
        raise SystemExit
    except Exception as e:
        print('script is exiting...')
        raise SystemExit
    if rawList.status_code != 200:
        print('Error exiting script...')
        print(rawList.text)
        raise SystemExit
    jsonDump = rawList.json()
    vhmId = jsonDump['vhm_id']
    ownerId = jsonDump['owner_id']
    #-------------------------------
    url = URL + "/account/home"
    try:
        rawList = requests.get(url, headers=headers, verify = True)
    except ValueError as e:
        print('script is exiting...')
        raise SystemExit
    except Exception as e:
        print('script is exiting...')
        raise SystemExit
    if rawList.status_code != 200:
        print('Error exiting script...')
        print(rawList.text)
        raise SystemExit
    jsonDump = rawList.json()
    accountName = jsonDump['name']
    #-------------------------------
    page = 1
    pageCount = 1
    pageSize = 100
    foundUsers = []
    while page <= pageCount:
        url = URL + "/users?page=" + str(page) + "&limit=" + str(pageSize)
        try:
            rawList = requests.get(url, headers=headers, verify = True)
        except ValueError as e:
            print('script is exiting...')
            raise SystemExit
        except Exception as e:
            print('script is exiting...')
            raise SystemExit
        if rawList.status_code != 200:
            print('Error exiting script...')
            print(rawList.text)
            raise SystemExit
        jsonDump = rawList.json()
        for users in jsonDump['data']:
            newData = {}
            newData['ID'] = users['id']
            newData['LOGIN NAME'] = users['login_name']
            newData['FIRST NAME'] = users['first_name']
            newData['LAST NAME'] = users['last_name']
            newData['DISPLAY NAME'] = users['display_name']
            newData['USER ROLE'] = users['user_role']
            newData['VHM ID'] = vhmId
            newData['OWNER ID'] = ownerId
            newData['ACCOUNT NAME'] = accountName
            foundUsers.append(newData)
        pageCount = jsonDump['total_pages']
        print(f"{colorPurple}\nCompleted page {page} of {jsonDump['total_pages']} collecting VIQ User Accounts")
        page = jsonDump['page'] + 1
    return foundUsers

##This is the start of the program
def main():
    ##Test if a token is provided.  If not, use credentials.
    if not XIQ_Token:
        try:
            login = GetaccessToken(XIQ_username, XIQ_password)
        except TypeError as e:
            print(e)
            raise SystemExit
        except:
            log_msg = "Unknown Error: Failed to generate token"
            print(log_msg)
            raise SystemExit
    else:
        headers["Authorization"] = "Bearer " + XIQ_Token
    ##Test if template file was found in the current directory which is required.
    if os.path.exists(filename): 
        print(f'{colorPurple}\nLocating the XLSX file in the current directory: {filename}')
        dfFromFile = pd.read_excel(filename, sheet_name='Template')
        print(f'{colorPurple}\nCurrent file contents: ')
        pp(dfFromFile) # Print XLSX file contents
        ##Go acquire every user in the VIQ
        accountUsers = GetAllAccountUsers()
        while True:
            user_input = input(f'{colorCyan}\nWould you like to replace or append file contents? <Replace>/Append/Cancel: ').strip().lower()
            if user_input == 'Replace' or user_input == 'replace' or user_input == 'R' or user_input == 'r' or user_input == '':
                accountUsers_df = pd.DataFrame(accountUsers)
                updated_df = accountUsers_df
                updated_df.to_excel(filename, sheet_name='Template', index=False)
                print(f'{colorGreen}\nXLSX file has been overwritten with the VIQ\'s account users: {filename}')
                break
            elif user_input == 'Append' or user_input == 'append' or user_input == 'A' or user_input == 'a':
                accountUsers_df = pd.DataFrame(accountUsers)
                updated_df = pd.concat([dfFromFile, accountUsers_df], ignore_index=True)
                updated_df.to_excel(filename, sheet_name='Template', index=False)
                print(f'{colorGreen}\nXLSX file has been appended with the VIQ\'s account users, not overwritten: {filename}')
                break
            elif user_input == 'Cancel' or user_input == 'C' or user_input == 'c':
                print(f'{colorPurple}\nCancelled... XLSX file was not altered: {filename}')
                break
            else:
                print(f"{colorRed}Invalid input. Please enter 'Replace' or 'R' or 'Append' or 'A'.")
        
        dfFromFile = pd.read_excel(filename, sheet_name='Template')
        pp(dfFromFile) # Print XLSX file contents

    else: #inform the user if the script can't find the XLSX file in the current directory
        print(f'{colorRed}\nABORT: File missing! You must copy the provided XSLX (from Github) into your current Python script directory!: {filename} \n')
        
##Python will see this and run whatever function is provided: xxxxxx(), should be the last items in this file
if __name__ == '__main__':
    main() ##Go to main function

##***end script***


