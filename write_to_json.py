import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

path = '/'
fileName = 'check_last_file'

data = {}
data['lastAddressPrefixFile'] = 'azure_gov_ip_2018-06-21.json'

writeToJSONFile(path, fileName, data)
