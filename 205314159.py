"""
Created on Wed Jun 16 13:41:33 2021
Python 3.9.2
@author: Dito
Aplikasi Harga Saham berbasis web
"""
# import seluruh library yang akan digunakan
import yfinance as yf
import streamlit as st
import cufflinks as cf
import datetime
from googletrans import Translator

# init the Google API translator - dari tutorial googletrans
translator = Translator()

# SETUP WIDE STREAMLIT 
st.set_page_config(page_title='Stock Price App v2', layout="wide", page_icon='🤑')

# Judul awal aplikasi
st.markdown('''
# Stock Price App

**The Extended Version of [Aplikasi Harga Saham](https://github.com/synraax/hargaSahamApp)**

**Credits**
- App built by [Data Professor](https://www.youtube.com/channel/UCV8e2g4IWQqK71bbzGDEI4Q) and customized by Paulus Caesario Dito Putra Hartono
- [Tutorial](https://www.youtube.com/watch?v=0pHJOzNDdOo) from Data Professor
- [How to Get Stock Data Using Python](https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75)
- [freeCodeCamp.org](https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ) - [Build 12 Data Science Apps with Python and Streamlit - Full Course](https://youtu.be/JwSS70SZdyM?t=569)
- Dibuat dengan `Python` dengan library dari `streamlit`, `yfinance`, `datetime`, `googletrans`, dan `cufflinks`

**Notes**
- Input the Ticker Symbol from this site: [finance.yahoo.com](https://finance.yahoo.com/trending-tickers)
''')


st.write('---') # border

# Sidebar streamlit
st.sidebar.subheader('Input Tanggal')   

#Input date
start_date = st.sidebar.date_input("Start date", datetime.date(2020, 1, 1)) #
end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 1))    

st.sidebar.subheader('Input Ticker')   

# Sidebar input
tickerSymbol1 = st.sidebar.text_input('Enter Ticker Symbol #1', 'KO')

tickerSymbol2 = st.sidebar.text_input('Enter Ticker Symbol #2', 'TSLA')

if tickerSymbol1 and tickerSymbol2:    

    col1, col2 = st.beta_columns(2)

    # COL1
    tickerData1 = yf.Ticker(tickerSymbol1)                                        
    tickerDf1 = tickerData1.history(period='1d', start=start_date, end=end_date) 
    # COL2
    tickerData2 = yf.Ticker(tickerSymbol2)                                        
    tickerDf2 = tickerData2.history(period='1d', start=start_date, end=end_date)

    ### Divide DATA SUMMARY ###
    ### SHOW DATA ###
    # COL1
    string_logo = '<img src=%s>' % tickerData1.info['logo_url']      
    col1.markdown(string_logo, unsafe_allow_html=True)                           

    string_name = tickerData1.info['longName']                          
    col1.header('**%s**' % string_name)                                          

    string_summary = tickerData1.info['longBusinessSummary']                  
    translation = translator.translate(string_summary, dest='id')               
    string_info = translation.text + '\n\n*-translated by googletrans*'       
    col1.info(string_info)  

    # COL2
    ### SHOW DATA ###
    string_logo = '<img src=%s>' % tickerData2.info['logo_url']      
    col2.markdown(string_logo, unsafe_allow_html=True)                           

    string_name = tickerData2.info['longName']                          
    col2.header('**%s**' % string_name)                                          

    string_summary = tickerData2.info['longBusinessSummary']                  
    translation = translator.translate(string_summary, dest='id')               
    string_info = translation.text + '\n\n*-translated by googletrans*'       
    col2.info(string_info)

    ### END DATA SUMMARY ###

    ### Divide DATA TABEL ###
    col3, col4 = st.beta_columns(2)

    # COL3
    # Ticker historical data
    col3.header('**Ticker Historical Data**')                                   
    col3.write(tickerDf1)

    # COL4
    # Ticker historical data
    col4.header('**Ticker Historical Data**')                                   
    col4.write(tickerDf2)

    ### END DATA TABEL ###

    ### Divide DATA GRAFIK ###
    col5, col6 = st.beta_columns(2)

    # COL5
    # Bollinger bands atau grafik
    col5.header('**Grafik Saham**')                                              
    qf=cf.QuantFig(tickerDf1,title='First Quant Figure',legend='top',name='GS')  
    qf.add_bollinger_bands()                                                   
    fig = qf.iplot(asFigure=True)                                             
    col5.plotly_chart(fig)                                                    

    # COL6                                                   
    # Bollinger bands atau grafik
    col6.header('**Grafik Saham**')                                              
    qf=cf.QuantFig(tickerDf2,title='First Quant Figure',legend='top',name='GS')  
    qf.add_bollinger_bands()                                                   
    fig = qf.iplot(asFigure=True)                                             
    col6.plotly_chart(fig)
                                                
else:
   
    st.markdown("<h2 style='text-align: center; color: white;'>input ticker symbol first</h2>", unsafe_allow_html=True)   

st.write('---') 
