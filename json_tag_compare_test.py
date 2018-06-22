import json 
import requests
import sys, os
from datetime import date
import glob

# changed dir to file locations
path = os.path.dirname(__file__)
os.chdir(path)

# download json file from website
#url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=57063"
url= "https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20180620.json"
r = requests.get(url)
print("downloading")
# create file with todays date
with open('azure_gov_ip_{}.json'.format(date.today()), "wb") as code:
    file_c = code.write(r.content)

# create log file with results
sys.stdout = open('log1.txt', 'w')

def json_compare():

    # Find and read json files   
    with open(r'azure_gov_ip_2018-06-21.json') as fh:
        file_a = json.load(fh)
    with open(r'azure_gov_ip_' + str(date.today()) + '.json') as fh:
        file_b = json.load(fh) 
        
    # Parses through json files to determine if file a equals file b for SQL.USGovVirginia
    for f_a in file_a['values']:
        for f_b in file_b['values']:
            if f_a['name'] == 'Sql.USGovVirginia' and f_b['name'] == 'Sql.USGovVirginia':
                if f_a['properties']['changeNumber'] == f_b['properties']['changeNumber']:
                    print("There are no changes: SQL.USGovVirginia")
                else:
                    # prints diff of two lists
                    print("There are changes: SQL.USGovVirginia")
                    old_addresses = list(set(f_a['properties']['addressPrefixes']) - set(f_b['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    new_addresses = list(set(f_b['properties']['addressPrefixes']) - set(f_a['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(old_addresses))
                    print("Added: " + str(new_addresses))
                    print('')
                    # return f_a['name'], f_b['name']

    # Parses through json files to determine if file a equals file b for Storage.USGovVirginia
    for f_a in file_a['values']:
        for f_b in file_b['values']:
            if f_a['name'] == 'Storage.USGovVirginia' and f_b['name'] == 'Storage.USGovVirginia':
                if f_a['properties']['changeNumber'] == f_b['properties']['changeNumber']:
                    print("There are no changes: Storage.GovVirginia")
                else:
                    # prints diff of two lists 
                    print("There are changes: Storage.USGovVirginia")
                    old_addresses = list(set(f_a['properties']['addressPrefixes']) - set(f_b['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    new_addresses = list(set(f_b['properties']['addressPrefixes']) - set(f_a['properties']['addressPrefixes']))#[0].encode('UTF-8')
                    print("Removed: " + str(old_addresses))
                    print("Added: " + str(new_addresses))
                    return f_a['name'], f_b['name']
    
json_compare()
sys.stdout.close()
