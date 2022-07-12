from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import pandas as pd
import datetime
import numpy as np
import time

from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

import math
import re

from tqdm import tqdm

def find_columns(df):
  for i in df.index:
    cols = []
    count = 0
    broken = False
    for j in range(len(df.iloc[i])):
      if(isinstance(df.iloc[i][j],str)):
        cols.append(df.iloc[i][j])
        count += 1
      if count == len(df.iloc[i]):
        broken = True
        break
    if broken:
      return i, cols

def dr_or_cr(row):
  if (row[-3] - row[-2] == row[-1]) & (row[-2] - row[-3] == row[-1]):
    return 'Unknown'
  elif row[-3] - row[-2] == row[-1]:
    return 'DR'
  elif row[-2] - row[-3] == row[-1]:
    return 'CR'
  else:
    return 'Unknown'

def replace_to_number(s):
    if type(s).__name__ == "str":
        s = s.strip()
        if s == "-":
            s = 0
        else:
            s = s.replace(",","").replace("$","")
            if s.find("(") >= 0 and s.find(")") >= 0:
                s = s.replace("(","-").replace(")","")
    return s

def output(df, account_names, file_name):

  writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
  char_to_replace = {'[': ' ', ']': ' ', ':' : ' ', '*' : ' ', '?' : ' ', '/' : ' ', '\\':' '}
  account_names[:] = [x for x in account_names if x]
  account_names = list(dict.fromkeys(account_names))

  for an in account_names:
    df_an = df.loc[df['Account'] == an]
    sheet_name = an[0:31]

    # Iterate over all key-value pairs in dictionary
    for key, value in char_to_replace.items():
      # Replace key character with value character in string
      sheet_name = sheet_name.replace(key, value)

    # print(sheet_name)
    df_an.to_excel(writer, sheet_name = sheet_name)

  writer.save()

st.title('Uber pickups in NYC')

st.file_uploader('Upload a CSV')


st.download_button('Download file', data)


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
