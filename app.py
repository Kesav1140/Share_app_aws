# libraries used
import requests
import csv

class Protfolio:
    def __init__(self):
        self.head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36 "}
        self.get_details = 'https://www.nseindia.com/api/quote-equity?symbol={}'
        

    def lambda_handler(self):

        current_data = []
        
        # read the current protfolio from csv file
        with open('holdings.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            
            for i in csv_reader:
                share_dict = {}
                if i[0] == 'Instrument':
                    pass
                else:
                    share_dict['stock_name'] = i[0]
                    share_dict['quantity'] = int(i[1])
                    share_dict['price'] = float(i[2])
                    share_dict['invested_value'] = int(i[1]) * float(i[2])
                
                    current_data.append(share_dict)
        session = requests.session()
        session.get('https://www.nseindia.com/', headers=self.head)

        total_data = []
        for stock in current_data:
            # print(stock)
            stock_name = stock['stock_name']
            
            try:
                url = str(self.get_details.format(stock_name))
                company_details = session.get(url=url, headers=self.head)
                live_data = company_details.json()

                stock['eod_price'] = float(live_data['priceInfo']['lastPrice'])
                stock['52_week_high'] = float(live_data['priceInfo']['weekHighLow']['max'])
                stock['52_week_low'] = float(live_data['priceInfo']['weekHighLow']['min'])
                stock['current_value'] = stock['quantity'] * stock['eod_price']
                stock['profit/loss'] = (stock['current_value'] - stock['invested_value'])/100
                    
                total_data.append(stock)

            except Exception as err:
                print(err)
                print()

        print(total_data)
    

# if __name__ == __main__:
    # obj1 = Protfolio()
    # obj1.lambda_handler()
    #test


