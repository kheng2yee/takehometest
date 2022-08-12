#!/usr/bin/env python
# coding: utf-8

# #### Challenge 1

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import re

pd.set_option('display.max_rows', 500)


# In[ ]:


df_loyalty = pd.read_csv("loyalty.csv")
df_txn = pd.read_csv("transactions.csv")

df_join = pd.merge(df_loyalty[['id', 'license-plate']], df_txn, on='id', how='inner', suffixes = ("_l","_t"))


# In[ ]:


bins = [-1, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
labels = ["1. 0-250", "2. >250-500", "3. >500-750", "4. >750-1000", "5. >1000-1250", "6. >1250-1500", "7. >1500-1750", "8. >1750-2000"]
df_join['binned_amount'] = pd.cut(df_join['Amount'], bins=bins, labels=labels)
df_join['email_type'] = df_join['email'].apply(lambda x: x.split("@")[1])
df_join['area_code'] = df_join['phone-number'].apply(lambda x: x.split("-")[0].strip())


# #### Challenge 3

# In[ ]:


base_url = f"https://www.npanxxsource.com/area-codes.htm"

main_page0 = requests.get(base_url).text
doc0 = BeautifulSoup(main_page0, "html.parser")

area_table = doc0.findAll("table", id="npatab")[0]
TR_list = area_table.find("tbody").findAll("tr")

area_code_list = []
time_zone_list = []
region_list = []
country_list = []

for TR in TR_list:
    TD = TR.findAll("td")

    area_code, time_zone, region, country = TD[0].text, TD[3].text, TD[4].text, TD[5].text
    area_code_list.append(area_code)
    time_zone_list.append(time_zone)
    region_list.append(region)
    country_list.append(country)

df_scrape = pd.DataFrame(list(zip(area_code_list, time_zone_list, region_list, country_list))
                  , columns =['area_code', 'time_zone', 'region', 'country'])

df_scrape['area_code'] = df_scrape['area_code'].apply(lambda x: x.strip())

df_join2 = pd.merge(df_join, df_scrape, on="area_code", how="left")


# In[ ]:


# df_join2 is the final dataset with external data sources

