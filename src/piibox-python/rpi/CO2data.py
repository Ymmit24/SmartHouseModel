import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#log('json test start')

import urllib, json

class CO2data:

    url = "https://api.carbonintensity.org.uk/intensity/date"
    def getData(self):
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        raw_data = data['data']
        return data

#log('api call')

    def process_data(self, data):
        timestamp=[]
        actual=[]
        forecast=[]

        for row in raw_data:
            timestamp.append(np.datetime64(row['from']))
            intensity1 = row['intensity']
            actual.append(intensity1['actual'])

            intensity2 = row['intensity']
            forecast.append(intensity2['forecast'])

        return timestamp, actual, forecast

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

if __name__ == '__main__':
    this_instance = CO2data()
    d = this_instance.getData()
    t,a,f = this_instance.process_data(d)
    intensity_plot = this_instance.plot(t,a,f)

#log('end of co2data')