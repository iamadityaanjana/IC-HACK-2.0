import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=300):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

EMMISION_FACTOR = {
    "India 🇮🇳" :{
        "Transportation": 0.14,
        "Electricity": 0.82,
        "Food": 1.25,
        "Waste": 0.1,
        "Water":0.029,
    }
}
st.set_page_config(layout="wide", page_title="Carbon Calculator")

st.title('🍂Carbon Emission Calculator')

#Input Values for data collection and calculation 

st.subheader(" 🌏 Select your country ")
country = st.selectbox("Select", ["India 🇮🇳"])


col1, col2 = st.columns(2)

with col1:
    st.subheader("👨‍👩‍👧 Total Family members")
    members = st.number_input('No. of members', min_value= 1, step=1)

    st.subheader("🚙 Daily Commute Distance ")
    distance = st.number_input('in km',key = "distance_travelled",min_value=0, step=1)

    st.subheader("⚡️ Monthly electricity usage")
    electricity = st.number_input('In Kwh', key = "electricity_usage", step=1)

with col2:

    st.subheader("🍛 Daily Meals")
    food = st.number_input('Whole Family (no. of plates)', key = "Daily_meals", step=1)

    st.subheader("🚿 Daily water use(approx)")
    water = st.number_input('In litres', key = "water_usage", step=1)

    st.subheader("🗑️ Daily waste (approx)")
    waste = st.number_input('In kg', key = "waste_produced", step=1)

#converting units to monthly units
if distance > 0:
    distance = distance * 365 

if electricity > 0:
    electricity = electricity * 12

if water > 0:
    water = water * 365

if food > 0:
    food = food * 365

if waste > 0:
    waste = waste * 365

#Conversion using conversion factors ( different for different countries)

transport_emission = EMMISION_FACTOR[country]['Transportation'] * distance
electricity_emission = EMMISION_FACTOR[country]['Electricity'] * electricity
water_emission = EMMISION_FACTOR[country]['Water'] * water
waste_emission = EMMISION_FACTOR[country]['Waste'] * waste
food_emission = EMMISION_FACTOR[country]['Food'] * food

#conversion to tonnes of emission and aprroximating waste

transport_emission = round( transport_emission/1000 , 2)
electricity_emission = round( electricity_emission/1000 , 2)
water_emission = round(water_emission/1000 , 2)
waste_emission = round(waste_emission/1000 , 2)
food_emission = round(food_emission/1000 , 2)


Total_Emissions = round(
    transport_emission + electricity_emission + water_emission + waste_emission + food_emission , 2 ,
)
Per_Person_emission = round(
    (Total_Emissions)/members , 2
)

       
#Creating sessions states to store value of variables across web pages temporarily
st.session_state.trans = (f"🚙 Transportation: {transport_emission} Tonnes of Co2 / year")
st.session_state.food = (f"🍛 Food: {food_emission} Tonnes of Co2 / year")
st.session_state.water = (f"🚿 Water: {water_emission} Tonnes of Co2 / year")
st.session_state.waste = (f"🗑️ Waste: {waste_emission} Tonnes of Co2 / year")
st.session_state.elec = (f"⚡️ Electricity: {electricity_emission} Tonnes of Co2 / year")

st.session_state.total = (f"Total Carbon Footprint: {Total_Emissions} Tonnes of Co2 / Year")
st.session_state.per_person = (f"Emission Per Person:{Per_Person_emission} Tonnes of Co2 / year")
st.session_state.total_calc = Total_Emissions
st.session_state.person_calc = Per_Person_emission


if st.button("Go to Results" , use_container_width=True , help='Get Calculations for your carbon footprint'):
 nav_page("Results")
