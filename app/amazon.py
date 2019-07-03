
from lxml import html 
import json
import os
from datetime import date
import requests
import pandas as pd
#from exceptions import ValueError
from time import sleep
import matplotlib.pyplot as plt

def AmzonParser(url,asin):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    t =True
    while t:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
 
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
 
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
 
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
 
            if page.status_code!=200:
                
               # raise ValueError('Page Not Found')
                t=False
            data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'ASIN':asin
                    }
 
            print(data)
            return data,t
        
        except Exception as e:
            print(e)


def print_graph(df):
    unique_list=pd.unique(df.URL)
    for values in unique_list:
        data_filter=df.loc[df['URL'] == values]
        title1=pd.unique(data_filter.NAME).astype(str)
        fullname = ''.join(title1)
        data_filter['date'] =  pd.to_datetime(data_filter['date'])
        data_filter.set_index('NAME')
        data_filter.plot(kind='line',x='date',y='SALE_PRICE',title=fullname[0:80],ax=plt.gca())
        plt.show()


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
    
    price_csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "amazon.csv")
    with open(price_csv_filepath, 'a') as f:
        final.to_csv(f,header = False)
    print(df)
    df1=pd.read_csv(price_csv_filepath)
    df2=df1.drop_duplicates(subset=['URL','date'])
    
    print_graph(df2)
    
if __name__ == "__main__":
    ReadAsin()