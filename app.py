import streamlit as st
from geopy.geocoders import Nominatim
import requests
import pandas as pd

def address_check(txt, address):
    if txt == 'From...' or txt == 'To...':
        pass
    elif address != None:
        st.write(f"Address: {address.address}")
    else:
        st.write("Address not found")


st.set_page_config(
    page_title=
    "NY Taxi Fare prediction interface",  # => Quick reference - Streamlit
    page_icon=":oncoming_taxi:",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed

nom = Nominatim(user_agent="my-app")

'''
# New York Taxifare Interface
'''

'''
#
'''
# Pickup
title = st.text_input('Pickup address', 'From...')
pickup = nom.geocode(title)
address_check(title, pickup)

# Dropoff
title = st.text_input('Dropoff address', 'To...')
dropoff = nom.geocode(title)
address_check(title, dropoff)

#Date Input
columns = st.columns(3)
my_date = columns[0].date_input("Select date")

#Time Input
my_time = columns[1].time_input('Select time')
datetime = str(my_date) + ' ' + str(my_time)

#Passengers number
pass_count = columns[2].selectbox('Number of passengers', [1,2,3,4,5,6,7,8])

#Dictionary containing the parameters for the API
params = dict(pickup_datetime=datetime,
              pickup_longitude=pickup.longitude,
              pickup_latitude=pickup.latitude,
              dropoff_longitude=dropoff.longitude,
              dropoff_latitude=dropoff.latitude,
              passenger_count=int(pass_count))

#API URL
taxifare_api_url = 'https://firstapi-mopnv4zura-ew.a.run.app/predict'

'''
#
'''

#Retrieve the response
columns2 = st.columns(3)
columns3 = st.columns(3)
if columns2[0].button('Get fare'):
    response = requests.get(taxifare_api_url, params=params)
    fare = round(response.json().get("prediction"),2)
    columns3[0].info(f'${fare}')

    map_data = pd.DataFrame({'lat': [pickup.latitude, dropoff.latitude],
    'lon': [pickup.longitude, dropoff.longitude]})
    st.map(map_data, zoom=10)
else:
    pass
