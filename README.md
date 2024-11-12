# XIQ Account User Export to XLSX
## Purpose
The ExtremeCloud IQ (XIQ) supports local and external account access to a VIQ.  This script will export all accounts to an XLSX template.  The primary purpose is to gather SSO account information since the username is auto generated via the ID Provider connection.

### Overview
1. Download all files from GitHub
2. Store all files in the same folder
3. Prepare your Python environment and run the script
4. Run script and review output by opening `XIQ-AccountExport.xlsx`
- By default you'll be prompted for XIQ credentials
- You'll be prompted to Replace(overwrite) or Append to the existing file contents
- Final results will be printed to screen and the XLSX template file will be updated

## Actions & Requirements
Install the required modules and generate an API Token to run script without user prompts.  If you need assistance setting up your computing environment, see this guide: https://github.com/ExtremeNetworksSA/API_Getting_Started

### Copy Required Files
You must copy from Github and place these files into the same folder:  `XIQ-ExportAccountsToXLSX_v#.py` & `requirements.txt` & `XIQ-AccountExport.xlsx`

### Install Modules
There are additional modules that need to be installed in order for this script to function.  They're listed in the *requirements.txt* file and can be installed with the command `pip install -r requirements.txt` if using `PIP`.  Store the *requirements.txt* file in the same directory as the Python script file.

## User Settings
Review the user controllable variables within `XIQ-ExportAccountsToXLSX_v#.py` which are outlined below.
Locate in the script "Begin user settings section" (around line 58)
  - **Authentication Options**:  [Token](#api-token), static entry for user/password, or prompt for credentials (Default).
  - `filename = "XIQ-AccountExport.xlsx"` < if you change this variable, remember to also change the file name to match.

### API Token - Optional (Prompt for credentials is default)
The default setup uses tokens for authentication to run without user prompts. Other options include hard-coded credentials (less secure) or prompting for credentials each time.

To run this script without user prompts, generate a token using `api.extremecloudiq.com`. Follow this [KB article](https://extreme-networks.my.site.com/ExtrArticleDetail?an=000102173) for details.

Brief instructions:

  1) Navigate to [API Swagger Site - api.extremecloudiq.com](https://api.extremecloudiq.com)
  2) Use the Authentication: /login API (Press: Try it out) to authenticate using a local administrator account in XIQ
  ```json
    {
    "username": "username@company.com",
    "password": "ChangeMe"
    }
  ```
  3) Press the Execute button
  4) Copy the `access_token` value (excluding the "" characters).  Note the expiration, it's 24 hours.
  ```json
    {
    "access_token": "---CopyAllTheseCharacters---",
    "token_type": "Bearer",
    "expires_in": 86400
    }
  ```
  5) Scroll to the top and press the Authorize button
  6) Paste contents in the Value field then press the **Authorize** button.  You can now execute any API's listed on the page.  **WARNING!** - You have the power to run all POST/GET/PUT/DELETE/UPDATE APIs and affect your live production VIQ environment.
  7) Scroll down to Authorization section > `/auth/apitoken` API (Press: Try it out)
  8) You need to convert a desired Token expiration date and time to EPOCH time:  Online time EPOCH converter:  https://www.epochconverter.com/
  
    EPOCH time 1748736000 corresponds to Sunday, June 1, 2025 12:00:00 AM
  
  9) Update the `description` and `expire_time` as you see fit.  Update the permissions as shown for minimal privileges to run only specific APIs for this script.
  ```json
    "description": "Token for API Script",
    "expire_time": 1764547200,
    "permissions": [
      "auth:r","logout","user:r","account:r"
    ]
  ```
  10) Press the **Execute** button
  11) Scroll down and copy the contents of the `access_token`:

    "access_token": "---ThisIsYourScriptToken---",

    ^^^ Use this Token in your script ^^^
    Locate `XIQ_Token` in your Python script and paste your token:

    XIQ_Token = "---ThisIsYourScriptToken---"

## Example XLSX Template:

| ID | LOGIN NAME | FIRST NAME | LAST NAME | DISPLAY NAME | USER ROLE | VHM ID | OWNER ID | ACCOUNT NAME |
| --: | --:| --:| --:| --:| --:| --:| --:| --:|

- These are the columns that are provided as default in the template along row 1
