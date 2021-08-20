#!/usr/bin/env python3
#encoding: utf-8

# <xbar.title>comEd Current hourly price</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Jonathan Dror</xbar.author>
# <xbar.author.github>jondror</xbar.author.github>
# <xbar.desc>See the current price of comEd hourly pricing.</xbar.desc>
# <xbar.dependencies>python, requests module</xbar.dependencies>

import requests
import datetime as dt
import pytz
import json

comedCurrentApi = "https://hourlypricing.comed.com/api?type=5minutefeed"
tz = "America/Chicago"

def tz_from_utc_ms_ts(utc_ms_ts, tz_info):
    """Given millisecond utc timestamp and a timezone return dateime

    :param utc_ms_ts: Unix UTC timestamp in milliseconds
    :param tz_info: timezone info
    :return: timezone aware datetime
    """
    # convert from time stamp to datetime
    utc_datetime = dt.datetime.utcfromtimestamp(utc_ms_ts / 1000.)

    # set the timezone to UTC, and then convert to desired timezone
    return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz_info)

url = requests.get(comedCurrentApi)
text = url.text

data = json.loads(text)

currentPrice = data[0]
priceUSD = currentPrice['price']


## Decide on the color. default: orange
alertColor = "orange"
if float(priceUSD) < 5:
	alertColor = "green"
elif float(priceUSD) > 10:
	alertColor = "red"

priceTimeUTC = currentPrice['millisUTC']
priceTimeInLocalTZ = tz_from_utc_ms_ts(int(priceTimeUTC), pytz.timezone(tz))
# print(str(priceUSD)+"¢ :electric_plug: | symbolize=false color="+alertColor)
print(str(priceUSD)+"¢ :gauge: | sfcolor="+alertColor)
print ("---")
print ("as of "+priceTimeInLocalTZ.strftime('%H:%M%p'))
print ("---")
print("Original JSON: | href="+comedCurrentApi)
print(data[0])