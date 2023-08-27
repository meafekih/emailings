import requests
import json
import requests
import base64


url = 'http://127.0.0.1:8000/api/'
headers = {
    #'Content-Type': 'multipart/form-data; boundary=JVU6Re79Sw53jKG4i6LwQENx2bfBEXQM',    
    #'Content-Type': 'application/graphql',
    #'Authorization': 'Bearer your-access-token',
    #'Content-Type': 'application/json',
    #'Accept': '*/*',
}

query = '''
mutation sendEmail ($attachment: Upload) {
  sendingEmail(
    userId:1,
    emailTo:"mea.fekih@gmail.com",
    subject:"Testing Sending4",
    content:"Sending Email From Graphql4",
    attachments: [$attachment])
  { success }
}
'''

 


variables = {
    'attachments': []
}
 
with open('Requests/docs/attachment.pdf', 'rb') as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')
    variables['attachments'].append(image_data)

request_payload = {
    'query': query,
    'variables': variables,
}

response = requests.post(url,headers=headers, json=request_payload)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(response.text)