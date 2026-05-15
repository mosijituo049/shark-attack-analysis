import pandas as pd
import numpy as np
import re
import pycountry

def clean_col_names(df):
    df2 = df.copy()
    df2.columns = df2.columns.map(lambda x: x.lower().replace(' ','_'))
    return df2

def clean_df(df):
    df2=df.copy()
    df2 = df2.map(lambda x:x.lower().strip() if isinstance(x,str) else x)
    df2 = df2.dropna(how='all')
    df2 = df2.drop_duplicates()
    df2.drop(columns=["pdf"], inplace = True)
    df2.drop(columns=["href_formula"], inplace = True)
    df2.drop(columns=["href"], inplace = True)
    df2.drop(columns=["case_number"], inplace = True)
    df2.drop(columns=["case_number.1"], inplace = True)
    df2.drop(columns=["original_order"], inplace = True)
    df2.drop(columns=["unnamed:_21"], inplace = True)
    df2.drop(columns=["unnamed:_22"], inplace = True)
    return df2

def clean_col_date(df):
      df2=df.copy()
    
      #clean date string
      df2["Date"] = (
        df2["Date"]
        .astype("string")
        .str.title()
        .str.strip()
        # remove space around "-""
        .str.replace(
            r'\s*-\s*',
            '-',
            regex=True
        )
        # keep only one "-"
        .str.replace(
        r'-+',
        '-',
        regex=True
        )
        # remove upfront words befor date
        .str.replace(
            r'^(Reported|Updated|Dated|Letter dated)\s+',
            '',
            regex=True
        )
        # replace separator
        .str.replace(
            r'(?<=[A-Za-z])-(?=\d)',
            ' ',
            regex=True
        )
        .str.replace(
            r'(?<=\d)-(?=[A-Za-z])',
            ' ',
            regex=True
        )
         # combine spaces
        .str.replace(
            r'\s+',
            ' ',
            regex=True
        )
      )
      #conver month
      month_map = {
          "January": "Jan",
          "February": "Feb",
          "March": "Mar",
          "April": "Apr",
          "June": "Jun",
          "July": "Jul",
          "August": "Aug",
          "September": "Sep",
          "Sept": "Sep",
          "October":"Oct",
          "November":"Nov",
          "December":"Dec"
      }
      for full, short in month_map.items():
          df2["Date"] = (
              df2["Date"]
              .str.replace(
                  full,
                  short,
                  regex=False
              )
          )
      # clean Year columne
      df2["Year"] = (
          df2["Year"]
          .astype("Int64")
          .astype("string")
      )
      # date type classification
      conditions = [
          # datetime_string ^\d{4}\s+\d{2}\s+\d{2}\s+\d{2}:\d{2}:\d{2}$
          df2["Date"].str.match(
              r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$',
              na=False
          ),
          # english_full_date
          df2["Date"].str.match(
              r'^\d{1,2}\s+[A-Za-z]{3}\s+\d{4}$',
              na=False
          ),
          # english_day_month
          df2["Date"].str.match(
              r'^\d{1,2}(st|nd|rd|th)?\s+[A-Za-z]+$',
              case=False,
              na=False
          ),
    
          # seasonal_date
          df2["Date"].str.match(
              r'^(Spring|Summer|Fall|Autumn|Winter)\s+\d{4}$',
              case=False,
              na=False
          ),
          # approximate_date
          df2["Date"].str.match(
              r'^(Late|Early|Mid)\s+[A-Za-z]{3}-\d{4}$',
              case=False,
              na=False
          ),
          # approximate_year
          df2["Date"].str.match(
              r'^(Early|Mid|Late)\s+\d{4}$',
              case=False,
              na=False
          ),
          # circa_date
          df2["Date"].str.match(
              r'^(Circa|Approx\.?|Around)\s+\d{4}$',
              case=False,
              na=False
          ),
          # before_after
          df2["Date"].str.match(
              r'^(Before|After)\s+\d{4}$',
              case=False,
              na=False
          ),
    
          # month_year
          df2["Date"].str.match(
              r'^[A-Za-z]+\s+\d{4}$',
              na=False
          ),
          # year_only
          df2["Date"].str.match(
              r'^\d{4}$',
              na=False
          )
    
      ]
    
      choices = [
          "datetime_string",
          "english_full_date",
          "english_day_month",
    
          "seasonal_date",
          "approximate_date",
          "approximate_year",
          "circa_date",
          "before_after",
    
          "month_year",
          "year_only",
      ]
    
      df2["date_type"] = np.select(
          conditions,
          choices,
          default="invalid"
      )
    
      # deal with datetime_string
      df2.loc[df2["date_type"] == "datetime_string","clean_date"] = pd.to_datetime(
          df2.loc[df2["date_type"]== "datetime_string", "Date"],
          format="%Y-%m-%d %H:%M:%S",
          errors="coerce"
      )
      # deal with english_full_date
      df2.loc[df2["date_type"]== "english_full_date","clean_date"]=pd.to_datetime(
          df2.loc[df2["date_type"]== "english_full_date", "Date"],
          format="%d %b %Y",
          errors="coerce"
      )
      # deal with month_year, set day as 1
      temp = ("1 "+ df2.loc[df2["date_type"] == "month_year","Date"])
      df2.loc[df2["date_type"] == "month_year","clean_date"] = pd.to_datetime(
          temp,
          format="%d %b %Y",
          errors="coerce"
      )
      # deal with english_day_month
      temp = (
          df2.loc[df2["date_type"] == "english_day_month","Date"]
          .str.replace(
              r'(\d+)(st|nd|rd|th)',
              r'\1',
              regex=True
          )
      )
      temp = (
          temp
          + " "
          + df2.loc[df2["date_type"] == "english_day_month","Year"]
      )
    
      df2.loc[df2["date_type"] == "english_day_month","clean_date"] = pd.to_datetime(
          temp,
          format="%d %b %Y",
          errors="coerce"
      )
      # deal with year_only
      # set day month as 01-01
      temp = (df2.loc[df2["date_type"] == "year_only","Date"]+ "-01-01")
      df2.loc[df2["date_type"] == "year_only","clean_date"] = pd.to_datetime(
          temp,
          format="%Y-%m-%d",
          errors="coerce"
      )
    
      df2["Date"]=df2["clean_date"]
      df2=df2.drop(columns=["clean_date"])
      df2=df2.drop(columns=["date_type"])

      # df2=df2[df2["Date"].notna()]
      
      return df2

def clean_col_3_type(df):
    df2 = df.copy()
    df2.type = df2.type.map(lambda x:'other' if x not in ['unprovoked','provoked','watercraft'] else x)
    return df2

def clean_col_4_country(df):
    df2 = df.copy()
    countries_list = [country.name.lower() for country in pycountry.countries]
    df2.country = df2.country.replace({'usa':'united states',
                                       'okinawa':'japan','reunion':'réunion','reunion island':'réunion',
                                       'us virgin islands':'virgin islands, u.s.','?':'',
                                       "england": "united kingdom", "scotland": "united kingdom","usa": "united states","us":
                                       "united states","u.s.a": "united states","u.s.": "united states","columbia": "colombia",
                                       "bahrein": "bahrain","ceylon": "sri lanka","ceylon (sri lanka)": "sri lanka",
                                       "burma": "myanmar","cape verde": "cabo verde","san domingo": "dominican republic",
                                       "trinidad": "trinidad and tobago","tobago": "trinidad and tobago",
                                       "trinidad & tobago": "trinidad and tobago", "curacao": "curaçao","korea": "south korea"})
    missing = [i for i in list(df2.country) if i not in countries_list]
    df2['country'] = df2['country'].apply(lambda x: x.upper() if x in countries_list else 'other')
    return df2

def clean_col_activity(df):

    df2 = df.copy()
    # no_board_pattern = r'\b(?:swim(?:ming)?|bathing|snorkel(?:ing)?)\b'
    # fishing_pattern = r'\b\w*fishing\b'
    # board_pattern = r'\b(?:board|surf)\b'
    # diving_pattern = r'\b(?:dive|diving|scuba)\b'
    # df2.loc[df2.activity.str.contains(r'sunbathing', case=False, na=False),'activity'] = 'other'
    # df2.loc[df2.activity.str.contains(board_pattern, case=False, na=False),'activity'] = 'boarding'
    # df2.loc[df2.activity.str.contains(no_board_pattern, case=False, na=False),'activity'] = 'swimming'
    # df2.loc[df2.activity.str.contains(fishing_pattern, case=False, na=False),'activity'] = 'fishing'
    # df2.loc[df2.activity.str.contains(diving_pattern, case=False, na=False),'activity'] = 'diving'

    no_board_pattern = r'\b(swim(ming)?|bathing|snorkel(ing)?)\b'
    fishing_pattern = r'\b\w*fishing\b'
    board_pattern = r'board|surf'
    diving_pattern = r'\b(div(e|ing)?|scuba)\b'
    df2.loc[df2.activity.str.contains(r'sunbathing', case=False, na=False),'activity'] = 'other'
    df2.loc[df2.activity.str.contains(board_pattern, case=False, na=False),'activity'] = 'boarding'
    df2.loc[df2.activity.str.contains(no_board_pattern, case=False, na=False),'activity'] = 'swimming'
    df2.loc[df2.activity.str.contains(fishing_pattern, case=False, na=False),'activity'] = 'fishing'
    df2.loc[df2.activity.str.contains(diving_pattern, case=False, na=False),'activity'] = 'diving'
    
    return df2

def clean_col_sex(df):
    df2 = df.copy()
    df2.sex = df2.sex.replace({'m x 2':'m','lli':'m','n':'m','?':'unknown','.':'unknown'}) #visual inspection
    df2.sex = df2.sex.apply(lambda x: x.upper() if x in ['m','f'] else 'unknown')
    return df2

def clean_col_age(df):
    df2 = df.copy()
    df2.age = df2.age.replace({'!':''})
    df2.age = df2.age.str.replace(r'.*month.*','0',regex=True)
    pattern = r'.*?(\d+).*' #r'(\d+).*'
    df2.age = df2.age.str.replace(pattern,r'\1', regex=True)
    df2.age = df2.age.apply(lambda x: int(x) if str(x).isdigit() else 'unknown')
    return df2