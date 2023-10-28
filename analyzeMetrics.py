import csv
##TESNSOR FLOW
count_overbought_sell = 0
count_oversold_buy = 0
count_bullish_divergence_buy = 0
count_bearish_divergence_sell = 0
count_bullish_rsi_cross_buy = 0
count_bearish_rsi_cross_sell = 0
count_bullish_signal_buy = 0
count_bearish_signal_sell = 0

def testTrends(previousPrice, price, previousRSI, rsi, previousSMA, sma, previousVWAP, vwap, resistance_level, support_level, sma_50, sma_200):
    global count_overbought_sell
    global count_oversold_buy
    global count_bullish_divergence_buy
    global count_bearish_divergence_sell
    global count_bullish_rsi_cross_buy
    global count_bearish_rsi_cross_sell
    global count_bullish_signal_buy
    global count_bearish_signal_sell

    if rsi > 70 and price <= resistance_level:
        # Overbought condition, potential sell signal
        count_overbought_sell += 1

    if rsi < 30 and price >= support_level:
        # Oversold condition, potential buy signal
        count_oversold_buy += 1

    if rsi > previousRSI and price < previousPrice:
        # Bullish divergence pattern detected, potential buy signal
        count_bullish_divergence_buy += 1

    if rsi < previousRSI and price > previousPrice:
        # Bearish divergence pattern detected, potential sell signal
        count_bearish_divergence_sell += 1

    if previousRSI < 30 and rsi > 30:
        # Bullish RSI cross detected, potential buy signal
        count_bullish_rsi_cross_buy += 1

    if previousRSI > 70 and rsi < 70:
        # Bearish RSI cross detected, potential sell signal
        count_bearish_rsi_cross_sell += 1

    if rsi > 50 and sma_50 > sma_200:
        # Bullish signal, potential buy signal
        count_bullish_signal_buy += 1

    if rsi < 50 and sma_50 < sma_200:
        # Bearish signal, potential sell signal
        count_bearish_signal_sell += 1

# Open and read the CSV file
with open('stock_prices.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the first 14 lines
    for _ in range(14):
        next(csv_reader)
    
    count = 0
    previousPrice = 0
    previousRSI = 0
    previousVWAP = 0
    previousSMA = 0
    higher = 0
    lower = 0
    count = 0

    # Read each line into a singular variable and process the data
    for row in csv_reader:
        # Extract data from the current row
        date, time, price, sma, vwap, rsi = row
        price = float(price)
        
        # Check if sma, vwap, and rsi are empty and handle them accordingly
        sma = float(sma) if sma else None
        vwap = float(vwap) if vwap else None
        rsi = float(rsi) if rsi else None
        
        testTrends(previousPrice, price, previousRSI, rsi, previousSMA, sma, previousVWAP, vwap )


        # Update previousPrice and previousRSI (assuming these values need to be updated for the next iteration)
        previousPrice = price
        previousRSI = rsi
        previousSMA = sma
        previousVWAP = vwap
        count+=1

print("Number of times RSI was high and price was high:", count_rsi_high_price_high)
print("Number of times RSI was low and price was high:", count_rsi_low_price_high)
print("Number of times RSI was high and price was low:", count_rsi_high_price_low)
print("Number of times RSI was low and price was low:", count_rsi_low_price_low)
print("Count:", count)

