import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st


tesla = 'https://query1.finance.yahoo.com/v7/finance/download/TSLA?period1=1645482599&period2=1677018599&interval=1d&events=history&includeAdjustedClose=true'
intel = 'https://query1.finance.yahoo.com/v7/finance/download/INTC?period1=322099200&period2=1676937600&interval=1d&events=history&includeAdjustedClose=true'
df_tesla = pd.read_csv(tesla)
df_intel = pd.read_csv(intel)
# df.head()
st.title("Vinny's Stock Dashboard 💸💰")
st.sidebar.title('Options')

df_tesla.Date = df_tesla.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df_intel.Date = df_intel.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))





categories = st.multiselect('Categories', ['Date', 'Open', 'Close', 'High', 'Low', 
'Volume'])
stocks = st.sidebar.multiselect('Stocks', ['Tesla', 'Intel'])

def hist_plot(categories, stocks):
    fig, ax = plt.subplots(figsize=(20,6))
    for categorie in categories:
        for stock in stocks:
            if stock == 'Tesla':
                df = df_tesla
            elif stock == 'Intel':
                df = df_intel
            ax.hist(categorie, data=df)
            # ax.set_title(f"{str(categorie)} - {stock}")
            ax.legend(stock)
            st.pyplot(fig)
hist = st.sidebar.button('Histogram')
if hist:
    hist_plot(categories, stocks)
