import traceback
import requests
import csv
from collections import deque

API_KEY = 'V8KED7B2E3CU7R2V'
SYMBOL = 'TQQQ'
START_DATE = '2023-09-29'
END_DATE = '2023-10-20'

rsiGain = deque(maxlen=14)
rsiLoss = deque(maxlen=14)
gain = False
previousPrice = 0
periodCount = 0

def getRSI(price):
    global periodCount, previousPrice

    priceChange = price - previousPrice
    previousPrice = price

    if priceChange >= 0:
        rsiGain.append(priceChange)
        rsiLoss.append(0)
    else:
        rsiGain.append(0)
        rsiLoss.append(-priceChange)

    periodCount += 1

    if periodCount >= 14:
        averageGain = sum(rsiGain) / 14
        averageLoss = sum(rsiLoss) / 14
        
        if averageLoss == 0:
            return 100.00 
        else:
            rs = averageGain / averageLoss
            rsi = 100 - (100 / (1 + rs))
            return round(rsi, 2)
    else:
        return None


prices = deque(maxlen=14)

def getSMA(price):
    prices.append(price)

    if len(prices) < 14:
        return None

    sma = sum(prices) / 14 
    return round(sma, 2)


try:
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=1min&apikey={API_KEY}&datatype=json&outputsize=full')

    data = response.json()

    minute_prices = data['Time Series (1min)']

    sorted_prices = sorted(minute_prices.items())

    with open('stock_prices.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['date', 'time', 'price', 'sma', 'vwap', 'rsi'])

        total_volume = 0
        vwap_sum = 0

        for timestamp, price_data in sorted_prices:
            date, time = timestamp.split(' ')
            if START_DATE <= date <= END_DATE:
                price = float(price_data['1. open'])
                volume = int(price_data['5. volume'])

                vwap_sum += price * volume
                total_volume += volume
                if total_volume != 0:
                    vwap = round(vwap_sum / total_volume,2)
                else:
                    vwap = round(0,2)

                rsi = getRSI(price)

                sma = getSMA(price)

                csvwriter.writerow([date, time, price, sma, vwap, rsi])
                #print(f'{date} {time}: {price}')

    print("Done")

except Exception as e:
    print(f'Error: {e}')
    print(f'Traceback: {traceback.format_exc()}')