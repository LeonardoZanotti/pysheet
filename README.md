# Pysheet
Python program to work with online sheets from Microsoft Excel.

## Prerequisites
First, you will need to generate the `credentials.json` file. Just read the `Prerequisites` topic from [this link](https://developers.google.com/sheets/api/quickstart/python) that you will end with a json file with your credentials (just rename this file to `credentials.json` before running the program).

You also need [Python 3.7+](https://www.python.org/) and the [Pip](https://pypi.org/project/pip/) of your Python version to run this software. With Python and Pip in hands, just install the dependencies with this command:
```bash
$ pip3.7 install python-decouple google-api-python-client google-auth-httplib2 google-auth-oauthlib    # use your pip version  
```

Then, just clone the `.env.example` file to `.env` and fill the `SPREADSHEET_ID` variable with your spreadsheet id (available in the URL of the sheet) like this:
```properties
SPREADSHEET_ID="<spreadsheet-id>"
```

Now, we are ready to go!

## Running the program
Just run the following command:
```bash
$ python3.7 pysheet.py      # use your python version
```

### Leonardo Zanotti