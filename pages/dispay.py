#import os

#リストファイルを削除
#os.remove('list.txt')

import streamlit as st
import pickle
import datetime
import time

DIFF_JST_FROM_UTC = 9
now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)

ut_now = time.time()

f = open('./list.txt','rb')

def main():
	    
    st.title("UIL Dashboard")

    st.page_link("UIL_dashboard.py", label="Back to home page")
	
