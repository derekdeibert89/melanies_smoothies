# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothe:')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)
    time_to_insert = st.button('Submit Order')
    
    insert_statement = """insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """','""" +name_on_order+"""')"""

    #st.write(insert_statement)

    if time_to_insert:
        session.sql(insert_statement).collect()
        success_string = """Your Smoothie is ordered, """+name_on_order+"""!"""
        st.success(success_string)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())