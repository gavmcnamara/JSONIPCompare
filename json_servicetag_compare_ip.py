import json 
import requests
import sys, os
from datetime import date, datetime, timedelta 

# changed dir to file locations
path = os.path.dirname(__file__)
os.chdir(path)

# Create date that returns last two days
today = date.today()
yesterday = today - timedelta(days=1)
two_days = today - timedelta(days=2)

# if file is two days old move to archive
files = os.listdir('.')
for f in files:
    if f == 'azure_gov_ip_' + two_days.strftime('%Y-%m-%d') + '.json':
        os.rename('azure_gov_ip_' + two_days.strftime('%Y-%m-%d') + '.json',
                    'archive/azure_gov_ip_' + two_days.strftime('%Y-%m-%d' + '.json'))

# creates json file that stores last file object
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

path = '/'
fileName = 'check_last_file'

today = datetime.today()
yesterday = today - timedelta(days=1)

data = {}
data['lastAddressPrefixFile'] = 'azure_gov_ip_' + yesterday.strftime('%Y-%m-%d') + '.json'
writeToJSONFile(path, fileName, data)

# download json file from website
#url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=57063"
url= "https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20180620.json"
#'https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_[0-2][0-1][0-2][0-1][0-9][0-9][0-9].json'
r = requests.get(url)

# replaces last file with latest file
def checkLastFile():   
    # opens file with json object of last opened file
    metadataFile = open('check_last_file.json', 'r')
    metadata = json.loads(metadataFile.read())

    # reads data to get last json file used
    lastConfigurationFile = open(metadata['lastAddressPrefixFile'], 'r')
    lastConfiguration = json.loads(lastConfigurationFile.read())

    # do code to compare last configuration
    latestFileName = 'azure_gov_ip_{}.json'.format(date.today())
    latestConfigurationFile = open(latestFileName, 'w')
    latestConfigurationFile.write(json.dumps(latestFileName))

    # stores latest json file as a string
    metadata['lastAddressPrefixFile'] = latestFileName
    metadataFile_ = open('check_last_file.json', 'w')
    metadataFile_.write(json.dumps(latestFileName))
checkLastFile()

# create log file with results
sys.stdout = open('log.txt', 'w')

# compares last and latest json files
def json_compare():
    # create file with todays date
    with open('azure_gov_ip_{}.json'.format(date.today()), "wb") as code:
        download_file = code.write(r.content)

    # Find and read json file from yesterday   
    with open(r'azure_gov_ip_' + yesterday.strftime('%Y-%m-%d') +'.json') as fh:
        last_file = json.load(fh)      

    # Find and read json file from today
    with open(r'azure_gov_ip_' + str(date.today()) + '.json') as fh:
        latest_file = json.load(fh)

    # Parses through json files if last file equals latest file on SQL.USGovVirginia
    for last in last_file['values']:
        for latest in latest_file['values']:
            if last['name'] == 'Sql.USGovVirginia' and latest['name'] == 'Sql.USGovVirginia':
                if last['properties']['changeNumber'] == latest['properties']['changeNumber']:
                    print("There are no changes: SQL.USGovVirginia")
                    print('')
                else:
                    # prints diff of two lists
                    print("There are changes: SQL.USGovVirginia")
                    last_ips = list(set(last['properties']['addressPrefixes']) - set(latest['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    latest_ips = list(set(latest['properties']['addressPrefixes']) - set(last['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(last_ips))
                    print("Added: " + str(latest_ips))
                    print('')

    # Parses through json files if last file equals latest file on Storage.USGovVirginia
    for last in last_file['values']:
        for latest in latest_file['values']:
            if last['name'] == 'Storage.USGovVirginia' and latest['name'] == 'Storage.USGovVirginia':
                if last['properties']['changeNumber'] == latest['properties']['changeNumber']:
                    print("There are no changes: Storage.GovVirginia")
                    print('')
                else:
                    # prints diff of two lists 
                    print("There are changes: Storage.USGovVirginia")
                    last_ips = list(set(last['properties']['addressPrefixes']) - set(latest['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    latest_ips = list(set(latest['properties']['addressPrefixes']) - set(last['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(last_ips))
                    print("Added: " + str(latest_ips))
                    return last, latest
json_compare()
sys.stdout.close()

