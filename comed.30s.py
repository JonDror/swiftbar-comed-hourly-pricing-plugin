#!/usr/bin/env python3
#encoding: utf-8

# <bitbar.title>comEd Current hourly price</xbar.title>
# <bitbar.version>v1.0</xbar.version>
# <bitbar.author>Jonathan Dror</xbar.author>
# <bitbar.author.github>JonDror</xbar.author.github>
# <bitbar.desc>See the current price of comEd hourly pricing.</xbar.desc>
# <bitbar.dependencies>python, requests module</xbar.dependencies>

import requests
import datetime as dt
import pytz
import json

comedCurrentApi = "https://hourlypricing.comed.com/api?type=5minutefeed"
tz = "America/Chicago"

def utc_ms_to_timezone(utc_ms_ts):
    # convert from time stamp to datetime
    utc_datetime = dt.datetime.utcfromtimestamp(int(utc_ms_ts) / 1000.)

    # set the timezone to UTC, and then convert to desired timezone
    return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone(tz)).strftime('%H:%M%p')

# Get data
url = requests.get(comedCurrentApi)
text = url.text
data = json.loads(text)

# Get current price
currentPrice = data[0]
priceUSD = currentPrice['price']

# Get current time
priceTimeUTC = currentPrice['millisUTC']

## Decide on the color. default: orange
alertColor = "orange"
if float(priceUSD) < 5:
	alertColor = "green"
elif float(priceUSD) > 10:
	alertColor = "red"

## Print menu bar
print(str(priceUSD)+"¢ :gauge: | sfcolor="+alertColor)

## Print dropdown
print ("---")
print ("updated at "+utc_ms_to_timezone(priceTimeUTC))
print ("---")
print ("History:")
for x in range(1,6):
  print(utc_ms_to_timezone(data[x]['millisUTC'])+": "+data[x]['price']+"¢")
print ("---")
print("Click here to see original JSON | href="+comedCurrentApi)