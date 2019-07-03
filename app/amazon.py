
from lxml import html  
import json
import os
from datetime import date
import requests
import pandas as pd
#from exceptions import ValueError
from time import sleep
import matplotlib.pyplot as plt

# csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "asin.csv")
# asin=df1=pd.read_csv(csv_filepath)
# AsinList=asin["ASIN"].values.tolist()
# print(AsinList)    





def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "asin.csv")
    asin=df1=pd.read_csv(csv_filepath)
    AsinList=asin['ASIN'].values.tolist()
    #AsinList = ['B01HSIIFQ2','B00BJB1L5C','B01MG4VZCT','B07H2JNF9V']
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print( "Processing: "+url)
        
        data,t=AmzonParser(url,i)
        
        while data['NAME'] == None:
            data,t=AmzonParser(url,i)
            
        if t:
            extracted_data.append(data)
        sleep(5)
    f=open('data.json','w')
    json.dump(extracted_data,f,indent=4)
    df=pd.DataFrame(extracted_data)
    df['date']=str(date.today())
    df['SALE_PRICE']=df['SALE_PRICE'].astype(str)
    df['SALE_PRICE']=df['SALE_PRICE'].str.slice(1)
    df['SALE_PRICE']=pd.to_numeric(df['SALE_PRICE'])
    final = pd.merge(df, asin, on=['ASIN'])
    
    with open('amazon.csv', 'a') as f:
        final.to_csv(f,header = False)
    print(df)
    df1=pd.read_csv('amazon.csv' )
    df2=df1.drop_duplicates(subset=['URL','date'])
    
#    print_graph(df2)



    
if __name__ == "__main__":
    ReadAsin()