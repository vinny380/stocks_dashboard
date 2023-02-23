import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import streamlit as st
import time
import seaborn as sns

sns.set()

t = time.time()
ml = int(t * 1000)
print('Current time in milliseconds:', ml)
tesla = f'https://query1.finance.yahoo.com/v7/finance/download/TSLA?period1=1645482599&period2={ml}&interval=1d&events=history&includeAdjustedClose=true'
intel = f'https://query1.finance.yahoo.com/v7/finance/download/INTC?period1=322099200&period2={ml}&interval=1d&events=history&includeAdjustedClose=true'
df_tesla = pd.read_csv(tesla)
df_intel = pd.read_csv(intel)
# df.head()
st.title("Vinny's Stock Dashboard 💸💰")
st.sidebar.title('Options')

df_tesla.Date = df_tesla.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df_intel.Date = df_intel.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
col1, col2 = st.columns(2)


def red_or_green_daily(dfs):
    for n in dfs:
        # if n == dfs[0]:
        #     company = 'Tesla'
        # elif n == dfs[1]:
        #     company = 'Intel'
        company = 'Tesla'
        if (float(n.Close.iloc[-1]) >= (float(n.Close.iloc[-2]))):
            string = f"{company} is up by ${round(float(n.Close.iloc[-1]) - (float(n.Close.iloc[-2])), 3)}",
            display = f'<p style="color:green;">{string}</p>'
        else:
            string = f'''{company} is down by ${round(float(n.Close.iloc[-2]) - (float(n.Close.iloc[-1])), 3)}
                    || -{100 - round(float(n.Close.iloc[-1])/float(n.Close.iloc[-2]), 3) * 100}%'''
            display = f'<p style="color:red;">{string}</p>'
        st.write(display, unsafe_allow_html=True)

red_or_green_daily([df_tesla, df_intel])

period_selectbox = st.sidebar.selectbox('Period', ['1 day', '1 week', '1 month', '3 months' ,'6 months', '1 year', '5 years', 'Max'])

def period(df, period_selectbox):
    last_day = df.Date.iloc[-1]
    most_recent = df.Date.iloc[0]
    
    if period_selectbox == '1 day':
        days = 1
    elif period_selectbox == '1 week':
        days = 7
    elif period_selectbox == '1 month':
        days = 30
    elif period_selectbox == '3 months':
        days = 90
    elif period_selectbox == '6 months':
        days = 180
    elif period_selectbox == '1 year':
        days = 365
    elif period_selectbox == '5 years':
        days = 365 * 5
    elif period_selectbox == 'Max':
        date = most_recent
        sliced_df = df
        return sliced_df
    
    date = last_day - timedelta(days=days)
    sliced_df = df[df.Date >= date]
    return sliced_df



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
            ax.hist(categorie,data=df, label=stock)
            ax.set(title=f"{str(categorie)} - {stock}", xlabel=categorie, ylabel="Frequency")
            fig.autofmt_xdate()
            ax.legend()
            plt.tight_layout()
            
    st.pyplot(fig)
hist = st.sidebar.button('Histogram')
if hist:
    hist_plot(categories, stocks)


def line_plot(categories, stocks):
    fig, ax = plt.subplots(figsize=(20,6))
    for categorie in categories:
        for stock in stocks:
            if stock == 'Tesla':
                df = period(df_tesla, period_selectbox)
            elif stock == 'Intel':
                df = period(df_intel, period_selectbox)
            ax.plot(df.Date,categorie,data=df, label=stock)
            ax.set(title=f"{str(categorie)} - {stock}", xlabel='Time', ylabel=categorie)
            fig.autofmt_xdate()
            ax.legend()
            plt.tight_layout()
            
    st.pyplot(fig)
line = st.sidebar.button('Line Plot')
if line:
    line_plot(categories, stocks)
