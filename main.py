import streamlit as st
import pickle
import datetime
import time

import streamlit_authenticator as stauth
import yaml

######################

# Define timezone difference
DIFF_JST_FROM_UTC = 9
ent_time = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)

start = time.time() 

# Load configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# Create an authenticator instance
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'],
)

# User login process
name, authentication_status, username = authenticator.login('main', 'main')


if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if st.session_state["authentication_status"]:
    # Successful login, redirect to the next page
    authenticator.logout('Logout', 'main')
    st.write(f'Login successful')		

	
        #After login process

    def main():
	    
    	# Add redirect to the page after login
    	st.experimental_rerun()
	    
	#st.title("UIL Dashboard")

    	#st.page_link("pages/dispay.py", label="Back to home page")
	
        ####
elif st.session_state["authentication_status"] is False:
    st.error('The username or password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password') 
