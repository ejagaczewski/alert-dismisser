import requests, json, csv, os
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Set Destination Tenant Keys
dest_accessKey = ""
dest_secretKey = ""

#Specify destination tenant API address to compare alerts to
dest_apiUrl = "https://api2.prismacloud.io/v2/alert?timeType=relative&timeAmount=1&timeUnit=year&detailed=true&alert.status=Open"

#Auth for dest
dest_loginUrl = "https://api2.prismacloud.io/login"
dest_loginPayload = '{"username" : "' + dest_accessKey + '", "password" : "' + dest_secretKey + '"}'
dest_headers = {'accept': "application/json; charset=UTF-8",'content-type': "application/json"}
dest_loginResponse = requests.request("POST", dest_loginUrl, data=dest_loginPayload, headers=dest_headers, verify=False)
dest_jsonResponse = dest_loginResponse.json()
dest_token = dest_jsonResponse['token']

#Build headers and data for destination
dest_headers = {'content-type': "application/json", 'x-redlock-auth': dest_token}
dest_payload={}

dest_response = requests.request("GET", dest_apiUrl, headers=dest_headers, data=dest_payload)

#Get Resources and associated Policies on dest origin tenant. Output to CSV to be used for comparison.
dest_response = json.loads(dest_response.text)

#Get Alerts CSV and build from Destination
dest_run = 0
with open('dest_alerts.csv','w') as f2:
  dest_writer=csv.writer(f2)
  for dest_response in dest_response["items"]:
   dest_policyName = (dest_response["policy"]["name"])
   dest_rrn = (dest_response["resource"]["name"])
   dest_id = (dest_response["id"])
   dest_policyName = {'Policy Name': [dest_policyName], 'Resource Name': [dest_rrn], 'Alert ID': [dest_id]}
   df = pd.DataFrame(dest_policyName)
   if dest_run == 0:
     df.to_csv('dest_alerts.csv', mode = 'a', index=False)
     dest_run = dest_run + 1
   if dest_run != 0:
     df.to_csv('dest_alerts.csv', mode = 'a', header=None, index=False)

#Compare Origin and Destination Alerts and Output Matches

a = pd.read_csv("origin_dismissed.csv")
b = pd.read_csv("dest_alerts.csv")
merged = pd.merge(a, b, on=['Policy Name'], how='outer')
#merged.to_csv('todismiss.csv', mode = 'a',index=False)
df = pd.read_csv('todismiss.csv')
#Find matches and output to CSV matches.csv
df = df.loc[df['Resource Name_x'] == df['Resource Name_y']]
df.to_csv('matches.csv')

#Grab Alert IDs from matches.csv and dismiss them
df = pd.read_csv('matches.csv')
alertIds = df['Alert ID'].to_list()
print(alertIds)

dismiss_url = "https://api2.prismacloud.io/alert/dismiss"

i=0
for x in alertIds:
    payload = {"alerts":['' + alertIds[i] + ''],"policies":[],"filter":{"filters":[{"operator":"=","name":"alert.id","value":'' + alertIds[i] + ''},{"operator":"=","name":"alert.status","value":"open"}],"timeRange":{"type":"to_now","value":"epoch"}},"dismissalNote":"test"}
    dismiss_response = requests.request("POST", dismiss_url, json=payload, headers=dest_headers)
    print(dismiss_response.json)
    i = i + 1

#Cleanup
os.remove("todismiss.csv")
os.remove("dest_alerts.csv")
