from bs4 import BeautifulSoup
import re
import json 
import urllib2
import requests
import sys, os
from datetime import date, timedelta 

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
                    'archive/azure_gov_ip_' + two_days.strftime('%Y-%m-%d') + '.json')

# create log file with results or errors
sys.stdout = open('log_{}.txt'.format(date.today()), 'w')
for f in files:
    if f == 'log_' + yesterday.strftime('%Y-%m-%d') + '.txt':
        os.rename('log_' + yesterday.strftime('%Y-%m-%d') + '.txt',
                    'archive/log_' + yesterday.strftime('%Y-%m-%d') + '.txt')

# creates json file that stores last file object
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

path = '/'
fileName = 'check_last_file'

today = date.today()
yesterday = today - timedelta(days=1)

data = {}
data['lastAddressPrefixFile'] = 'azure_gov_ip_' + yesterday.strftime('%Y-%m-%d') + '.json'
writeToJSONFile(path, fileName, data)

# download json file from website
req = urllib2.Request('https://www.microsoft.com/en-us/download/confirmation.aspx?id=57063', headers={ 'User-Agent': 'Mozilla/5.0' })
html = urllib2.urlopen(req).read()
# using BeautifulSoup library to parse through html
soup = BeautifulSoup(html, 'html.parser')

# array to store the results
json_file =[]
for a in soup.findAll('a', href=True):
    # search for href links with ServiceTags in string
    if re.search('ServiceTags', a['href']):
        json_file = a['href']

# request link
r = requests.get(json_file)

# if url is invalid raise error
try:
   urllib2.urlopen(json_file)
except urllib2.HTTPError as err:
   if err.code == 404:
       print("Copy and paste new url.")
       print(err)

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
                    last_ips = list(set(last['properties']['addressPrefixes'])
                                 - set(latest['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    latest_ips = list(set(latest['properties']['addressPrefixes'])
                                 - set(last['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(last_ips))
                    print("Added: " + str(latest_ips))
                    print('')

    # Parses through json files if last file equals latest file on Storage.USGovVirginia
    for last in last_file['values']:
        for latest in latest_file['values']:
            if last['name'] == 'Storage.USGovVirginia' and latest['name'] == 'Storage.USGovVirginia':
                if last['properties']['changeNumber'] == latest['properties']['changeNumber']:
                    print("There are no changes: Storage.USGovVirginia")
                    print('')
                else:
                    # prints diff of two lists 
                    print("There are changes: Storage.USGovVirginia")
                    last_ips = list(set(last['properties']['addressPrefixes'])
                                 - set(latest['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    latest_ips = list(set(latest['properties']['addressPrefixes'])
                                 - set(last['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(last_ips))
                    print("Added: " + str(latest_ips))
                    return last, latest

    # Parses through json files if last file equals latest file on ServiceBus.USGovVirginia
    for last in last_file['values']:
        for latest in latest_file['values']:
            if last['name'] == 'ServiceBus.USGovVirginia' and latest['name'] == 'ServiceBus.USGovVirginia':
                if last['properties']['changeNumber'] == latest['properties']['changeNumber']:
                    print("There are no changes: ServiceBus.USGovVirginia")
                    print('')
                else:
                    # prints diff of two lists
                    print("There are changes: ServiceBus.USGovVirginia")
                    last_ips = list(set(last['properties']['addressPrefixes'])
                                 - set(latest['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    latest_ips = list(set(latest['properties']['addressPrefixes'])
                                 - set(last['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(last_ips))
                    print("Added: " + str(latest_ips))
                    print('')
json_compare()
sys.stdout.close()