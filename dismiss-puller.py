import requests, json, time, csv
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Provide Prisma Cloud Origin Keys
origin_accessKey = ""
origin_secretKey = ""

#Specify API address to get dismissed alerts on original tenant - https://api.docs.prismacloud.io/reference#get-alerts-v2, this is pulling dismissed alerts for the past year
apiUrl = "https://api3.prismacloud.io/v2/alert?timeType=relative&timeAmount=1&timeUnit=year&detailed=true&alert.status=Dismissed"

#Auth for origin
origin_loginUrl = "https://api3.prismacloud.io/login"
origin_loginPayload = '{"username" : "' + origin_accessKey + '", "password" : "' + origin_secretKey + '"}'
headers = {'accept': "application/json; charset=UTF-8",'content-type': "application/json"}
#Get JWT Token for origin login
loginResponse = requests.request("POST", origin_loginUrl, data=origin_loginPayload, headers=headers, verify=False)
jsonResponse = loginResponse.json()
#Extract token from origin json
token = jsonResponse['token']

#Build headers and data for origin
headers = {'content-type': "application/json", 'x-redlock-auth': token}
payload={}

#Get Dimissed Alerts on origin
response = requests.request("GET", apiUrl, headers=headers, data=payload)

#Get Resources and associated Policies that are Dismissed on the origin tenant. Output to CSV to be used for comparison.
response = json.loads(response.text)

#Build CSV for Origin
run = 0
with open('origin_dismissed.csv','w') as f1:
  writer=csv.writer(f1)
  for response in response["items"]:
   policyName = (response["policy"]["name"])
   rrn = (response["resource"]["name"])
   policyName = {'Policy Name': [policyName], 'Resource Name': [rrn]}
   df = pd.DataFrame(policyName)
   if run == 0:
     df.to_csv('origin_dismissed.csv', mode = 'a', index=False)
     run = run + 1
   if run != 0:
     df.to_csv('origin_dismissed.csv', mode = 'a', header=None, index=False)
