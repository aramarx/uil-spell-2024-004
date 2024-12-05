import streamlit as st
import pickle
import datetime
import time

import streamlit_authenticator as stauth
import yaml


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

    with st.form(key="1_form"): 


	    
	st.subheader('1号')
        #Text box
        tank1A= st.text_input(('1-A'),0)
        a1= st.checkbox("1a")
        tank1B= st.text_input(('1-B'),0)
        b1= st.checkbox("1b")
        tank1C= st.text_input(('1-C'),0)
        c1= st.checkbox("1c")
        st.write(f"---------")
               
        st.subheader('2号')
        #Text box
        tank2A= st.text_input(('2-A'),0)
        a2= st.checkbox("2a")
        tank2B= st.text_input(('2-B'),0)
        b2= st.checkbox("2b")
        tank2C= st.text_input(('2-C'),0)
        c2= st.checkbox("2c")
        st.write(f"---------")
                
        st.subheader('3号')
        #Text box
        tank3A= st.text_input(('3-A'),0)
        a3= st.checkbox("3a")
        tank3B= st.text_input(('3-B'),0)
        b3= st.checkbox("3b")
        tank3C= st.text_input(('3-C'),0)
        c3= st.checkbox("3c")
        st.write(f"---------")
        
        st.subheader('4号')
        #Text box
        tank4A= st.text_input(('4-A'),0)
        a4= st.checkbox("4a")
        tank4B= st.text_input(('4-B'),0)
        b4= st.checkbox("4b")
        tank4C= st.text_input(('4-C'),0)
        c4= st.checkbox("4c")
        st.write(f"---------")
                
        st.subheader('5号')
        #Text box
        tank5A= st.text_input(('5-A'),0)
        a5= st.checkbox("5a")
        tank5B= st.text_input(('5-B'),0)
        b5= st.checkbox("5b")
        tank5C= st.text_input(('5-C'),0)
        c5= st.checkbox("5c")
        st.write(f"---------")
                
        st.subheader('6号')
        #Text box
        tank6A= st.text_input(('6-A'),0)
        a6= st.checkbox("6a")
        tank6B= st.text_input(('6-B'),0)
        b6= st.checkbox("6b")
        tank6C= st.text_input(('6-C'),0)
        c6= st.checkbox("6c")
        st.write(f"---------")
                
        st.subheader('7号')
        #Text box
        tank7A= st.text_input(('7-A'),0)
        a7= st.checkbox("7a")
        tank7B= st.text_input(('7-B'),0)
        b7= st.checkbox("7b")
        tank7C= st.text_input(('7-C'),0)       
        c7= st.checkbox("7c")
        st.write(f"---------")
                
        st.subheader('8号')
        #Text box
        tank8A= st.text_input(('8-A'),0)
        a8= st.checkbox("8a")
        tank8B= st.text_input(('8-B'),0)
        b8= st.checkbox("8b")
        tank8C= st.text_input(('8-C'),0)
        c8= st.checkbox("8c")
        st.write(f"---------")
        
        consumption_rate = st.number_input('【------消費率------】') 
        hour_later = st.number_input('時間',0)

        
        submit_btn = st.form_submit_button("Submit")
        cancel_btn = st.form_submit_button("Cancel")
        st.write(f"ver 1.1")
        

    if submit_btn:

                
        #Create a list file
        f = open('list.txt','wb')
        
        list_start = []
        list_start.append(float(start))
                    
        list0 = []
        #list0.append(format(ent_time,'%Y/%m/%d'))
        #list0.append(format(ent_time,'%H:%M'))
        list0.append(format(ent_time,'%Y'))
        list0.append(format(ent_time,'%m'))
        list0.append(format(ent_time,'%d'))
        list0.append(format(ent_time,'%H'))
        list0.append(format(ent_time,'%M'))
                              
        list1 = []
        list1.append(float(tank1A))
        list1.append(float(tank1B))
        list1.append(float(tank1C))
                    
        list2 = []
        list2.append(float(tank2A))
        list2.append(float(tank2B))
        list2.append(float(tank2C))
                    
        list3 = []
        list3.append(float(tank3A))
        list3.append(float(tank3B))
        list3.append(float(tank3C))
                    
        list4 = []
        list4.append(float(tank4A))
        list4.append(float(tank4B))
        list4.append(float(tank4C))

        list5 = []
        list5.append(float(tank5A))
        list5.append(float(tank5B))
        list5.append(float(tank5C))
                    
        list6 = []
        list6.append(float(tank6A))
        list6.append(float(tank6B))
        list6.append(float(tank6C))
                    
        list7 = []
        list7.append(float(tank7A))
        list7.append(float(tank7B))
        list7.append(float(tank7C))
                        
        list8 = []
        list8.append(float(tank8A))
        list8.append(float(tank8B))
        list8.append(float(tank8C))
        
        consumption_list = []
        consumption_list.append(float(consumption_rate))
        hour_later_list = []
        hour_later_list.append(int(hour_later))  

                  
        #Save the list file 
        pickle.dump(list0,f)   
        pickle.dump(list1,f)
        pickle.dump(list2,f)
        pickle.dump(list3,f)
        pickle.dump(list4,f)
        pickle.dump(list5,f)
        pickle.dump(list6,f)
        pickle.dump(list7,f)
        pickle.dump(list8,f)
        pickle.dump(consumption_list,f)
        pickle.dump(hour_later_list,f)
        
        
        v1a = []
        v1b = []
        v1c = []
        v2a = []
        v2b = []
        v2c = []
        v3a = []
        v3b = []
        v3c = []
        v4a = []
        v4b = []
        v4c = []
        v5a = []
        v5b = []
        v5c = []
        v6a = []
        v6b = []
        v6c = []
        v7a = []
        v7b = []
        v7c = []
        v8a = []
        v8b = []
        v8c = []
        

        if a1:
            v1a.append('　←開')
        else:
            v1a.append('')
        if b1:
            v1b.append('　←開')
        else:
            v1b.append('')
        if c1:
            v1c.append('　←開')
        else:
            v1c.append('')   
        if a2:
            v2a.append('　←開')
        else:
            v2a.append('')
        if b2:
            v2b.append('　←開')
        else:
            v2b.append('')
        if c2:
            v2c.append('　←開')
        else:
            v2c.append('')  
        if a3:
            v3a.append('　←開')
        else:
            v3a.append('')
        if b3:
            v3b.append('　←開')
        else:
            v3b.append('')
        if c3:
            v3c.append('　←開')
        else:
            v3c.append('')         
        if a4:
            v4a.append('　←開')
        else:
            v4a.append('')
        if b4:
            v4b.append('　←開')
        else:
            v4b.append('')
        if c4:
            v4c.append('　←開')
        else:
            v4c.append('')         
        if a5:
            v5a.append('　←開')
        else:
            v5a.append('')
        if b5:
            v5b.append('　←開')
        else:
            v5b.append('')
        if c5:
            v5c.append('　←開')
        else:
            v5c.append('')         
        if a6:
            v6a.append('　←開')
        else:
            v6a.append('')
        if b6:
            v6b.append('　←開')
        else:
            v6b.append('')
        if c6:
            v6c.append('　←開')
        else:
            v6c.append('')         
        if a7:
            v7a.append('　←開')
        else:
            v7a.append('')
        if b7:
            v7b.append('　←開')
        else:
            v7b.append('')
        if c7:
            v7c.append('　←開')
        else:
            v7c.append('')         
        if a8:
            v8a.append('　←開')
        else:
            v8a.append('')
        if b8:
            v8b.append('　←開')
        else:
            v8b.append('')
        if c8:
            v8c.append('　←開')
        else:
            v8c.append('')         
            
        pickle.dump(v1a,f)
        pickle.dump(v1b,f)
        pickle.dump(v1c,f)
        pickle.dump(v2a,f)
        pickle.dump(v2b,f)
        pickle.dump(v2c,f)
        pickle.dump(v3a,f)
        pickle.dump(v3b,f)
        pickle.dump(v3c,f)
        pickle.dump(v4a,f)
        pickle.dump(v4b,f)
        pickle.dump(v4c,f)
        pickle.dump(v5a,f)
        pickle.dump(v5b,f)
        pickle.dump(v5c,f)
        pickle.dump(v6a,f)
        pickle.dump(v6b,f)
        pickle.dump(v6c,f)
        pickle.dump(v7a,f)
        pickle.dump(v7b,f)
        pickle.dump(v7c,f)
        pickle.dump(v8a,f)
        pickle.dump(v8b,f)
        pickle.dump(v8c,f)   
        
        pickle.dump(list_start,f)
        
        ####
elif st.session_state["authentication_status"] is False:
    st.error('The username or password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password') 
