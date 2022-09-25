import string
import uvicorn
from fastapi import FastAPI
from yahoofinancials import YahooFinancials
app = FastAPI()

@app.get('/ticker/{ticker_name}')
async def root(ticker_name):
    yahoo_financials = YahooFinancials(ticker_name)
    return yahoo_financials.get_financial_stmts('annual', ['income', 'cash', 'balance'])
