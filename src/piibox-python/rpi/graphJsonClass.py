import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#log('json test start')

import urllib, json

class graphJsonClass:

    url = "https://api.carbonintensity.org.uk/intensity/date"
    def getData(self):
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        raw_data = data['data']
        return data

# python3
# import json
# import urllib.request, json
# with urllib.request.urlopen("https://api.carbonintensity.org.uk/intensity/date") as url:
#     data = json.loads(url.read().decode())

#log('api call')

    def proces_data(self, data):
        timestamp=[]
        actual=[]
        forecast=[]

#log('forecast')

        for row in raw_data:
            timestamp.append(np.datetime64(row['from']))
            intensity1 = row['intensity']
            actual.append(intensity1['actual'])

            intensity2 = row['intensity']
            forecast.append(intensity2['forecast'])

        return timestamp, actual, forecast

#log('for loop in rawdata')
    def plot(self, timestamp, actual,forecast):
        fig, ax = plt.subplots(1,1)
        ax.plot(timestamp, actual, color='b', linestyle='-', marker='o', label='y1 data')
        ax.plot(timestamp, forecast, color='r', linestyle='-', marker='o', label='y2 data')

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))

        for label in ax.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')

        plt.grid(True)
        plt.show()
        fig.savefig('/usr/local/projects/piiboxweb/src/piibox-python/rpi/static/day1.png')

#log('saved figure')

#JSON test
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
#
# import json
# import urllib.request, json
# with urllib.request.urlopen("https://api.carbonintensity.org.uk/intensity/2022-03-17T12:00Z/pt24h") as url:
#     data = json.loads(url.read().decode())
#    # print(data)
#     print(type(data))
#
# raw_data = data['data']
# print(type(raw_data))
# timestamp=[]
# actual=[]
# forecast=[]
#
# for row in raw_data:
#     timestamp.append(np.datetime64(row['from']))
#     intensity1 = row['intensity']
#     actual.append(intensity1['actual'])
#
#     intensity2 = row['intensity']
#     forecast.append(intensity2['forecast'])
#
# print(np.sort(forecast))
# # xData = np.array(timestamp)
# # yData1 = np.array(actual)
# # yData2 = np.array(forecast)
#
#
# fig, ax = plt.subplots(1,1)
# ax.plot(timestamp, actual, color='b', linestyle='-', marker='o', label='y1 data')
# ax.plot(timestamp, forecast, color='r', linestyle='-', marker='o', label='y2 data')
#
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))
#
# for label in ax.get_xticklabels(which='major'):
#     label.set(rotation=30, horizontalalignment='right')
#
# plt.grid(True)
# plt.show()
# plt.savefig('static/img/plot2.png')
#
# # for python 2
# # import urllib, json
# # url = "https://api.carbonintensity.org.uk/regional/postcode/LE1"
# # response = urllib.urlopen(url)
# # data = json.loads(response.read())
# # print data
#
# message = json.dumps(data)
# with open('myfile.json','w+') as f:
# #     f.write(timestamp)
#     f.write(message)

if __name__ == '__main__':
    this_instance = graphJsonClass()
    d = this_instance.getData()
    t,a,f = this_instance.proces_data(d)
    this_instance.plot(t,a,f)