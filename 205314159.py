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

# Judul awal aplikasi
st.markdown('''
# Aplikasi Harga Saham
Ditujukan untuk memvisualisasikan saham **bank** di Indonesia. Namun anda juga bisa memasukkan Custom Ticker (cek **catatan**).
Bank yang tersedia ada 5 yaitu: BCA, BNI, BRI, Mandiri, dan Cimb Niaga

**Credits**
- App built by [Data Professor](https://www.youtube.com/channel/UCV8e2g4IWQqK71bbzGDEI4Q) and customized by Paulus Caesario Dito Putra Hartono
- [Tutorial](https://www.youtube.com/watch?v=0pHJOzNDdOo) from Data Professor
- [How to Get Stock Data Using Python](https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75)
- [freeCodeCamp.org](https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ) - [Build 12 Data Science Apps with Python and Streamlit - Full Course](https://youtu.be/JwSS70SZdyM?t=569)
- Dibuat dengan `Python` dengan library dari `streamlit`, `yfinance`, `datetime`, `googletrans`, dan `cufflinks`

**Catatan**
- Terkadang program membutuhkan waktu beberapa menit untuk menampilkan informasi keseluruhannya
- Interval dari data adalah **harian**
- Jika data terlalu sedikit untuk ditammpilkan di grafik terkadang grafik menjadi sangat kecil, coba double click pada bagian 'BOOL' di legend untuk memperbaiki 
- Untuk custom ticker, harus menggunakan list ticker yang tersedia di [finance.yahoo.com](https://finance.yahoo.com/trending-tickers)
''')
st.write('---') # border

# Sidebar streamlit
st.sidebar.subheader('Input Tanggal')   # Subheader
# Penyimpanan data di variabel sidebar
start_date = st.sidebar.date_input("Start date", datetime.date(2020, 1, 1)) #variabel untuk batas awal historical data
end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 1))    #variabel untuk batas akhir historical data

# Sidebar streamlit
st.sidebar.subheader('Input Ticker')    # Subheader

# Penyimpanan data di variabel sidebar
checkboxButton = st.sidebar.checkbox('Custom Ticker?')                      # Checkbox untuk custom ticker
# Menu untuk custom input atau tidak
if checkboxButton:
    tickerSymbol = st.sidebar.text_input('Enter Ticker Symbol')             # Widget untuk input custom
else:
    ticker_list = ['BBCA.JK', 'BBNI.JK', 'BBRI.JK', 'BMRI.JK', 'BNGA.JK']   # Ticker List yang disediakan
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)        # Widget untuk memilih ticker symbol dari array ticker_list

if tickerSymbol:    # cek variabel tickerSymbol mempunyai isi atau tidak
    # Assign yfinance dengan ticker yang sudah diinput
    tickerData = yf.Ticker(tickerSymbol)                                        # mendapatkan data dari ticker yang disediakan
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)  # mendapatkan data historical price dari ticker yang dipilih

    ### Perolehan informasi dari data dalam Ticker 
    #   (data diambil dari variabel 'tickerData' kemudian di-assign ke variabel selanjutnya)
    ###
    string_logo = '<img src=%s>' % tickerData.info['logo_url']      # Data logo, diambil dari '<ticker>.info' kemudian mengambil urlnya dan disimpan di variabel
    st.markdown(string_logo, unsafe_allow_html=True)                            # Menampilkan gambar

    string_name = tickerData.info['longName']                           # Pengambilan nama perusahaan dari '<ticker>.info' menggunakan keyword 'longName'
    st.header('**%s**' % string_name)                                           # Menampilkan nama perusahaan dengan format bold dan header

    string_summary = tickerData.info['longBusinessSummary']                     # Pengambilan data untuk bio singkat tentang perusahaan dan disimpan di variabel
    # translate info tentang perusahaan (en) ke dalam bahasa Indonesia
    translation = translator.translate(string_summary, dest='id')               # Penggunaan fungsi dari lib googletrans untuk translate
    string_info = translation.text + '\n\n*-translated by googletrans*'         # Penambahan keterangan dari data yang sudah ditranslate
    st.info(string_info)                                                        # Menampilkan data bio

    # Ticker historical data
    st.header('**Ticker Historical Data**')                                     # Menampilkan header
    st.write(tickerDf)                                                          # Menampilkan tabel

    # Bollinger bands atau grafik
    st.header('**Grafik Saham**')                                               # Menampilkan header
    qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')  # Isi grafik
    qf.add_bollinger_bands()                                                    # Menambahkan grafik
    fig = qf.iplot(asFigure=True)                                               # Memplot grafik
    st.plotly_chart(fig)                                                        # Menampilkan grafik di web
else:
    # Menampilkan header jika variabel tickerSymbol kosong
    st.markdown("<h2 style='text-align: center; color: white;'>input ticker symbol first</h2>", unsafe_allow_html=True)   

st.write('---') # border