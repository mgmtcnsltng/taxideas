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


# from google.colab import files
# uploaded = files.upload()

# # click on the folder icon on the left navigation bar, and make sure the 'Files' only contains one 'inputs.csv'
# # files with the same name will be appended with a number, so the incorrect file would be selected as input

# import io


"""
# Welcome to Streamlit!
Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).
In the meantime, below is an example of what you can do with just a few lines of code:
"""
