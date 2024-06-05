# libraries used
import requests
import csv
import datetime 
import boto3
import os
from botocore.exceptions import ClientError
import json

class Protfolio:
    def __init__(self):
        self.head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36 "}
        self.get_details = 'https://www.nseindia.com/api/quote-equity?symbol={}'


    def save_to_s3(self, data):
        # Role arn for temp credentials
        role_arn = 'arn:aws:iam::767397923004:role/kesavan_aws_role1'

        # Create an STS client
        sts_client = boto3.client('sts', aws_access_key_id="AKIA3FLD3BC6HEUWGWME", aws_secret_access_key="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")

        # Assumerole to get temperory creds
        assumerole_response = sts_client.assume_role(
            RoleArn = role_arn,
            RoleSessionName = 'S3_call'
        )

        aws_temp_creds = assumerole_response['Credentials']

        # Creating S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id= aws_temp_creds['AccessKeyId'],
            aws_secret_access_key=aws_temp_creds['SecretAccessKey'],
            aws_session_token = aws_temp_creds['SessionToken']
            )
        
        # Get the current date
        current_date = datetime.date.today()

        # Create the filename with the current date
        filename = f"portfolio_data_{current_date.strftime('%d-%m-%Y')}"

        # Specify the S3 bucket name and the complete path
        s3_bucket_name = "k7-lambda-bucket1"
        s3_file_path = f"share_data/{filename}"

        # Convert the list of dictionaries to a CSV string
        csv_data = []
        for item in data:
            csv_data.append([item['stock_name'], item['quantity'], item['price'], item['invested_value'], item['eod_price'], item['52_week_high'], item['52_week_low'], item['current_value'], item['profit_loss']])
        
        # Add headers
        headers = ['stock_name', 'quantity', 'price', 'invested_value', 'eod_price', '52_week_high', '52_week_low', 'current_value', 'profit_loss']

        with open('temp.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)  # Write headers
            writer.writerows(csv_data)  # Write data

        # Write the CSV string to the S3 bucket
        s3.put_object(Body=open('temp.csv', 'rb'), Bucket=s3_bucket_name, Key=s3_file_path + '.csv')

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
                stock['profit_loss'] = ((stock['current_value'] - stock['invested_value'])/stock['invested_value'])*100
                    
                total_data.append(stock)

            except Exception as err:
                print(err)
        
        # function to save the data as csv file
        self.save_to_s3(total_data)

'''
if __name__ == "__main__":
    obj1 = Protfolio()
    obj1.lambda_handler()
'''

