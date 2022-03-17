import numpy as np
import matplotlib.pyplot as plt

import json
import urllib.request, json
with urllib.request.urlopen("https://api.carbonintensity.org.uk/intensity/date") as url:
    data = json.loads(url.read().decode())
   # print(data)
    print(type(data))

raw_data = data['data']
print(type(raw_data))
timestamp=[]
actual=[]
forecast=[]
for row in raw_data:
    timestamp.append(np.datetime64(row['from']))
    intensity1 = row['intensity']
    actual.append(intensity1['actual'])
    #print(timestamp)

for row in raw_data:
    #timestamp.append(np.datetime64(row['from']))
    intensity2 = row['intensity']
    forecast.append(intensity2['forecast'])

xData = np.array(timestamp)
yData1 = np.array(actual)
yData2 = np.array(forecast)
plt.plot(xData, yData1, color='b', linestyle='-', marker='o', label='y1 data')
plt.plot(xData, yData2, color='r', linestyle='-', marker='o', label='y2 data')
plt.show()
plt.savefig('static/img/plot2.png')

# for python 2
# import urllib, json
# url = "https://api.carbonintensity.org.uk/regional/postcode/LE1"
# response = urllib.urlopen(url)
# data = json.loads(response.read())
# print data

message = json.dumps(data)
with open('myfile.json','w+') as f:
#     f.write(timestamp)
    f.write(message)
