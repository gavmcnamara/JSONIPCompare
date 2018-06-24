import json 
import requests
import sys, os
from datetime import date, datetime, timedelta

# changed dir to file locations
path = os.path.dirname(__file__)
os.chdir(path)

# creates json file that stores latest file object
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

path = '/'
fileName = 'check_last_file'

today = datetime.today()
yesterday = today - timedelta(days=2)
print(today)
print(yesterday)

data = {}
data['lastAddressPrefixFile'] = 'archive/azure_gov_ip_' + yesterday.strftime('%Y-%m-%d') + '.json'
writeToJSONFile(path, fileName, data)

# download json file from website
#url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=57063"
url= "https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20180620.json"
r = requests.get(url)
print("downloading")

def checkLastFile():
    # opens and reads file with json object
    metadataFile = open('check_last_file.json', 'r')
    metadata = json.loads(metadataFile.read())

    # reads data from json to get last json file used
    lastConfigurationFile = open(metadata['lastAddressPrefixFile'], 'r')
    lastConfiguration = json.loads(lastConfigurationFile.read())
    #print(lastConfiguration)

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

# Create date that returns yesterday
today = date.today()
yesterday = today - timedelta(days=2)

def json_compare():

    # create file with todays date
    with open('azure_gov_ip_{}.json'.format(date.today()), "wb") as code:
        file_c = code.write(r.content)

    # Find and read json file from yesterday   
    with open(r'azure_gov_ip_' + yesterday.strftime('%Y-%m-%d') + '.json') as fh:
        last_file = json.load(fh)

    # Find and read json file from today
    with open(r'azure_gov_ip_' + str(date.today()) + '.json') as fh:
        latest_file = json.load(fh) 
            
    # Parses through json files to determine if file a equals file b for SQL.USGovVirginia
    for last in last_file['values']:
        for latest in latest_file['values']:
            if last['name'] == 'Sql.USGovVirginia' and latest['name'] == 'Sql.USGovVirginia':
                if last['properties']['changeNumber'] == latest['properties']['changeNumber']:
                    print("There are no changes: SQL.USGovVirginia")
                else:
                    # prints diff of two lists
                    print("There are changes: SQL.USGovVirginia")
                    last_ips = list(set(last['properties']['addressPrefixes']) - set(latest['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    latest_ips = list(set(latest['properties']['addressPrefixes']) - set(last['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(last_ips))
                    print("Added: " + str(latest_ips))
                    print('')
                    # return f_a['name'], f_b['name']

    # Parses through json files to determine if file a equals file b for Storage.USGovVirginia
    for last in last_file['values']:
        for latest in latest_file['values']:
            if last['name'] == 'Storage.USGovVirginia' and latest['name'] == 'Storage.USGovVirginia':
                if last['properties']['changeNumber'] == latest['properties']['changeNumber']:
                    print("There are no changes: Storage.GovVirginia")
                else:
                    # prints diff of two lists 
                    print("There are changes: Storage.USGovVirginia")
                    last_ips = list(set(last['properties']['addressPrefixes']) - set(latest['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    latest_ips = list(set(latest['properties']['addressPrefixes']) - set(last['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(last_ips))
                    print("Added: " + str(latest_ips))
                    return last['name'], latest['name']
    
json_compare()
sys.stdout.close()
