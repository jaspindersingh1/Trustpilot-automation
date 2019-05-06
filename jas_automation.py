import csv
import requests
import json
from requests.auth import HTTPBasicAuth

header = {'grant_type':'password' , 'username':USERNAME@HOST.COM, 'password':PASSWORD}
username= "ENCRYPTION_KEY"
password= "KEY"
res = requests.post(
    'https://request.com',
    auth=HTTPBasicAuth(username, password),
    data=header)
#print(res.content) #See content of the call result.

data = res.json()  # get response as parsed json (will return a dict)
auth_token = data.get('access_token')

if auth_token == None:
    print('No Access Token Received')
else:
    with open('BUIDQ2.csv', 'r') as f:
        ids = csv.reader(f)
        outfile = 'automationHist.csv'
        writeFile = open(outfile, 'w', encoding='utf-8', newline='')
        writer = csv.writer(writeFile, delimiter=',')
        writeFile.write('BUID')
        writeFile.write(',')
        writeFile.write('recipientName')
        writeFile.write(',')
        writeFile.write('recipientEmail')
        writeFile.write(',')
        writeFile.write('Source')
        writeFile.write(',')
        writeFile.write('createdTime')
        writeFile.write('\n')
        # print('test test ', ids)
        for row in ids:
            # print(row[0])
            buID = row[0]
            page = 1
            automatic_invitations = 'method=XYZ&method=XYZv1&method=SEGEMENT'
            url = 'https://requestURL.com' + buID + '/invitations?' + automatic_invitations + '&perpage=1000&token=' + auth_token + '&page=%s'
            print(url % page)
            response = requests.get(url % page)
            json_data = response.json()
            # print("THIS IS THE DATA:::", json_data)
            customer_array = []
            while json_data['invitations']:
                for invitation in json_data['invitations']:
                    recipientName = invitation['recipient']['name']
                    recipientEmail = invitation['recipient']['email']
                    sourceType = invitation['source']
                    autoDate = invitation['createdTime']
                    customer_array.append([buID, recipientName, recipientEmail, sourceType, autoDate])
                page +=1
                response = requests.get(url % page)
                json_data = response.json()
            if customer_array:
                writeFile.write(customer_array[-1][0]) #grab last element/ initial instance of automation, if any.
                writeFile.write(',')
                writeFile.write(customer_array[-1][1])
                writeFile.write(',')
                writeFile.write(customer_array[-1][2])
                writeFile.write(',')
                writeFile.write(customer_array[-1][3])
                writeFile.write(',')
                writeFile.write(customer_array[-1][4])
                writeFile.write('\n')
                print('FULL ROW::', customer_array[-1][0], customer_array[-1][1], customer_array[-1][2], customer_array[-1][3], customer_array[-1][4])
            else:
                writeFile.write(buID)
                writeFile.write(',')
                writeFile.write('No Automation Data')
                writeFile.write('\n')
                print(buID, 'No Automation Data')
            customer_array = []
print('All Done!')
