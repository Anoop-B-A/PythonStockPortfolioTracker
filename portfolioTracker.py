# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 22:16:13 2019

@author: banoop
"""

from yahoo_fin import stock_info as si
import pandas as pd
from tqdm import tqdm
from datetime import datetime, date 
#si.get_live_price("maruti.ns")
si.get_live_price("538970.bom")
inputDir="D:\PythonCode\PycharmProjects\pythonProject\portfolio\Data\Input"
inputFile="purchase_details.csv"
outputDir="D:\PythonCode\PycharmProjects\pythonProject\portfolio\Data\Output"
def get_stock_price(my_stocks):
    stocks_lst=[]
    price_lst=[]
    for stock in tqdm(my_stocks):
        stocks_lst.append(stock)
        price_lst.append(si.get_live_price(stock))
    stock_dict={'Ticker':stocks_lst, 'Price':price_lst}
    return pd.DataFrame(stock_dict,columns=['Ticker','Price'])

purchase_info=pd.read_csv("{0}\{1}".format(inputDir, inputFile), parse_dates=True)
#print(purchase_info)
purchase_info['Total_Buy_Price']=purchase_info['Price']*purchase_info['Qty']
purchase_info['Ticker']=purchase_info['Ticker'].str.lower()
my_stocks= purchase_info['Ticker'].unique() #{x:si.tickers_other() for x in purchase_info['Ticker']}
my_stocks
current_prices=get_stock_price(my_stocks)
portfolio=current_prices.merge(purchase_info, on='Ticker', how='inner')

portfolio['current_value']=portfolio['Price']*portfolio['Qty']
portfolio=portfolio.rename(columns={'Price':'Current_price'})
portfolio.reset_index(drop=True,inplace=True)
portfolio.index=portfolio['Ticker']


def createPortfolio(stockList,fileName):
    portfolio1=portfolio.loc[stockList,['Ticker','Qty','Total_Buy_Price','current_value']]
    portfolio1['Ticker']=portfolio1['Ticker'].str.upper()
    portfolio1['Ticker']=portfolio1['Ticker'].str.replace('.NS','')
    portfolio1=portfolio1.groupby(portfolio1['Ticker']).sum()
    portfolio1['Current_price']=portfolio.loc['Current_price'].avg()
    portfolio1['percent_chg']=((portfolio1['current_value']-portfolio1['Total_Buy_Price'])/portfolio1['Total_Buy_Price'])*100
    portfolio1['allocation']=(portfolio1['Total_Buy_Price']/portfolio1['Total_Buy_Price'].sum())*100
    portfolio1[['allocation','percent_chg','current_value']]=portfolio1[['allocation','percent_chg','current_value']].round(1)
    total=list(portfolio1[['Total_Buy_Price','current_value']].sum())
    total.insert(0,' ')
    total.insert(0,'Total')
    total.append(((total[3]-total[2])/total[2])*100)
    total.append(' ')
    total.remove('Total')
    total_Series=pd.Series(total,index=portfolio1.columns)
    total_Series.name='Total'
    portfolio1=portfolio1.append(total_Series)
    portfolio1.to_excel(fileName,freeze_panes=(1,1))


'''createPortfolio(['asianpaint.ns',	'bajfinance.ns',	'boschltd.ns',	'godrejcp.ns',	'havells.ns',	'hdfc.ns',	'irctc.ns',	'lt.ns',	'm&m.ns',	'maruti.ns',	'pidilitind.ns',	'reliance.ns',	'tcs.ns',	'titan.ns'
],outputDir+"portfolio_primary.xlsx")
 
createPortfolio(
['ashokley.ns','cgpower.ns','ioc.ns','recltd.ns','ujjivansfb.ns'],"D:\Stock investmentsportfolio_secondary.xlsx")

createPortfolio(
['arvindfasn.ns','sbin.ns','vedl.ns','yesbank.ns','axisbank.ns'],"D:\Stock investmentsportfolio_inactive.xlsx")
'''

"""
portfolio2=portfolio[['Total_Buy_Price']].groupby(portfolio['Date']).sum()
#portfolio2['Date']=portfolio2.index
#portfolio2.sort_index(axis=1, inplace=True)
portfolio2.reset_index(inplace=True)

#portfolio2['Date']=portfolio2['Date'].apply(lambda x : pd.to_datetime(str(x)))

portfolio2['Date']=pd.to_datetime(portfolio2['Date'])

type(portfolio2.iloc[0,0])

portfolio2['Month']=portfolio2['Date'].dt.month
portfolio2['Year']=portfolio2['Date'].dt.year
portfolio3=portfolio2.groupby(['Month','Year']).sum()
portfolio3.sort_index(inplace=True)
portfolio3.reset_index(inplace=True)
#portfolio3.to_csv("D:\Stock investmentsmonthly_purchase_details.csv")"""

