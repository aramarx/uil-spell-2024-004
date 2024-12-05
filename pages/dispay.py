#import os

#リストファイルを削除
#os.remove('list.txt')

import streamlit as st
import pickle
import datetime
import time

def main():

    st.title("UIL Dashboard")

    st.page_link("app.py", label="Back to home page")

    st.write(
        "This dashboard was created by [Blaine Cowen](mailto:blaine.cowen@gmail.com)"
    )
	
if __name__ == "__main__":
    main()
