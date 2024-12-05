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
hour_later_list =pickle.load(f)


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
progress = (ut_now - start)/3600
#消費量
consumption = consumption_rate * (progress + hour_later)
#20時間
de = ut_now -start



entY = list0[0]
entm = list0[1]
entd = list0[2]
entH = list0[3]
entM = list0[4]


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
if '　←開' in v5b:
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
    
    if hour_later == 0:
            st.write(f"予測条件は{consumption_rate}/hで現在({later_.strftime('%H:%M')})")      
    else:
            st.write(f"予測条件は{consumption_rate}/hで{hour_later}時間後（{later_.strftime('%H:%M')}）")
      
    
    col1, = st.columns(1)
    
    with col1:
        st.subheader('---1号予測')
        st.subheader(f"**:red[A : {lv1a}{v1a[0]}]**")
        st.subheader(f"**:red[B : {lv1b}{v1b[0]}]**")
        st.subheader(f"**:red[C : {lv1c}{v1c[0]}]**")
        
        st.subheader('---2号予測')
        st.subheader(f"**:red[A : {lv2a}{v2a[0]}]**")
        st.subheader(f"**:red[B : {lv2b}{v2b[0]}]**")
        st.subheader(f"**:red[C : {lv2c}{v2c[0]}]**") 
        
        st.subheader('---3号予測')
        st.subheader(f"**:red[A : {lv3a}{v3a[0]}]**")
        st.subheader(f"**:red[B : {lv3b}{v3b[0]}]**")
        st.subheader(f"**:red[C : {lv3c}{v3c[0]}]**") 
        
        st.subheader('---4号予測')
        st.subheader(f"**:red[A : {lv4a}{v4a[0]}]**")
        st.subheader(f"**:red[B : {lv4b}{v4b[0]}]**")
        st.subheader(f"**:red[C : {lv4c}{v4c[0]}]**") 
        
        st.subheader('---5号予測')
        st.subheader(f"**:red[A : {lv5a}{v5a[0]}]**")
        st.subheader(f"**:red[B : {lv5b}{v5b[0]}]**")
        st.subheader(f"**:red[C : {lv5c}{v5c[0]}]**") 
        
        st.subheader('---6号予測')
        st.subheader(f"**:red[A : {lv6a}{v6a[0]}]**")
        st.subheader(f"**:red[B : {lv6b}{v6b[0]}]**")
        st.subheader(f"**:red[C : {lv6c}{v6c[0]}]**") 
        
        st.subheader('---7号予測')
        st.subheader(f"**:red[A : {lv7a}{v7a[0]}]**")
        st.subheader(f"**:red[B : {lv7b}{v7b[0]}]**")
        st.subheader(f"**:red[C : {lv7c}{v7c[0]}]**") 
        
        st.subheader('---8号予測')
        st.subheader(f"**:red[A : {lv8a}{v8a[0]}]**")
        st.subheader(f"**:red[B : {lv8b}{v8b[0]}]**")
        st.subheader(f"**:red[C : {lv8c}{v8c[0]}]**")
        st.write(f"---------") 
        st.write(f"※消費量は登録時に変更可能")
        st.write(f"※ページを開いた時からX時間が経過した予測です")       
