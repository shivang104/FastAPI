import string
import uvicorn
from fastapi import FastAPI
from yahoofinancials import YahooFinancials
import pandas as pd
import json

app = FastAPI()

@app.get('/ticker/{ticker_name}')
async def root(ticker_name):
    yahoo_financials = YahooFinancials(ticker_name)
    stmnts = yahoo_financials.get_financial_stmts('annual', ['income', 'cash', 'balance'])
    income_statement = stmnts['incomeStatementHistory'][ticker_name]
    cash_statement = stmnts['cashflowStatementHistory'][ticker_name]
    balance_statement = stmnts['balanceSheetHistory'][ticker_name]
    df_list_is = []
    df_list_cs = []
    df_list_bs = []
    for d in income_statement:
        df_list_is.append(pd.DataFrame.from_dict(d, orient='index'))
    for d in cash_statement:
        df_list_cs.append(pd.DataFrame.from_dict(d, orient='index'))
    for d in balance_statement:
        df_list_bs.append(pd.DataFrame.from_dict(d, orient='index'))
    df_is = pd.concat(df_list_is)
    df_cs = pd.concat(df_list_cs)
    df_bs = pd.concat(df_list_bs)
    is_json = df_is.to_json()
    cs_json = df_cs.to_json()
    bs_json = df_bs.to_json()
    list_json = {}
    list_json['is'] = is_json
    list_json['cs'] = cs_json
    list_json['bs'] = bs_json
#     json_obj = json.dumps(list_json)
    return list_json
