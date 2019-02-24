import http.client
import json

conn = http.client.HTTPSConnection('www.httpbin.org')

headers = {'Content-type': 'application/json'}

foo = {'text': 'Hello HTTP #1 **cool**, and #1!'}
json_data = json.dumps(foo)


conn.request("PUT", "/put", json_data)
response = conn.getresponse()
print(response.status, response.reason)