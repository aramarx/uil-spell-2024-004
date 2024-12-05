import streamlit as st
import pickle
import datetime
import time

import streamlit_authenticator as stauth
import yaml

def main():
    st.title("UIL Dashboard")

    st.page_link("UIL_dashboard.py", label="Back to home page")

    st.header("Methodology")
    text1 = "Data is collected from the UIL website and stored in a database. The data is then cleaned to try to match the song that the director inputs to a song on the official PML list. \
        sometimes grades on the lists change, and songs are deleted, so the data is not always perfect. \
            Your support will help us improve the results, add new features, and keep the site running for years to come."

    st.write(text1)

    st.header("About Song Score")

    text2 = "Song Score is a metric that grades a song based on how it has performed at UIL competitions. \
        The score is calculated by comparing the average scores of a song by year and performance count since \
            the song as been released. The score is calculated by taking the percentile of the song's score vs the average score for that contest."

    text3 = "For example, the average score in 2006 was a 1.6. If a song scored straight 1's at that contest, it performed .6 points better than the average song. \
    The more performances a song has, the more accurate that score will be, so the song score will be higher."

    st.write(text2)
    st.write(text3)

    st.write(
        "This dashboard was created by [Blaine Cowen](mailto:blaine.cowen@gmail.com)"
    )
    # create buy me coffee image with link
    st.html(
        '<a href="https://www.buymeacoffee.com/blainecowen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 36px !important;width: 136px !important;" ></a>'
    )


if __name__ == "__main__":
    main()

######################

DIFF_JST_FROM_UTC = 9
ent_time = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)

start = time.time() 

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'],
)

name, authentication_status, username = authenticator.login('main', 'main')


if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Login successful')
		
  
        #After login process
  
        
        ####
elif st.session_state["authentication_status"] is False:
    st.error('The username or password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password') 
