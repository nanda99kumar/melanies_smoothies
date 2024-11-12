# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie")
st.write(
    """choose from below:).
    """
)

#import streamlit as st
name_on_order=st.text_input('Name on smoothie')
st.write('Name on the smoothie is:', name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('choose 5',my_dataframe,max_selections=6);

if ingredients_list:
    ingredients_string=''
    for x in ingredients_list:
        ingredients_string+=x+' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',
            '"""+ name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ,'+name_on_order, icon="✅")
    
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text((smoothiefroot_response).json())
fv_df=st.dataframe(data=((smoothiefroot_response).json()), use_container_width=True)
