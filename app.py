# libraries used
import requests
import pandas as pd
import csv

class Protfolio:
    def __init__(self):
        pass

    def get_info(self):
        
        with open('holdings.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            print("Temp")

            print(csv_reader)

obj1 = Protfolio()
obj1.get_info()


