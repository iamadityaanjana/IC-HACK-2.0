import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
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

st.title('Results')

col1 , col2 = st.columns(2)

with col1:
 st.subheader('Category wise emissions')
 st.info(st.session_state.trans)
 st.info(st.session_state.waste)
 st.info(st.session_state.water)
 st.info(st.session_state.food)
 st.info(st.session_state.elec)

with col2:
 st.subheader('Total Carbon Emission')
 st.info(st.session_state.total)             
 st.info(st.session_state.per_person)
 if st.session_state.total_calc > 2.29 :
    st.warning('Your Emissions are more than national Average!')
 else:
    st.success('Your Emissions are less than national Average!', icon="✅")
    st.balloons()
 st.warning("In India average Co2 emission per capita is 2.29 tonnes per year")
 st.warning("In World average Co2 emission per capita is 4.70 tonnes per year")




data = {"footprint":["Your Average","National Average","World Average"],"Tonnes of Co2/year":[st.session_state.person_calc,2.29 , 4.70]}
data = pd.DataFrame(data)
data=data.set_index("footprint")
st.bar_chart(data)

if st.button("Learn More" , use_container_width=True , help="Get some educational content and provide us valuable feedback"):
 nav_page("Learn_More")