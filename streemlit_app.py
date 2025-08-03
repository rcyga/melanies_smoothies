import streamlit as st

st.title(f"Customize your smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you for your smoothie!
  """)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

conn = st.connection("snowflake")
session = conn.session()
from snowflake.snowpark.functions import col
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections = 5
)

if ingredients_list:

    ingredients_string=''

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '  

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)

time_to_insert = st.button('Submit order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    
    st.success('Your Smoothie is ordered!' + ' ' + name_on_order, icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
