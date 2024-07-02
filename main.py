from app import Protfolio

def lambda_handler():
    portfolio = Protfolio()
    return portfolio.lambda_handler()