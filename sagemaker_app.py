from textwrap import fill
import pickle
import requests
import json
import streamlit as st
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OrdinalEncoder
from PIL import Image

html_temp = """
<div style="background-color:#7EB294;padding:10px">
<h2 style="color:white;text-align:center;">Car Price Prediction </h2>
</div>"""
st.sidebar.markdown(html_temp,unsafe_allow_html=True)


html_temp = """
<div style="background-color:#7EB294;padding:10px">
<h3 style="color:white;text-align:center;">Autoscout Price Prediction </h3>
</div>"""
st.markdown(html_temp,unsafe_allow_html=True)


car_model=st.sidebar.selectbox("Select model of your car", ('Audi A1', 'Audi A3', 'Opel Astra', 'Opel Corsa', 'Opel Insignia', 'Renault Clio', 'Renault Duster', 'Renault Espace'))
gearing_type=st.sidebar.radio('Select gear type',('Automatic','Manual','Semi-automatic'))
age=st.sidebar.slider("What is the age of your car:",0,10, step=1)
hp=st.sidebar.slider("What is the hp_kw of your car?", 40, 300, step=5)
km=st.sidebar.slider("What is the km of your car", 0,350000, step=1000)

car_fotos= {'Audi A1':'Audi A1.jpeg' , 'Audi A3': 'Audi A3.jpg', 'Opel Astra':'opel-astra-electric-2022-04-min-1400x700.png', 
            'Opel Corsa': '01-opel-corsa-electric-fahrbericht-2023.jpg', 'Opel Insignia': 'Opel_Insignia.jpg',
              'Renault Clio': 'renault_clio.jpeg', 'Renault Duster':'novo-Renault-Duster.jpg', 'Renault Espace':'R escape.jpeg'}

if car_model in car_fotos:
    img = Image.open(car_fotos[car_model])
    st.image(img, caption="car model", width=300, use_column_width=True)
else:
    st.write("Car model not found in the database.")



richard_transformer = pickle.load(open('transformer', 'rb'))


my_dict = {
    "age": age,
    "hp_kW": hp,
    "km": km,
    'Gearing_Type':gearing_type,
    "make_model": car_model
    
}

df = pd.DataFrame.from_dict([my_dict])


st.header("The configuration of your car is below")
st.table(df)

df2 = richard_transformer.transform(df)
df2 = pd.DataFrame(df2)
df2.to_csv('df2.csv', index=False, header=False)
with open('df2.csv', 'r') as f:
    payload = f.read().strip('\n')

url = 'https://900ltjjiwg.execute-api.us-east-1.amazonaws.com/beta'

st.subheader("Press predict if configuration is okay")

 
# Single Observation
event = {
  "data": payload
  
}



response = requests.post(url, data=json.dumps(event))
result = response.json()

if st.button("Predict"):
    st.success("The estimated price of your car is €{} ".format(int(result)))
    


