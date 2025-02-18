import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.header('Market of used vehicles')
st.write("""
         #### Filter the data below based on model and year
         # """)


df=pd.read_csv('vehicles_us.csv')

df['model_year']=df.groupby('model')['model_year'].transform(lambda x:x.fillna(x.median()))
df['model_year']=df['model_year'].astype(int)

df['cylinders']=df.groupby('model')['cylinders'].transform(lambda x:x.fillna(x.median()))

df['odometer']=df.groupby(['model','model_year'])['odometer'].transform(lambda x:x.fillna(x.median()))

df=df.drop(columns=['is_4wd'])

df['paint_color']=df['paint_color'].fillna('not_mentioned')
df['date_posted']=pd.to_datetime(df['date_posted'])
df['date_posted']=df['date_posted'].dt.date

Q1 =df['model_year'].quantile(0.25)
Q3 =df['model_year'].quantile(0.75)
IQR=Q3-Q1
year_max=Q3 + 1.5*IQR
year_min =Q1 -1.5*IQR

Q1 =df['price'].quantile(0.25)
Q3 =df['price'].quantile(0.75)
IQR=Q3-Q1
price_max=Q3 + 1.5*IQR
price_min =Q1 -1.5*IQR

data=df[(df['model_year'] >=year_min) & (df['model_year'] <=year_max) & (df['price'] >=price_min) & (df['price'] <=price_max)]
min_year, max_year =(data['model_year'].min()),(data['model_year'].max())
min_price, max_price =int(data['price'].min()), int(data['price'].max())


manufacturer_model =data['model'].unique()

selected_menu = st.selectbox('Select a model', manufacturer_model)
min_year, max_year =(data['model_year'].min()),(data['model_year'].max())
year_range=st.slider("Choose years", value=(min_year, max_year),min_value=min_year, max_value=max_year)
price_range=st.slider("Choose price", value=(min_price, max_price),min_value=min_price, max_value=max_price)
actual_range=list(range(year_range[0],year_range[1]+1))

filtered_df=data[(data.model==selected_menu) & (data.model_year.isin(list(actual_range)))]
filtered_df

st.header('Type of vehicle')
st.write("""
         ##### Let us analyze to find the most popular type of vehicle in the market
         """)

fig_1 =px.bar(data, x='type', color='model',title = 'Type of vehicle')
st.plotly_chart(fig_1)

st.header('Price Analysis')
st.write("""
         #####  Let us analyze the price of vehicle based on model year
         """)
fig_2=px.scatter(data, x='model_year', y='price', title='Model Year VS Price', hover_data=['model', 'type'])
st.plotly_chart(fig_2)

st.write("""
         #####  Analyze the price of vehicle based on type, fuel, colour of vehicle and transmission type
         """)

list_for_hist =['transmission', 'type', 'fuel', 'paint_color']
selected_type = st.selectbox('Split for price distribution', list_for_hist)
fig_3 =px.histogram(data, x='price', color=selected_type)
fig_3.update_layout(title ="<b> Split of price by {} </b>".format(selected_type))
st.plotly_chart(fig_3)

st.write("""
         #####  Analyze the price of vehicle based on odometer and number of cylinders with divisions on age category
         """)
def age_category(x):
    if x<5:
        return '<5'
    elif x>=5 and x<10:
        return '5-10'
    elif x>=10 and x<20:
        return '10-20'
    else:
        return '>20'
    
data['age']=2025-data['model_year']
data['age_category'] =data['age'].apply(age_category)
list_for_scatter = ['odometer', 'cylinders']
selected_type_scatter = st.selectbox('Price dependency on', list_for_scatter)
fig_4 =px.scatter(data, x='price', y=selected_type_scatter, color ='age_category', hover_data=['model_year', 'model'])
fig_4.update_layout(title ="<b> Price by {} </b>".format(selected_type_scatter))
st.plotly_chart(fig_4)
        