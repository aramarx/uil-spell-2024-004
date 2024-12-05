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

list0 = pickle.load(f)
list1 = pickle.load(f)
list2 = pickle.load(f)
list3 = pickle.load(f)
list4 = pickle.load(f)
list5 = pickle.load(f)
list6 = pickle.load(f)
list7 = pickle.load(f)
list8 = pickle.load(f)

consumption_list = pickle.load(f)
hour_later_list = pickle.load(f)


v1a = pickle.load(f)
v1b = pickle.load(f)
v1c = pickle.load(f)
v2a = pickle.load(f)
v2b = pickle.load(f)
v2c = pickle.load(f)
v3a = pickle.load(f)
v3b = pickle.load(f)
v3c = pickle.load(f)
v4a = pickle.load(f)
v4b = pickle.load(f)
v4c = pickle.load(f)
v5a = pickle.load(f)
v5b = pickle.load(f)
v5c = pickle.load(f)
v6a = pickle.load(f)
v6b = pickle.load(f)
v6c = pickle.load(f)
v7a = pickle.load(f)
v7b = pickle.load(f)
v7c = pickle.load(f)
v8a = pickle.load(f)
v8b = pickle.load(f)
v8c = pickle.load(f)

list_start = pickle.load(f)

    

#登録時間
start = list_start[0]
#消費率
consumption_rate = consumption_list[0]
#x時間後
hour_later = hour_later_list[0]
#x時間後の日時
later_ = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC + hour_later_list[0])
#経過時間
progress = ((ut_now - start)/3600 )
#消費量
consumption = consumption_rate * (progress+hour_later)
#20時間
de = ut_now -start

entY = list0[0]
entm = list0[1]
entd = list0[2]
entH = list0[3]
entM = list0[4]

print(start)
#print(ut_now)
#print (de)

#######
if '　←開' in v1a:
    lv1a = (list1[0] - consumption)
else:
    lv1a = list1[0]
lv1a = round(lv1a,2)   
if '　←開' in v1b:
    lv1b = (list1[1] - consumption)
else:
    lv1b = list1[1]
lv1b = round(lv1b,2) 
if '　←開' in v1c:
    lv1c = (list1[2] - consumption)
else:
    lv1c = list1[2]
lv1c = round(lv1c,2)

if '　←開' in v2a:
    lv2a = (list2[0] - consumption)
else:
    lv2a = list2[0]
lv2a = round(lv2a,2)   
if '　←開' in v2b:
    lv2b = (list2[1] - consumption)
else:
    lv2b = list2[1]
lv2b = round(lv2b,2) 
if '　←開' in v2c:
    lv2c = (list2[2] - consumption)
else:
    lv2c = list2[2]
lv2c = round(lv2c,2)

if '　←開' in v3a:
    lv3a = (list3[0] - consumption)
else:
    lv3a = list3[0]
lv3a = round(lv3a,2)   
if '　←開' in v3b:
    lv3b = (list3[1] - consumption)
else:
    lv3b = list3[1]
lv3b = round(lv3b,2) 
if '　←開' in v3c:
    lv3c = (list3[2] - consumption)
else:
    lv3c = list3[2]
lv3c = round(lv3c,2)  

if '　←開' in v4a:
    lv4a = (list4[0] - consumption)
else:
    lv4a = list4[0]
lv4a = round(lv4a,2)   
if '　←開' in v4b:
    lv4b = (list4[1] - consumption)
else:
    lv4b = list4[1]
lv4b = round(lv4b,2) 
if '　←開' in v4c:
    lv4c = (list4[2] - consumption)
else:
    lv4c = list4[2]
lv4c = round(lv4c,2)

if '　←開' in v5a:
    lv5a = (list5[0] - consumption)
else:
    lv5a = list5[0]
lv5a = round(lv5a,2)   
if '　←開' in v1b:
    lv5b = (list5[1] - consumption)
else:
    lv5b = list5[1]
lv5b = round(lv5b,2) 
if '　←開' in v5c:
    lv5c = (list5[2] - consumption)
else:
    lv5c = list5[2]
lv5c = round(lv5c,2)

if '　←開' in v6a:
    lv6a = (list6[0] - consumption)
else:
    lv6a = list6[0]
lv6a = round(lv6a,2)   
if '　←開' in v6b:
    lv6b = (list6[1] - consumption)
else:
    lv6b = list6[1]
lv6b = round(lv6b,2) 
if '　←開' in v6c:
    lv6c = (list6[2] - consumption)
else:
    lv6c = list6[2]
lv6c = round(lv6c,2)

if '　←開' in v7a:
    lv7a = (list7[0] - consumption)
else:
    lv7a = list7[0]
lv7a = round(lv7a,2)   
if '　←開' in v7b:
    lv7b = (list7[1] - consumption)
else:
    lv7b = list7[1]
lv7b = round(lv7b,2) 
if '　←開' in v7c:
    lv7c = (list7[2] - consumption)
else:
    lv7c = list7[2]
lv7c = round(lv7c,2)

if '　←開' in v8a:
    lv8a = (list8[0] - consumption)
else:
    lv8a = list8[0]
lv8a = round(lv8a,2)   
if '　←開' in v8b:
    lv8b = (list8[1] - consumption)
else:
    lv8b = list8[1]
lv8b = round(lv8b,2) 
if '　←開' in v8c:
    lv8c = (list8[2] - consumption)
else:
    lv8c = list8[2]
lv8c = round(lv8c,2)
######

#表示

if de >= 72000 :
    st.subheader(f"本日未登録")
    
else:
    st.subheader(f"**:red[{list0[0]}/{list0[1]}/{list0[2]}　{list0[3]}:{list0[4]}登録]**")
    
    col1, = st.columns(1)
    with col1:

        st.subheader('---1号---')
        st.subheader(f"A : {list1[0]}{v1a[0]}")
        st.subheader(f"B : {list1[1]}{v1b[0]}")
        st.subheader(f"C : {list1[2]}{v1c[0]}")

        st.subheader('---2号---')
        st.subheader(f"A : {list2[0]}{v2a[0]}")
        st.subheader(f"B : {list2[1]}{v2b[0]}")
        st.subheader(f"C : {list2[2]}{v2c[0]}")

        st.subheader('---3号---')
        st.subheader(f"A : {list3[0]}{v3a[0]}")
        st.subheader(f"B : {list3[1]}{v3b[0]}")
        st.subheader(f"C : {list3[2]}{v3c[0]}")

        st.subheader('---4号---')
        st.subheader(f"A : {list4[0]}{v4a[0]}")
        st.subheader(f"B : {list4[1]}{v4b[0]}")
        st.subheader(f"C : {list4[2]}{v4c[0]}")

        st.subheader('---5号---')
        st.subheader(f"A : {list5[0]}{v5a[0]}")
        st.subheader(f"B : {list5[1]}{v5b[0]}")
        st.subheader(f"C : {list5[2]}{v5c[0]}")

        st.subheader('---6号---')
        st.subheader(f"A : {list6[0]}{v6a[0]}")
        st.subheader(f"B : {list6[1]}{v6b[0]}")
        st.subheader(f"C : {list6[2]}{v6c[0]}")

        st.subheader('---7号---')
        st.subheader(f"A : {list7[0]}{v7a[0]}")
        st.subheader(f"B : {list7[1]}{v7b[0]}")
        st.subheader(f"C : {list7[2]}{v7c[0]}")
        
        st.subheader('---8号---')
        st.subheader(f"A : {list8[0]}{v8a[0]}")
        st.subheader(f"B : {list8[1]}{v8b[0]}")
        st.subheader(f"C : {list8[2]}{v8c[0]}")
        st.write(f"---------") 
        st.write(f"※左上の>からforecastをタップで予測値がみれる") 
        st.write(f"※登録日時は要確認です、前日の情報を見ているかも")       
        st.write(f"※登録時刻から20時間経過する
