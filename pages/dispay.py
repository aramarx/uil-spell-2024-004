#import os

#リストファイルを削除
#os.remove('list.txt')

import streamlit as st
import pickle
import datetime
import time

def main():
	    
    st.title("UIL Dashboard")

    st.page_link("UIL_dashboard.py", label="Back to home page")
	
