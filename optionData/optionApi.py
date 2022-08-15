import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
           'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8'}
urlNIFTY = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
urlBANKNIFTY = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"

def myround(x, base=5):
    return base * round(x/base)



    
def getNiftyData():
    dataNIFTY = requests.get(urlNIFTY, headers=headers).json()

    NiftyMktPrice = dataNIFTY['records']['data'][0]['PE']['underlyingValue']
    underlyingValueNIFTY = myround(
    NiftyMktPrice)
    indexNIFTY = ""
    for idx, row in enumerate(dataNIFTY['filtered']['data']):
        if(row['strikePrice'] == underlyingValueNIFTY):
            indexNIFTY = idx
            break
    def calculate_niftydata(indexNIFTY,counter):
        
        changeinOpenInterestCESumNIFTY = 0
        changeinOpenInterestPESumNIFTY = 0

        for i in range(indexNIFTY-counter, indexNIFTY+counter+1):
            changeinOpenInterestCESumNIFTY = changeinOpenInterestCESumNIFTY + \
                dataNIFTY['filtered']['data'][i]['CE']['changeinOpenInterest']
            changeinOpenInterestPESumNIFTY = changeinOpenInterestPESumNIFTY + \
                dataNIFTY['filtered']['data'][i]['PE']['changeinOpenInterest']
        diffNIFTY = changeinOpenInterestPESumNIFTY - changeinOpenInterestCESumNIFTY
        return {'diff':diffNIFTY, 'strike_price': dataNIFTY['filtered']['data'][indexNIFTY]['strikePrice'] }


    
    key_parameter = calculate_niftydata(indexNIFTY,10)
    atm_strike = calculate_niftydata(indexNIFTY,2)
    upper_strike = calculate_niftydata(indexNIFTY+1,2)
    lower_strike = calculate_niftydata(indexNIFTY-1,2)
    return {'market_price': NiftyMktPrice, 'key_parameter': key_parameter['diff'], 'data':[lower_strike, atm_strike, upper_strike]}
    
  
    

def getBankNiftyData():
    dataBANKNIFTY = requests.get(urlBANKNIFTY, headers=headers).json()

    bankNiftyMktPrice = dataBANKNIFTY['records']['data'][0]['PE']['underlyingValue']

    underlyingValueBANKNIFTY = myround(
        bankNiftyMktPrice, base=100)



    indexBANKNIFTY = ""

    for idx, row in enumerate(dataBANKNIFTY['filtered']['data']):

        if(row['strikePrice'] == underlyingValueBANKNIFTY):
            indexBANKNIFTY = idx
            break

    def calculate_bank_nifty_data(indexBANKNIFTY, counter):

        changeinOpenInterestCESumBANKNIFTY = 0
        changeinOpenInterestPESumBANKNIFTY = 0

        for i in range(indexBANKNIFTY-counter, indexBANKNIFTY+counter+1):
            changeinOpenInterestCESumBANKNIFTY = changeinOpenInterestCESumBANKNIFTY + \
                dataBANKNIFTY['filtered']['data'][i]['CE']['changeinOpenInterest']
            changeinOpenInterestPESumBANKNIFTY = changeinOpenInterestPESumBANKNIFTY + \
                dataBANKNIFTY['filtered']['data'][i]['PE']['changeinOpenInterest']

        diffBANKNIFTY = changeinOpenInterestPESumBANKNIFTY - \
            changeinOpenInterestCESumBANKNIFTY
        return {'diff':diffBANKNIFTY, 'strike_price': dataBANKNIFTY['filtered']['data'][indexBANKNIFTY]['strikePrice'] }

        
    atm_strike = calculate_bank_nifty_data(indexBANKNIFTY, 2) #Atm price

    key_parameter = calculate_bank_nifty_data(indexBANKNIFTY, 10)
    lower_strike = calculate_bank_nifty_data(indexBANKNIFTY-1, 2) #OTm price
    upper_strike = calculate_bank_nifty_data(indexBANKNIFTY+1, 2) # Itm price
    return {'market_price': bankNiftyMktPrice, 'key_parameter': key_parameter['diff'], 'data':[lower_strike, atm_strike, upper_strike]}




getNiftyData()
getBankNiftyData()