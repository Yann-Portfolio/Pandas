#!/usr/bin/env python
# coding: utf-8

# Import
import glob
import pandas as pd
import matplotlib as pp
import matplotlib.pyplot as plt
import seaborn as sns

# Load and concatenate the different set of datas
# Data is published quaterly from https://opendata-ajuntament.barcelona.cat/data/es/dataset/est-mercat-immobiliari-lloguer-mitja-mensual
# Format is YYYY_lloguer_preu_trim.csv

all_files = glob.glob("Data/*.csv")
df = pd.concat((pd.read_csv(f) for f in all_files))

# Add a new column with Date, format YYYY-Quarter
df["Date"] = "Q"+ df["Trimestre"].astype(str) + " " + df['Any'].astype(str)
df["Date"] = pd.to_datetime(['-'.join(x.split()[::-1]) for x in df['Date']])

df.reset_index(drop=True)

# Clean the price column and transtype to float
df.replace("NA",'0', inplace=True)
df['Preu'] = pd.to_numeric(df['Preu'], errors='coerce')

#Split DataFrame in 2, one with the average rent and the other with the average rent per meter square
average_rent = df[df["Lloguer_mitja"]=="Lloguer mitjà mensual (Euros/mes)"].copy()
average_rent_per_size = df[df["Lloguer_mitja"]=="Lloguer mitjà per superfície (Euros/m2 mes)"].copy()
average_rent.reset_index(drop=True)
average_rent_per_size.reset_index(drop=True)
average_rent_per_size.index = average_rent.index
average_rent['price_per_m2'] = average_rent_per_size["Preu"]
average_rent['Size_per_barrio'] = average_rent['Preu'] / average_rent['price_per_m2']
price_per_barrio = average_rent.pivot(index='Date', columns='Nom_Barri', values='Preu')

g = sns.lineplot(
    data = average_rent.groupby(["Nom_Districte", "Date"])['Preu'].mean().reset_index(), 
    x = 'Date', 
    y = 'Preu', 
    hue = 'Nom_Districte'
)
g.set(title='Average rent per District')
g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=2)

g = sns.lineplot(
    data = average_rent.groupby(["Nom_Districte", "Date"])['Size_per_barrio'].mean().reset_index(), 
    x = 'Date', 
    y = 'Size_per_barrio', 
    hue = 'Nom_Districte'
)
g.set(title = "Average size per district")
g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=2)

#Time to dig into each district and have the data per barrio





# In[ ]:




