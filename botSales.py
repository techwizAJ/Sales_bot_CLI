# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 15:27:41 2018
@author: arihant
Example Queries to be addressed 
    Sales for today 
    Sales for week
    Sales for month  or for any number of days
    Sales for any mentioned article or brands
    Top articles or brands sold in week ,month..
Considering Today as 31 AUG,2008 according to data given
"""
# Sales Info 
def salesInfo(df , date , brand= None, category = None):
    start, end = date, datetime.datetime(2018, 8, 31, 0, 0)
    df = df[ (df['sale_date'] >= start) &  (df['sale_date'] <= end) ] 
    if brand is not None:
        df = df[ (df['brand_name']==brand) ]
        return df['total_price'].sum()
    if category is not None:
        df = df[ (df['category_name']==category) ]
        return df['total_price'].sum()
    return df['total_price'].sum()

# Structured Response Type
def TopSalesInfo(df, date, brand = False, article =False):
    start, end = date, datetime.datetime(2018, 8, 31, 0, 0)
    df = df[ (df['sale_date'] >= start) &  (df['sale_date'] <= end) ] 
    if article:
        df2 = df[['id','name','total_price']]
        df2 = df2.groupby(['id', 'name']).sum()
        return df2.head()
    else:
        df2 = df[['id','brand_name','total_price']]
        df2 = df2.groupby(['id', 'brand_name']).sum()
        return df2.head()

# Entity Extractions
def getEntity_date(text):
    entities = { 'today':0 , 'yesterday':1 , 'week':7, 'month':30 }
    for w in entities:
        if w in text:
            loc = entities[w]
            t = datetime.datetime(2018, 8, 31-loc, 0, 0)
            return t
    return None
def entity_def(text):
    entities = ['sale','top']
    for w in entities:
        if w in text:
            loc = text.index(w)
            return text[loc]
    return None
def entity_type(text):
    entities =['article','brand']
    for w in entities:
        if w in text:
            loc = entities.index(w)
            print(loc)
            return True if loc == 0 else False
    return None
def entity_brand(text,df):
    brands = df['brand_name'].unique()
    for w in brands:
        if w in text:
            return w
    return None
def entity_category(text,df):
    category = df['category_name'].unique()
    for w in category:
        if w in text:
            return w
    return None
def response(df,def_type,date,types,brand,category):
    if def_type == 'sale':
        print('RS',salesInfo(df,date,brand,category))
    else:
        if types:
            print(TopSalesInfo(df,date,article =True))
        else:
            print(TopSalesInfo(df,date,brand =True ))

# Start Of Program          
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import datetime
import random
#Reading Data in Pandas DataFrames 
# All three .csv file to present with botSales.py 
articles = pd.read_csv('articles.csv')
train_bills = pd.read_csv('bills.csv')
hr = pd.read_csv('hierarchy.csv')
df = pd.merge(train_bills, hr, left_on='article_id', right_on='article_id', how='left')
df = pd.merge( df,articles ,left_on='article_id' , right_on='id' , how='left')
df['sale_date'] = pd.to_datetime(df['sale_date'])
close_greetings =[ 'bye' , 'goodbye','see you later','talk to you later','tada']
Pause_greet = ['Having some trouble looking at database' , 'Contact DB admin', 'Come again']
# Initializing bot
flag = True
while (flag==True):
    text = input('>>Speak to Sales Bot: ')
    text = text.lower()
    if ( text in close_greetings):
        flag= False
    # Removing stop words and Lemmatization using NLTK
    stop_words = set(stopwords.words("English"))
    words = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    fliter_sentence = []
    for w in words:
    	if w not in stop_words:
            fliter_sentence.append(lemmatizer.lemmatize(w))
    #Getting entity information   
    entity_date = getEntity_date(fliter_sentence)
    entitydef = entity_def(fliter_sentence)
    entitytype = entity_type(fliter_sentence)
    entitybrand = entity_brand(text,df)
    entitycategory = entity_category(text,df)
    if ( entitydef is None):
        random.choice(Pause_greet)
        break
    # response
    response(df,entitydef,entity_date,entitytype,entitybrand,entitycategory)